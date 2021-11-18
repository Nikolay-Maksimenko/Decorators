from datetime import datetime
from pathlib import Path

def write_log_decor(path_to_log):
    def write_log(any_function):
        def create_log(*args):
            result = any_function(*args)
            log = f'Date and time:  {datetime.today()}, Name function: {any_function.__name__}, Arguments: {args}, Return value: {result} \n'
            with open(path_to_log, 'a', encoding='utf-8') as write_file:
                write_file.write(log)
        return create_log
    return write_log

path_to_log = Path('/home/nikolay/Документы/Репозиторий/Decorators/log.txt')
documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
      ]
directories = {
        '1': ['2207 876234', '11-2'],
        '2': ['10006'],
        '3': []
      }

# проверка наличия документа с указанным номером в списке
def check_doc_number(doc_number):
    for id_doc, document in enumerate(documents):
        if doc_number == document["number"]:
            return id_doc

# проверка наличия полки с указанным номером в словаре
def check_shelf_number(shelf_num):
    for shelf in directories:
        if shelf_num in shelf:
            return shelf

# вывод имени владельца документа по его номеру
@write_log_decor(path_to_log)
def get_number_name (doc_number):
    for document in documents:
        if document["number"] == doc_number:
            print("Имя владельца: ", document["name"])

# вывод номера полки по номеру документа
@write_log_decor(path_to_log)
def get_number_shelf (doc_number):
    for shelf, documents in directories.items():
        if doc_number in documents:
            print(f"Документ №{doc_number} находится на полке №{shelf}")

# вывод списка документов
@write_log_decor(path_to_log)
def show_all_documents():
    for document in documents:
        print(document["type"], document["number"], document["name"])

# создание нового документа
@write_log_decor(path_to_log)
def create_document(list_of_documents, list_of_shelfs):
    type_doc = input("Введите тип документа: ")
    doc_number = input("Введите номер документа: ")
    name = input("Введите имя: ")
    while  True:
        shelf_number = input("Введите номер полки: ")
        if check_shelf_number(shelf_number) != None:
            break
        else:
            print("Нет полки с таким номером!")
    list_of_documents.append({"type": type_doc, "number": doc_number, "name": name})
    list_of_shelfs[shelf_number].append(doc_number)

# удаление документа по его номеру
@write_log_decor(path_to_log)
def delete_document(doc_number):
    del documents[int(check_doc_number(doc_number))]
    for num_shelf in directories:
        if doc_number in directories[num_shelf]:
            directories[num_shelf].remove(doc_number)

# перемещение документа между полками
@write_log_decor(path_to_log)
def move_document(doc_number, shelf_num):
    for shelf in directories:
        if doc_number in directories[shelf]:
            directories[shelf].remove(doc_number)
    directories[shelf_num].append(doc_number)

# создание новой полки
@write_log_decor(path_to_log)
def add_shelf(shelf_num):
    if check_shelf_number(shelf_num) == None:
        directories[shelf_num] = []
    else:
        print("Полка с таким номером уже существует!")

while True:
    command = input("Введите команду: ")
    if command == 'p':
        number = input("Введите номер документа: ")
        if check_doc_number(number) != None:
            get_number_name(number)
        else:
            print("Нет документа с таким номером!")
    elif command == 's':
        number = input("Введите номер документа: ")
        if check_doc_number(number) != None:
            get_number_shelf(number)
        else:
            print("Нет документа с таким номером!")
    elif command == 'l':
        show_all_documents()
    elif command == 'a':
        create_document(documents, directories)
    elif command == 'd':
        number = input("Введите номер документа: ")
        if check_doc_number(number) != None:
            delete_document(number)
        else:
            print("Нет документа с таким номером!")
    elif command == 'm':
        number = input("Введите номер документа: ")
        if check_doc_number(number) != None:
            shelf_number = input("Введите номер целевой полки: ")
            if check_shelf_number(shelf_number) != None:
                move_document(number, shelf_number)
            else:
                print("Нет полки с таким номером!")
        else:
            print("Нет документа с таким номером!")
    elif command == 'as':
        number = input("Введите номер новой полки: ")
        add_shelf(number)
    elif command == 'q':
        print ("Работа программы завершена!")
        break
    else:
        print("""Неверная команда!
              Список доступных команд: p, s, l, a, d, m, as
        Для выхода нажмите 'q'""")