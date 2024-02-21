import argparse

from conf.repository import list_lecturers, create_lecturers, update_lecturers, remove_lecturers
from conf.repository import list_group, create_group, update_group, remove_group

# Ініціалізація парсера
parser = argparse.ArgumentParser(description='CRUD operations with database')

# Додавання аргументів для виконання операцій
parser.add_argument('-a', '--action', help = 'Command: create, list, update, remove')
parser.add_argument('-m', '--model')
parser.add_argument('-id', '--id')
parser.add_argument('-n', '--name')

# Парсинг аргументів з командного рядка
args = parser.parse_args()

action = args.action
model = args.model
id_ = args.id
fullname = args.name


def main():
    if args.model == 'Teacher':
        if action == 'create':
            create_lecturers(fullname)
            print(f"Lecturer create: Name: {fullname}")
        elif action == 'list':
            lecturers = list_lecturers()
            for l in lecturers:
                print(f"Lecturer: Id: {l.id}, Name: {l.fullname}")
        elif action == 'update':
            u = update_lecturers(id_, fullname)
            if u:
                print(f"Lecturer update: Id: {u.id}, Name: {u.fullname}")
            else:
                print(f"Lecturer not found: Id: {id_}, Name: {fullname}")
        elif action == 'remove':
            r = remove_lecturers(id_)
            if r:
                print(f"Remove count: {id_}")
            else:
                print(f"Lecturer not found: Id: {id_}")
        else:
            print(f"Not found")

    if args.model == 'Group':
        if action == 'create':
            create_group(fullname)
            print(f"Group create: Name: {fullname}")
        elif action == 'list':
            groups = list_group()
            for l in groups:
                print(f"Group: Id: {l.id}, Name: {l.name}")
        elif action == 'update':
            u = update_group(id_, fullname)
            if u:
                print(f"Group update: Id: {u.id}, Name: {u.fullname}")
            else:
                print(f"Group not found: Id: {id_}, Name: {fullname}")
        elif action == 'remove':
            r = remove_group(id_)
            if r:
                print(f"Remove count: {id_}")
            else:
                print(f"Group not found: Id: {id_}")
        else:
            print(f"Not found")


if __name__ == "__main__" :
    main()
