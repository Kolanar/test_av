import os
import json
from typing import List, Optional, Dict


class Contact:
    def __init__(self, surname: str, name: str, patronymic: str, organization: str, work_phone: str,
                 personal_phone: str):
        """Создает новый контакт с фамилией, именем, отчеством, организацией и телефонами."""
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    def to_dict(self) -> Dict:
        """Приобразуем контакт в словарь для записи в файл."""
        return {
            "surname": self.surname,
            "name": self.name,
            "patronymic": self.patronymic,
            "organization": self.organization,
            "work_phone": self.work_phone,
            "personal_phone": self.personal_phone,
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Contact':
        """Создает контакт из словаря."""
        return Contact(
            data["surname"],
            data["name"],
            data["patronymic"],
            data["organization"],
            data["work_phone"],
            data["personal_phone"]
        )


class PhoneBook:
    FILE_PATH = "phonebook.txt"  # Тут контакты наши
    PAGE_SIZE = 5  # Сколько буду показывать контактов

    def __init__(self):
        """Загружает контакты из файла при создании справочника."""
        self.contacts: List[Contact] = []
        self.load_contacts()

    def load_contacts(self):
        """Загружает контакты из файла, если он существует."""
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.contacts = [Contact.from_dict(contact) for contact in data]

    def save_contacts(self):
        """Сохраняет контакты в файл."""
        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump([contact.to_dict() for contact in self.contacts], file, ensure_ascii=False, indent=4)

    def add_contact(self, contact: Contact):
        """Добавляет новый контакт и сохраняет изменения."""
        self.contacts.append(contact)
        self.save_contacts()

    def edit_contact(self, index: int, updated_contact: Contact):
        """Изменяет контакт по индексу."""
        if 0 <= index < len(self.contacts):
            self.contacts[index] = updated_contact
            self.save_contacts()

    def search_contacts(self, query: Optional[Dict[str, str]]) -> List[Contact]:
        """Ищет контакты по заданным критериям."""
        results = self.contacts
        for key, value in query.items():
            results = [contact for contact in results if getattr(contact, key).lower() == value.lower()]
        return results

    def display_contacts(self, page: int = 1):
        """Выводит контакты на экран постранично."""
        start = (page - 1) * self.PAGE_SIZE
        end = start + self.PAGE_SIZE
        for i, contact in enumerate(self.contacts[start:end], start=start + 1):
            print(f"{i}. {contact.surname} {contact.name} {contact.patronymic}, {contact.organization}, "
                  f"Раб. тел: {contact.work_phone}, Лич. тел: {contact.personal_phone}")


# Основная функция для работы со справочником
def main():
    phonebook = PhoneBook()

    while True:
        print("\n1. Показать контакты\n2. Добавить контакт\n3. Редактировать контакт\n4. Поиск контакта\n5. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            page = int(input("Введите номер страницы: "))
            phonebook.display_contacts(page)

        elif choice == "2":
            surname = input("Фамилия: ")
            name = input("Имя: ")
            patronymic = input("Отчество: ")
            organization = input("Организация: ")
            work_phone = input("Рабочий телефон: ")
            personal_phone = input("Личный телефон: ")
            new_contact = Contact(surname, name, patronymic, organization, work_phone, personal_phone)
            phonebook.add_contact(new_contact)
            print("Контакт добавлен.")

        elif choice == "3":
            index = int(input("Введите номер контакта для редактирования: ")) - 1
            surname = input("Фамилия: ")
            name = input("Имя: ")
            patronymic = input("Отчество: ")
            organization = input("Организация: ")
            work_phone = input("Рабочий телефон: ")
            personal_phone = input("Личный телефон: ")
            updated_contact = Contact(surname, name, patronymic, organization, work_phone, personal_phone)
            phonebook.edit_contact(index, updated_contact)
            print("Контакт обновлен.")

        elif choice == "4":
            query = {}
            if input("Искать по фамилии? (y/n): ") == "y":
                query["surname"] = input("Фамилия: ")
            if input("Искать по имени? (y/n): ") == "y":
                query["name"] = input("Имя: ")
            if input("Искать по отчеству? (y/n): ") == "y":
                query["patronymic"] = input("Отчество: ")
            if input("Искать по организации? (y/n): ") == "y":
                query["organization"] = input("Организация: ")
            if input("Искать по рабочему телефону? (y/n): ") == "y":
                query["work_phone"] = input("Рабочий телефон: ")
            if input("Искать по личному телефону? (y/n): ") == "y":
                query["personal_phone"] = input("Личный телефон: ")

            results = phonebook.search_contacts(query)
            if results:
                for contact in results:
                    print(f"{contact.surname} {contact.name} {contact.patronymic}, {contact.organization}, "
                          f"Раб. тел: {contact.work_phone}, Лич. тел: {contact.personal_phone}")
            else:
                print("Контакты не найдены.")

        else:
            print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()


"""

Я хз что тут описывать, нафиг типизация я тоже хз, крч хз что делать, но вроде оно работает

"""