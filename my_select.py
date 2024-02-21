import random

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from conf.db import session
from conf.models import Student, Group, Lecturer, Subject, Grade, Base


# Топ 5 студентов с наивысшим средним баллом
def select_1() :
    top_students = session.query(Student.id, Student.fullname,
                                 func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .join(Grade, Student.id == Grade.id_students) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.grade).desc()) \
        .limit(5) \
        .all()

    print("Топ-5 студентов с наивысшим средним баллом:")
    for student in top_students :
        print(f"ID: {student.id}, Студент: {student.fullname}, Средний балл: {student.average_grade}")


# Пошук назви предмета
def get_subject_name_by_id(subject_id) :
    subject = session.query(Subject).filter(Subject.id == subject_id).first()
    if subject :
        return subject.name
    else :
        return "Предмет не знайдено"


# 2. Найкращий учень з предмета
def select_2() :
    subject_id = random.randint(1, 8)  # генеруємо випадковий предмет
    subject_name = get_subject_name_by_id(subject_id)
    if subject_name :
        top_student_subject = session.query(Student.id, Student.fullname,
                                            func.round(func.avg(Grade.grade), 2).label('average_grade')) \
            .join(Grade, Student.id == Grade.id_students) \
            .filter(Grade.id_subjects == subject_id) \
            .group_by(Student.id) \
            .order_by(func.avg(Grade.grade).desc()) \
            .limit(1) \
            .first()
        if top_student_subject :
            print(f"Найкращий учень з предмета: {subject_name}:")
            print(
                f"ID: {top_student_subject[0]}, Студент: {top_student_subject[1]}, Середня оцінка: {top_student_subject[2]}")
        else :
            print(f"Не знайдено жодного студента з предмета: {subject_name} (ID: {subject_id})")
    else :
        print(f"Предмет з ID: {subject_id} не знайдено")


# 3. Пошук середнього балу по всім группам
def select_3() :
    subject_id = random.randint(1, 8)  # генеруємо випадковий предмет
    subject_name = get_subject_name_by_id(subject_id)
    if subject_name :
        average_grades_by_group = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
            .join(Student, Group.id == Student.id_groups) \
            .join(Grade, Student.id == Grade.id_students) \
            .filter(Grade.id_subjects == subject_id) \
            .group_by(Group.name) \
            .all()
        if average_grades_by_group :
            print(f"Середні бали по групах з предмета: {subject_name}")
            for group_grade in average_grades_by_group :
                print(f"Група: {group_grade[0]}, Середня оцінка: {group_grade[1]}")
    else :
        print(f"Предмет з ID: {subject_id} не знайдено")


# 4. Пошук середній бал на потоці (по всій таблиці оцінок)
def select_4() :
    average_grade_all_subjects = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')).scalar()
    if average_grade_all_subjects is not None :
        print(f"Середній бал з усіх предметів: {average_grade_all_subjects}")
    else :
        print("У базі даних не знайдено оцінок!")


# Пошук викладача
def get_lecturer_name_by_id(lecturer_id) :
    lecturer = session.query(Lecturer).filter(Lecturer.id == lecturer_id).first()
    if lecturer :
        return lecturer.fullname, lecturer.id_groups
    else :
        return "Викладача не знайдено"


# 5. Пошук які курси читає певний викладач.
def select_5() :
    lecturer_id = random.randint(1, 5)
    lecturer_name = get_lecturer_name_by_id(lecturer_id)
    if lecturer_name :
        lecturer = session.query(Subject.name).join(Lecturer).where(Lecturer.id == lecturer_id)
        courses_by_lecturer = [subject[0] for subject in lecturer]

        if courses_by_lecturer :
            print(f"Курси читає викладач: {lecturer_name}")
            for course in courses_by_lecturer :
                print(f"Курс: {course}")
        else :
            print(f"Не знайдено курсів для викладача: {lecturer_name}")
    else :
        print(f"Викладача з ID: {lecturer_name} не знайдено")


