import sqlite3
import logging

from conf.db import session, engine
from conf.models import Student, Group, Lecturer, Subject, Grade, Base
from my_select import select_1, select_2, select_3, select_4, select_5, select_6, select_7, select_8, select_9, \
    select_10, select_11, select_12

from seed import DataGenerator


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    'line_num: %(lineno)s > %(message)s'
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class DatabaseManager :
    def drop_tables(self) :
        Base.metadata.drop_all(engine)

    def delete_all_db(self) :
        session.query(Student).delete()
        session.query(Group).delete()
        session.query(Lecturer).delete()
        session.query(Subject).delete()
        session.query(Grade).delete()
        session.commit()
        session.close()

    def create_table(self, table) :
        table.metadata.create_all(engine)

    def insert_data(self, data) :
        session.bulk_save_objects(data)
        session.commit()

    def select_table(self, table, **kwargs) :
        result = session.query(table).filter_by(**kwargs).all()
        session.close()
        return result

    def close_connection(self) :
        engine.dispose()


def main() :
    db_manager = DatabaseManager()

    tables = [Student, Group, Lecturer, Subject, Grade]
    try :
        # видалення всіх баз
        logging.debug("Видалення таблиць")
        db_manager.drop_tables()
        # Створення таблиць
        for table_class in tables :
            logging.debug(f"Створення таблиць {table_class.__name__}")
            db_manager.create_table(table_class)
        #
        # Наповнення таблиць
        generator = DataGenerator()
        students_data = generator.generate_students(50)
        session.add_all(students_data)
        groups_data = generator.generate_groups(3)
        session.add_all(groups_data)
        lecturers_data = generator.generate_lecturers(5)
        session.add_all(lecturers_data)
        subjects_data = generator.generate_subjects(8)
        session.add_all(subjects_data)
        grades_data = generator.generate_grades(len(students_data), len(subjects_data))
        session.add_all(grades_data)

        session.commit()

        # Топ 5 студентов с наивысшим средним баллом
        select_1()
        # 2. Найкращий учень з предмета
        select_2()
        # 3. Пошук середнього балу по всім группам
        select_3()
        # 4. Пошук середній бал на потоці (по всій таблиці оцінок)
        select_4()
        # 5. Пошук які курси читає певний викладач.
        select_5()
        # 6 Пошук списку студентів у певній групі.
        select_6()
        # 7. Пошук оцінки студентів у окремій групі з певного предмета.
        select_7()
        # 8. Пошук середній бал, який ставить певний викладач зі своїх предметів.
        select_8()
        # 9. Пошук список курсів, які відвідує студент.
        select_9()
        # 10. Пошук курсів, які певному студенту читає певний викладач.
        select_10()
        # Додатково
        # 1. Середній бал, який певний викладач ставить певному студентові.
        select_11()
        # 2. Оцінки студентів у певній групі з певного предмета на останньому занятті.
        select_12()

    except sqlite3.Error as e :
        logging.error(f"Error {e}")
    finally :
        db_manager.close_connection()
        session.close()


if __name__ == "__main__" :
    main()
