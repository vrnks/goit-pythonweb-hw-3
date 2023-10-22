import time
from multiprocessing import Pool, cpu_count


def factorize(*number):
    """Функція factorize, яка приймає список чисел та повертає список чисел, на які числа з вхідного списку поділяються без залишку"""
    result = []
    for num in number:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        result.append(factors)
    return result


numbers = (128, 255, 99999, 10651060)
start_time = time.time()
results = factorize(*numbers)
end_time = time.time()
print(f"Синхронне виконання зайняло {end_time - start_time:.2f} секунд.")


def factorize_parallel(*numbers):
    pool = Pool(cpu_count())  # Використовуємо кількість доступних ядер
    results = pool.map(factorize, numbers)
    pool.close()
    pool.join()
    return results


if __name__ == "__main__":
    numbers = (128, 255, 99999, 10651060)

    start_time = time.time()
    results = factorize_parallel(*numbers)
    end_time = time.time()

    print(f"Паралельне виконання зайняло {end_time - start_time:.2f} секунд.")
