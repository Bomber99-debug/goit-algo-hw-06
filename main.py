from collections import UserDict


class Field:
    """Базовий клас для полів контакту (ім'я, телефон тощо)."""

    def __init__(self, value: str):
        self.value: str = value  # зберігаємо значення поля

    def __str__(self) -> str:
        return str(self.value)  # рядкове представлення поля


class Name(Field):
    """Поле для імені контакту (без додаткової логіки)."""
    pass


class Phone(Field):
    """Поле для номера телефону з валідацією."""

    def __init__(self, value: str):
        # Перевірка: номер має містити рівно 10 цифр
        if len(value) != 10 and not value.isdigit():
            raise ValueError(f"Phone number '{self.value}' is not valid")
        super().__init__(value)


class Record:
    """Запис контакту: ім'я та список телефонів."""

    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.phones: list[Phone] = []  # список телефонів контакту

    def add_phone(self, value: str) -> None:
        """Додає новий телефон до контакту."""
        self.phones.append(Phone(value))

    def remove_phone(self, value: str | Phone) -> None:
        """Видаляє телефон, якщо він існує."""
        if isinstance(value, str):
            value = self.find_phone(value)
        if value:
            self.phones.remove(value)

    def edit_phone(self, value: str, replace: str) -> None:
        """Замінює існуючий телефон на новий."""
        phone_obj = self.find_phone(value)
        if phone_obj:
            self.remove_phone(phone_obj)
            self.add_phone(replace)
        else:
            raise ValueError(f"The phone number '{value}' is not in the contact's phone list")

    def find_phone(self, value: str) -> Phone | None:
        """Повертає об'єкт Phone, якщо знайдено, або None."""
        return next((i for i in self.phones if i.value == value), None)

    def __str__(self) -> str:
        """Рядкове представлення контакту з усіма телефонами."""
        return f"Contact name: {self.name.value}, phones: {', '.join(i.value for i in self.phones)}"


class AddressBook(UserDict):
    """Сховище контактів (ключ — ім'я, значення — Record)."""

    def add_record(self, value: Record) -> None:
        """Додає Record у AddressBook."""
        self.data[value.name.value] = value

    def find(self, value: str) -> Record | None:
        """Повертає Record за ім'ям або None, якщо не знайдено."""
        return self.data.get(value)

    def delete(self, value: str) -> None:
        """Видаляє контакт за ім'ям, якщо він існує."""
        if value in self.data:
            del self.data[value]
        else:
            raise ValueError(f"Name '{value}' is not found in AddressBook")

    def __str__(self) -> str:
        """Рядкове представлення всіх контактів."""
        return '\n'.join(str(v) for v in self.data.values())
