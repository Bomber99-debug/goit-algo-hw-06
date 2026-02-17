from collections import UserDict
from dbm import error


class Field:  # Базовий клас для полів запису (ім'я, телефон і т.д.)
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):  # Клас для зберігання імені контакту
    pass  # Логіка додаткової обробки не потрібна, просто зберігає значення


class Phone(Field):  # Клас для зберігання номера телефону з валідацією
    def __init__(self, value: str):
        super().__init__(value)

        # Залишаємо лише цифри
        phone = ''.join(i for i in self.value if i.isdigit())
        if len(phone) == 10:  # перевірка довжини номера
            self.value = phone
        else:
            raise ValueError(f"Phone number '{self.value}' is not valid")


class Record:  # Клас для зберігання інформації про контакт
    def __init__(self, name):
        self.name = Name(name)  # обов'язкове поле
        self.phones = []  # список телефонів

    # Валідація номера через створення об'єкта Phone
    def __validate_phone(self, value: str) -> str | None:
        phone = Phone(value)
        return phone.value

    # Додає телефон до запису
    def add_phone(self, value: str) -> None:
        self.phones.append(self.__validate_phone(value))

    # Видаляє телефон із запису
    def remove_phone(self, value: str) -> None:
        phone_del = self.__validate_phone(value)
        if phone_del in self.phones:
            self.phones.remove(phone_del)

    # Замінює старий телефон на новий
    def find_phone(self, value: str, replace: str) -> None:
        old_phone = self.__validate_phone(value)
        new_phone = self.__validate_phone(replace)
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = new_phone

    def __str__(self) -> str:
        # Красивий друк контактів із усіма телефонами
        return f"Contact name: {self.name.value}, phones: {', '.join(p for p in self.phones)}"


class AddressBook(UserDict):  # Клас для зберігання та управління записами
    def add_record(self, value: Record):
        # Зберігаємо об'єкт Record, ключ — ім'я контакту
        self.data[value.name.value] = value

    def __str__(self):
        # Красивий друк усіх записів через __str__ Record
        return '\n'.join(str(v) for v in self.data.values())