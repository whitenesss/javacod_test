# Задача - Поиск элемента в упорядоченном списке
# Дан отсортированный список чисел, например: [1, 2, 3, 45, 356, 569, 600, 705, 923]
#
# Список может содержать миллионы элементов.
#
# Необходимо написать функцию search(number: id)
# -> bool которая принимает число number и возвращает True если это число находится в этом списке.
#
# Требуемая сложность алгоритма O(log n).


numbers = [1, 2, 3, 45, 356, 569, 600, 705, 923]


def search(numbers: list[int], number: int) -> bool:
    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        print(mid)
        print(numbers[mid])
        if numbers[mid] == number:
            return True
        elif numbers[mid] < number:
            left = mid + 1
        else:
            right = mid - 1
    return False


if __name__ == "__main__":
    assert search(numbers, 3) is True
    assert search(numbers, 9999999) is False
