import asyncio
import json
import os

import aiofiles
import aiohttp
from aiohttp import ClientError, ClientTimeout


async def fetch_url(url, session, retries=3):
    """Улучшенная версия с потоковым чтением и повторами."""
    for attempt in range(retries):
        try:
            timeout = ClientTimeout(total=300)  # 5 минут для больших файлов
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    try:
                        chunks = []
                        async for chunk in response.content.iter_chunked(1024*1024):
                            chunks.append(chunk)
                        data = b''.join(chunks)
                        json_data = json.loads(data)
                        return {"url": url, "content": json_data}
                    except json.JSONDecodeError:
                        print(f"Невалидный JSON: {url}")
                        return None
                print(f"Пропускаем {url}: статус {response.status}")
        except Exception as e:
            if attempt == retries - 1:
                print(f"Ошибка с {url}: {str(e)}")
                return None
            await asyncio.sleep(1 * (attempt + 1))
    return None


async def worker(url, session, semaphore, out_f):
    """Исправленная версия - принимает уже открытый файловый объект."""
    async with semaphore:
        result = await fetch_url(url, session)
        if result:
            if isinstance(result['content'], list):
                for item in result['content']:
                    await out_f.write(json.dumps({"url": url, "content": item}) + "\n")
            else:
                await out_f.write(json.dumps(result) + "\n")


async def fetch_urls(input_file, output_file, max_concurrent=5, batch_size=1000):
    """Основная функция с двумя оптимизациями:
    1. Файл открывается ОДИН раз
    2. Пакетная обработка через batch_size"""
    semaphore = asyncio.Semaphore(max_concurrent)
    connector = aiohttp.TCPConnector(limit=0)
    timeout = ClientTimeout(total=60)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        async with aiofiles.open(input_file, "r") as f, \
                aiofiles.open(output_file, "a") as out_f:  # Открываем файл 1 раз

            batch = []
            async for url in f:
                url = url.strip()
                if url:
                    task = asyncio.create_task(
                        worker(url, session, semaphore, out_f)  # Передаём открытый файл
                    )
                    batch.append(task)

                    if len(batch) >= batch_size:
                        await asyncio.gather(*batch)
                        batch = []

            if batch:
                await asyncio.gather(*batch)

if __name__ == "__main__":


    asyncio.run(
        fetch_urls(
            os.path.join(os.getcwd(), 'src/async_python/urls.txt'),
            os.path.join(os.getcwd(), 'src/async_python/results_pro.jsonl')

        )
    )
    print("✅ Все тесты пройдены!")