from collections import UserDict


class Field:  # Базовий клас для полів запису (ім'я, телефон і т.д.)
    def __init__(self, value: str):
        self.value = value  # зберігаємо значення поля

    def __str__(self) -> str:
        return str(self.value)  # рядкове представлення поля


class Name(Field):  # Клас для зберігання імені контакту
    pass  # без додаткової логіки, просто зберігає значення Name


class Phone(Field):  # Клас для зберігання номера телефону з валідацією
    def __init__(self, value: str):
        super().__init__(value)

        # Видаляємо всі небуквені символи, залишаємо лише цифри
        phone = ''.join(i for i in self.value if i.isdigit())

        # Перевірка коректності номера: повинен містити рівно 10 цифр
        if len(phone) == 10:
            self.value = phone
        else:
            raise ValueError(f"Phone number '{self.value}' is not valid")


class Record:  # Клас для зберігання інформації про контакт
    def __init__(self, name: str):
        self.name = Name(name)  # обов'язкове поле, ім'я контакту
        self.phones: list[str] = []  # список телефонів контакту

    # Технічний метод: створює об'єкт Phone для валідації номера
    def __validate_phone(self, value: str) -> str:
        phone = Phone(value)  # якщо номер некоректний — викликає ValueError
        return phone.value

    # Додає новий телефон до запису
    def add_phone(self, value: str) -> None:
        self.phones.append(self.__validate_phone(value))

    # Видаляє телефон зі списку контактів, якщо він існує
    def remove_phone(self, value: str) -> None:
        phone_del = self.__validate_phone(value)
        if phone_del in self.phones:
            self.phones.remove(phone_del)

    # Замінює старий телефон на новий
    def edit_phone(self, value: str, replace: str) -> None:
        old_phone = self.__validate_phone(value)
        new_phone = self.__validate_phone(replace)
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = new_phone
        else:
            # Технічне повідомлення про відсутність номера
            raise ValueError(f"The phone number '{old_phone}' is not in the contact's phone list")

    # Пошук телефону у списку контактів
    def find_phone(self, value: str) -> str | None:
        """Повертає знайдений номер, або None, якщо не існує"""
        if value in self.phones:
            return value
        return None

    def __str__(self) -> str:
        # Рядкове представлення контакту із усіма телефонами
        return f"Contact name: {self.name.value}, phones: {', '.join(self.phones)}"


class AddressBook(UserDict):  # Клас для зберігання та управління записами
    # Додає Record у AddressBook; ключ — ім'я контакту
    def add_record(self, value: Record):
        self.data[value.name.value] = value

    # Повертає Record по імені контакту
    def find(self, value: str) -> Record:
        return self.data[value]

    # Видаляє Record за іменем, якщо існує
    def delete(self, value: str) -> None:
        if value in self.data:
            del self.data[value]
        else:
            # Технічне повідомлення про відсутній контакт
            raise ValueError(f"Name '{value}' is not found in AddressBook")

    def __str__(self) -> str:
        # Красивий друк всіх контактів у AddressBook
        # Використовує __str__ Record
        return '\n'.join(str(v) for v in self.data.values())
