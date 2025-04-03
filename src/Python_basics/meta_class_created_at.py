# Задача - Атрибуты класса
# Напишите метакласс, который автоматически добавляет атрибут
# created_at с текущей датой и временем к
# любому классу, который его использует.

import time
from datetime import datetime


class AutoCreatedATMeta(type):
    """Метакласс, добавляющий created_at с текущим временем."""

    def __new__(cls, name, bases, namespace):
        namespace["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, namespace)


class NameClass(metaclass=AutoCreatedATMeta):
    pass


if __name__ == "__main__":
    created_at_time = NameClass.created_at
    time.sleep(1)
    assert created_at_time <= datetime.now()
    print(f"NameClass.created_at: {created_at_time}")
    print("✅ Все тесты пройдены!")
