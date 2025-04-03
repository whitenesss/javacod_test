import json
import math
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor

from multiprocessing import Pool, cpu_count, Queue, Process


def generate_data(n):
    """Генерирует список из n случайных чисел от 1 до 1000."""
    return [random.randint(1, 1000) for _ in range(n)]


def process_number(n):
    """Вычисляет факториал числа (ресурсоёмкая операция)."""
    return math.factorial(
        n % 20
    )  # Ограничиваем факториал до 20, чтобы избежать слишком больших чисел


def sequential_processing(numbers):
    """Однопоточная обработка списка чисел."""
    start_time = time.time()
    results = [process_number(n) for n in numbers]
    end_time = time.time()
    return results, end_time - start_time


def thread_pool_processing(numbers):
    """Параллельная обработка с использованием пула потоков."""
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_number, numbers))
    end_time = time.time()
    return results, end_time - start_time


def process_pool_processing(numbers):
    """Параллельная обработка с использованием пула процессов."""
    start_time = time.time()
    with Pool(cpu_count()) as pool:  # Используем все ядра
        results = pool.map(process_number, numbers)
    end_time = time.time()
    return results, end_time - start_time


def worker(q, numbers):
    """Процесс, который обрабатывает список чисел и кладёт в очередь."""
    results = [process_number(n) for n in numbers]
    q.put(results)


def process_queue_processing(numbers):
    """Обрабатываем данные, распределяя их по процессам с использованием очереди."""
    start_time = time.time()
    q = Queue()
    chunk_size = len(numbers) // cpu_count()
    processes = []

    for i in range(cpu_count()):
        chunk = numbers[i * chunk_size : (i + 1) * chunk_size]
        p = Process(target=worker, args=(q, chunk))
        processes.append(p)
        p.start()

    results = []
    for _ in range(cpu_count()):
        results.extend(q.get())

    for p in processes:
        p.join()

    end_time = time.time()
    return results, end_time - start_time


def save_results(file_name, data):
    """Сохраняет результаты в JSON."""
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    numbers = generate_data(100000)  # Генерируем 100 000 чисел

    methods = {
        "Sequential": sequential_processing,
        "ThreadPool": thread_pool_processing,
        "ProcessPool": process_pool_processing,
        "ProcessQueue": process_queue_processing,
    }

    results = {}

    for name, method in methods.items():
        print(f"Запуск {name}...")
        _, duration = method(numbers)
        results[name] = duration

    save_results(os.path.join(os.getcwd(), 'src/multiproc_python/results.json'), results)

    print("\n Время выполнения:")
    for key, value in results.items():
        print(f"{key}: {value:.2f} сек")
    print("✅ Все тесты пройдены!")