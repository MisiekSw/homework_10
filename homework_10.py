from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = Phone(new_phone)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search_records(self, criteria):
        result = []
        for record in self.values():
            match = all(
                getattr(record, field, None) and getattr(record, field).value == value
                for field, value in criteria.items()
            )
            if match:
                result.append(record)
        return result


class AssistantBot:
    def __init__(self):
        self.contacts = {}

    def input_error(func):
        def errors(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError:
                return "Wprowadź nazwę użytkownika."
            except ValueError:
                return "Podaj nazwę i telefon."
            except IndexError:
                return "Nie znaleziono kontaktu o podanej nazwie."

        return errors

    @input_error
    def handle_hello(self):
        return "How can I help you?"

    @input_error
    def handle_add(self, data):
        name, phone = data.split()
        self.contacts[name] = phone
        return f"Kontakt {name} dodany z numerem telefonu {phone}."

    @input_error
    def handle_change(self, data):
        name, phone = data.split()
        if name in self.contacts:
            self.contacts[name] = phone
            return f"Zmieniono numer telefonu dla kontaktu {name} na {phone}."
        else:
            raise IndexError

    @input_error
    def handle_phone(self, name):
        if name in self.contacts:
            return f"Numer telefonu dla kontaktu {name}: {self.contacts[name]}."
        else:
            raise IndexError

    @input_error
    def handle_show_all(self):
        if not self.contacts:
            return "Brak zapisanych kontaktów."
        return "\n".join([f"{name}: {phone}" for name, phone in self.contacts.items()])

    def main(self):
        while True:
            user_input = input("Wprowadź polecenie: ").lower()

            if user_input in ["good bye", "close", "exit"]:
                print("Good bye!")
                break
            elif user_input == "hello":
                print(self.handle_hello())
            elif user_input.startswith("add"):
                print(self.handle_add(user_input[4:]))
            elif user_input.startswith("change"):
                print(self.handle_change(user_input[7:]))
            elif user_input.startswith("phone"):
                print(self.handle_phone(user_input[6:]))
            elif user_input == "show all":
                print(self.handle_show_all())
            else:
                print("Nieznane polecenie. Spróbuj ponownie.")


if __name__ == "__main__":
    bot = AssistantBot()
    bot.main()
