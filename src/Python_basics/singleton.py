# Задача - Синглтон
# Реализуйте паттерн синглтон тремя способами:
#
# с помощью метаклассов
# с помощью метода __new__ класса
# через механизм импортов
from src.Python_basics.singleton_modul import singleton_instance


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonMetaClass(metaclass=SingletonMeta):
    """
    с помощью метаклассов
    """

    def __init__(self, value):
        self.value = value


class SingletonNew:
    """
    с помощью __new__ класса
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value


if __name__ == "__main__":
    obj_1 = SingletonMetaClass(1)
    obj_2 = SingletonMetaClass(2)
    assert (obj_1 is obj_2) is True
    obj_1 = SingletonNew(2)
    obj_2 = SingletonNew(3)
    assert (obj_1 is obj_2) is True
    obj_1 = singleton_instance
    obj_2 = singleton_instance
    assert (obj_1 is obj_2) is True
    print("✅ Все тесты пройдены!")
