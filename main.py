from collections import UserDict
from dbm import error


class Field:  # Базовий клас для полів запису.
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):  # Клас для зберігання імені контакту. Обов'язкове поле.
    pass


class Phone(Field):  # Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    def __init__(self, value: str):
        super().__init__(value)

        phone = ''.join(i for i in self.value if i.isdigit())
        if len(phone) == 10:
            self.value = phone
        else:
            raise ValueError(f"Phone number '{self.value}' is not valid")


class Record:  # Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __validate_phone(self, value: str) -> str | None:
        phone = Phone(value)
        return phone.value

    def add_phone(self, value: str) -> None:
        self.phones.append(self.__validate_phone(value))

    def remove_phone(self, value: str) -> None:
        phone_del = self.__validate_phone(value)
        if phone_del in self.phones:
            self.phones.remove(phone_del)

    def find_phone(self, value: str, replace: str) -> None:
        old_phone = self.__validate_phone(value)
        new_phone = self.__validate_phone(replace)
        if old_phone in  self.phones:
            self.phones[self.phones.index(old_phone)] = new_phone

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {', '.join(p for p in self.phones)}"


class AddressBook(UserDict):  # Клас для зберігання та управління записами.
    def add_record(self, value: Record):
        self.data[value.name.value] = value

    def __str__(self):
        return '\n'.join(str(v) for v in self.data.values())

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")


# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі

print(book)