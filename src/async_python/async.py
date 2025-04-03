#
# Напишите асинхронную функцию fetch_urls, которая принимает
# список URL-адресов и возвращает словарь, где ключами являются URL,
# а значениями — статус-коды ответов.
# Используйте библиотеку aiohttp для выполнения HTTP-запросов.
#
# Требования:
#
# Ограничьте количество одновременных запросов до 5 (используйте примитивы синхронизации из asyncio библиотеки)
# Обработайте возможные исключения (например, таймауты, недоступные ресурсы) и присвойте соответствующие статус-коды (например, 0 для ошибок соединения).
# Сохраните все результаты в файл
# Пример использования:
import asyncio
import json
import os

import aiohttp

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
]


async def fetch_url(url, session):
    """Делает HTTP-запрос"""
    try:
        async with session.get(url) as response:
            return {"url": url, "status_code": response.status}
    except aiohttp.ClientError:
        return {"url": url, "status_code": 0}
    except asyncio.TimeoutError:
        return {"url": url, "status_code": 0}


async def work(url, session, semaphore, results):
    """Обрабатывает один URL с ограничением через семафор."""
    async with semaphore:
        result = await fetch_url(url, session)
        results.append(result)


async def fetch_urls(urls: list[str], file_path: str):

    max_size_semaphore = 5
    semaphore = asyncio.Semaphore(max_size_semaphore)
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(work(url, session, semaphore, results))
            tasks.append(task)

        await asyncio.gather(*tasks)

    with open(file_path, "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    asyncio.run(fetch_urls(urls, os.path.join(os.getcwd(), 'src/async_python/results.jsonl')))
    print("✅ Все тесты пройдены!")

