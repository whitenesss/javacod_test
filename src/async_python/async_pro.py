import asyncio
import json
import os

import aiofiles
import aiohttp
from aiohttp import ClientError, ClientTimeout


async def fetch_url(url, session):
    """Делает HTTP-запрос и возвращает JSON, если статус 200."""
    try:
        async with session.get(url, timeout=ClientTimeout(total=30)) as response:
            if response.status == 200:
                try:
                    data = await response.read()
                    json_data = json.loads(data)
                    return {"url": url, "content": json_data}
                except json.JSONDecodeError:
                    print(f"Невалидный JSON: {url}")
                    return None
            print(f"Пропускаем {url}: статус {response.status}")
    except ClientError as e:
        print(f"Ошибка с {url}: {str(e)}")
    return None


async def worker(url, session, semaphore, output_file):
    """Обрабатывает один URL с ограничением через семафор."""
    async with semaphore:
        result = await fetch_url(url, session)
        if result:
            async with aiofiles.open(output_file, "a") as f:
                await f.write(json.dumps(result) + "\n")


async def fetch_urls(input_file, output_file, max_concurrent=5):
    """Читает URL из файла и запускает асинхронные задачи."""
    semaphore = asyncio.Semaphore(max_concurrent)
    connector = aiohttp.TCPConnector(limit=0)
    timeout = ClientTimeout(total=60)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        async with aiofiles.open(input_file, "r") as f:
            tasks = []
            async for url in f:
                url = url.strip()
                if url:
                    task = asyncio.create_task(
                        worker(url, session, semaphore, output_file)
                    )
                    tasks.append(task)
            await asyncio.gather(*tasks)


if __name__ == "__main__":


    asyncio.run(
        fetch_urls(
            os.path.join(os.getcwd(), 'src/async_python/urls.txt'), os.path.join(os.getcwd(), 'src/async_python/results_pro.jsonl')
        )
    )
    print("✅ Все тесты пройдены!")