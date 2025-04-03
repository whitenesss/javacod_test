import asyncio
import json
import os
from urllib.parse import urlparse

import aiofiles
import aiohttp
from aiohttp import ClientError, ClientTimeout, TCPConnector


class SmartTimeout:
    """Динамический таймаут на основе ожидаемого размера файла"""

    def __init__(self):
        self.base_timeout = 30  # Базовый таймаут 30 секунд
        self.per_mb_timeout = 2  # +2 секунды на каждый МБ

    def calculate(self, content_length):
        if not content_length:
            return self.base_timeout

        size_mb = content_length / (1024 * 1024)
        return min(
            self.base_timeout + int(size_mb * self.per_mb_timeout),
            300  # Максимальный таймаут 5 минут
        )


async def fetch_url(url, session, retries=3):
    """Упрощенная загрузка с умным таймаутом"""
    for attempt in range(retries):
        try:
            # Сначала HEAD запрос для определения размера
            async with session.head(url) as head_resp:
                content_length = int(head_resp.headers.get('Content-Length', 0))
                timeout = SmartTimeout().calculate(content_length)

            # Основной запрос с рассчитанным таймаутом
            async with session.get(
                    url,
                    timeout=ClientTimeout(total=timeout)
            ) as response:
                if response.status == 200:
                    try:
                        data = await response.read()
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
    """Обработчик с защитой от ошибок записи"""
    async with semaphore:
        result = await fetch_url(url, session)
        if result:
            try:
                await out_f.write(json.dumps(result) + "\n")
            except Exception as e:
                print(f"Ошибка записи для {url}: {str(e)}")


async def fetch_urls(input_file, output_file, max_concurrent=5):
    """Упрощенная основная функция"""
    connector = TCPConnector(
        limit=max_concurrent * 2,
        limit_per_host=5,
        force_close=True
    )

    semaphore = asyncio.Semaphore(max_concurrent)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with aiofiles.open(input_file, "r") as f, \
                aiofiles.open(output_file, "a") as out_f:

            tasks = []
            async for url in f:
                url = url.strip()
                if url and urlparse(url).scheme in ('http', 'https'):
                    task = asyncio.create_task(
                        worker(url, session, semaphore, out_f)
                    )
                    tasks.append(task)

                    if len(tasks) >= max_concurrent * 2:
                        done, pending = await asyncio.wait(
                            tasks,
                            return_when=asyncio.FIRST_COMPLETED
                        )
                        tasks = list(pending)

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(
        fetch_urls(
            os.path.join(os.getcwd(), 'src/async_python/urls.txt'),
            os.path.join(os.getcwd(), 'src/async_python/results_pro.jsonl'),
            max_concurrent=5
        )
    )
    print("✅ Все тесты пройдены!")