# Пошук групи
def get_group_name_by_id(group_id) :
    group = session.query(Group).filter_by(id = group_id).first()
    if group :
        return group.name
    else :
        return "Группу не знайдено"


# 6 Пошук списку студентів у певній групі.
def select_6() :
    group_id = random.randint(1, 3)  # Генеруємо випадкову групу
    group_name = get_group_name_by_id(group_id)  # Пошук групи

    students_by_group = session.query(Student).filter_by(id_groups = group_id).all()
    if students_by_group :
        print(f"Студенти в групі: {group_name}")
        for student in students_by_group :
            print(f"ID: {student.id}, Повне ім'я: {student.fullname}")
    else :
        print(f"Не знайдено студентів у групі: {group_name}")


# 7. Пошук оцінки студентів у окремій групі з певного предмета.
def select_7() :
    group_id = random.randint(1, 3)  # Генеруємо випадкову групу
    groups_name = get_group_name_by_id(group_id)  # Пошук групи

    subject_id = random.randint(1, 8)  # генеруємо випадковий предмет
    subject_name = get_subject_name_by_id(subject_id)

    grades_by_group_and_subject = session.query(Student.fullname, Grade.grade). \
        join(Grade, Student.id == Grade.id_students). \
        join(Group, Student.id_groups == Group.id). \
        filter(Group.id == group_id, Grade.id_subjects == subject_id). \
        order_by(Student.fullname, Grade.grade)

    if grades_by_group_and_subject :
        print(f"Оцінки за групу: {groups_name}, та предмет: {subject_name}.")
        for grade in grades_by_group_and_subject :
            print(f"Студент: {grade[0]}, Оцінка: {grade[1]}")
    else :
        print(f"Не знайдено оцінок для групи: {group_id}, та предмета: {subject_id}")


# 8. Пошук середній бал, який ставить певний викладач зі своїх предметів.
def select_8() :
    lecturer_id = random.randint(1, 5)  # генеруємо випадкового викладача
    lector_name = get_lecturer_name_by_id(lecturer_id)

    average_grade_by_lecturer = session.query(Subject.name,
                                              func.round(func.avg(Grade.grade), 2).label('average_grade')). \
        join(Lecturer).join(Grade). \
        filter(Lecturer.id == lecturer_id). \
        group_by(Subject.name).all()

    if average_grade_by_lecturer :
        print(f"Середні бали по викладачу: {lector_name}.")
        for subject in average_grade_by_lecturer :
            print(f"Предмет: {subject[0]}, Середня оцінка: {subject[1]}")
    else :
        print(f"Не знайдено оцінок для викладача: {lector_name}.")


# Пошук студента
def get_students_name_by_id(student_id) :
    # Query to get the full name of the student by their ID
    student = session.query(Student).filter(Student.id == student_id).first()
    if student :
        return student.fullname
    else :
        return "Студента не знайдено"


# 9. Пошук список курсів, які відвідує студент.
def select_9() :
    student_id = random.randint(1, 50)  # генеруємо випадкового студента
    lector_name = get_students_name_by_id(student_id)

    courses_by_student = session.query(Subject.name). \
        join(Grade, Grade.id_subjects == Subject.id). \
        join(Student, Student.id == Grade.id_students). \
        filter(Student.id == student_id).distinct().all()

    if courses_by_student :
        print(f"Предмети, відвідані студентом: {lector_name}.")
        for course in courses_by_student :
            print(f" Предмет: {course[0]}")
    else :
        print(f"Не знайдено предмета для студента with ID {student_id}")


# Пошук студента
def get_students_name_by_id(lecturer_group_id) :
    # Знаходимо випадкового студента з огляду на прив'язку до викладача через групу
    student = session.query(Student.id). \
        join(Group, Student.id_groups == Group.id). \
        join(Lecturer, Group.id == Lecturer.id_groups). \
        filter(Lecturer.id == lecturer_group_id). \
        order_by(func.random()). \
        limit(1). \
        scalar()

    return student


