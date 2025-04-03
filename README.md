## Описание задач и запуск

1. Декоратор кеширования (LRU Cache)
Реализация lru_cache декоратора.

### Запуск:
```bash
python -m src.Python_basics.decor
````
2. Паттерн Singleton
Реализация синглтона тремя способами:
Через метаклассы
Через __new__
Через механизм импортов

### Запуск:
```bash
python -m src.Python_basics.singleton
```

3. Метакласс с атрибутом created_at
Метакласс автоматически добавляет атрибут created_at с текущей датой.
### Запуск:

```bash
python -m src.Python_basics.meta_class_created_at
```
4. Поиск элемента в упарядоченном  списке
Функция search(number: int) -> bool реализует бинарный поиск с O(log n).
### Запуск:

```bash
python -m src.data_structure.search_data
```
5. Асинхронный HTTP-запрос
Функция fetch_urls(urls: list[str]) отправляет запросы и сохраняет результат.
Асинхронный HTTP-запрос. Продвинутая реализация.
### Запуск:

```bash
python -m src.async_python.async

```
```bash
python -m src.async_python.async_pro
```
6. Параллельная обработка чисел
Реализованы три варианта обработки данных:

ThreadPoolExecutor

multiprocessing.Pool

multiprocessing.Queue

### Запуск:

```bash
python -m src.multiproc_python.process_all
```
7. ASGI / WSGI Прокси для курса валют
Приложение отдаёт курс валюты через API https://api.exchangerate-api.com/v4/latest/USD.

Запуск:

```bash
python -m src.WSGI_ASGI.exchange_proxy
```