# 10. Пошук курсів, які певному студенту читає певний викладач.
def select_10() :
    lecturer_id = random.randint(1, 5)  # генеруємо випадкового викладача
    lector_name, lecturer_group_id = get_lecturer_name_by_id(lecturer_id)

    student = get_students_name_by_id(lecturer_group_id)

    if student :
        # Знаходимо предмети, які читає викладач для знайденого студента
        courses_by_lecturer_for_student = session.query(Student.id, Student.fullname, Subject.name). \
            join(Grade, Grade.id_students == Student.id). \
            join(Subject, Subject.id == Grade.id_subjects). \
            join(Lecturer, Subject.id_lecturer == Lecturer.id). \
            filter(Lecturer.id == lecturer_id, Student.id == student). \
            distinct(). \
            all()

        if student and courses_by_lecturer_for_student :
            print(f"Предмети відвідав студент: {courses_by_lecturer_for_student[0][1]}, викладача: {lector_name}.")
            for course in courses_by_lecturer_for_student :
                print(f"Предмет: {course.name}")
        else :
            print(f"Не знайдено курсів для студентів викладача: {lector_name}.")


# Додатково
# 1. Середній бал, який певний викладач ставить певному студентові.
def select_11() :
    lecturer_id = random.randint(1, 5)  # генеруємо випадкового викладача
    lector_name, lecturer_group_id = get_lecturer_name_by_id(lecturer_id)

    student_id = get_students_name_by_id(lecturer_group_id)

    courses_by_lecturer_for_student = (session.query(Student.id, Student.fullname, Subject.name,
                                                     func.round(func.avg(Grade.grade), 2).label("average_grade"))
                                       .join(Grade, Grade.id_students == Student.id)
                                       .join(Subject, Grade.id_subjects == Subject.id)
                                       .join(Lecturer, Subject.id_lecturer == Lecturer.id)
                                       .filter(Lecturer.id == lecturer_group_id,
                                               Student.id == student_id).distinct().all())

    if courses_by_lecturer_for_student :
        print(
            f"Середня оцінка студента: {student_id} {courses_by_lecturer_for_student[0][1]}, викладача: {lector_name}.")
        print(f"Середня оцінка: {courses_by_lecturer_for_student[0][3]}")
    else :
        print(f"Не знайдено курсів для студентів викладача: {lector_name}.")


# 2. Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12() :
    subject_id = random.randint(1, 8)  # генеруємо випадковий предмет
    subject_name = get_subject_name_by_id(subject_id)

    last_grades_for_subject = (session.query(Student.id, Student.fullname, Subject.name,
                                             Grade.grade, Grade.grade_date)
                               .join(Grade, Student.id == Grade.id_students)
                               .join(Subject, Grade.id_subjects == Subject.id)
                               .filter(Subject.id == subject_id)
                               .group_by(Student.id).having(Grade.grade_date == func.max(Grade.grade_date)).all())

    print(f"Останні оцінки з предмета: {subject_name}.")
    for grade in last_grades_for_subject :
        print(f"ID: {grade[0]}, Студент: {grade[1]}, Оцінка: {grade[3]}, Дата: {grade[4]}")


if __name__ == "__main__" :
    pass
    # # Топ 5 студентов с наивысшим средним баллом
    # select_1()
    # # 2. Найкращий учень з предмета
    # select_2()
    # # 3. Пошук середнього балу по всім группам
    # select_3()
    # # 4. Пошук середній бал на потоці (по всій таблиці оцінок)
    # select_4()
    # # 5. Пошук які курси читає певний викладач.
    # select_5()
    # # 6 Пошук списку студентів у певній групі.
    # select_6()
    # # 7. Пошук оцінки студентів у окремій групі з певного предмета.
    # select_7()
    # # 8. Пошук середній бал, який ставить певний викладач зі своїх предметів.
    # select_8()
    # # 9. Пошук список курсів, які відвідує студент.
    # select_9()
    # # 10. Пошук курсів, які певному студенту читає певний викладач.
    # select_10()
    # Додатково
    # # 1. Середній бал, який певний викладач ставить певному студентові.
    # select_11()
    # # 2. Оцінки студентів у певній групі з певного предмета на останньому занятті.
    # select_12()
