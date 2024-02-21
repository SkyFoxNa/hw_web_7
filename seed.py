from faker import Faker
import random
from conf.models import Student, Group, Lecturer, Subject, Grade
from conf.db import session


students = []
groups = []
lecturers = []
subjects = []
grades = []


class DataGenerator:
    def __init__(self):
        self.fake = Faker('uk_UA')

    # Таблиця студентів
    def generate_students(self, count):

        for _ in range(count):
            student = Student(fullname=self.fake.name(), id_groups=random.randint(1, 3))
            students.append(student)
        return students

    # Таблиця груп
    def generate_groups(self, count):

        for i in range(count):
            group = Group(name=f"Group {i+1}")
            groups.append(group)
        return groups

    # Таблиця викладачів
    def generate_lecturers(self, count):

        for _ in range(count):
            lecturer = Lecturer(fullname=self.fake.name(), id_groups=random.randint(1, 3))
            lecturers.append(lecturer)
        return lecturers

    # Таблиця предметів
    def generate_subjects(self, count):

        for _ in range(count):
            subject = Subject(name=self.fake.catch_phrase(), id_lecturer=random.randint(1, 5))
            subjects.append(subject)
        return subjects

    # Таблиця оцінок
    def generate_grades(self, students_count, subjects_count):

        for student_id in range(1, students_count + 1):
            # for subject_id in random.sample(subjects.id, random.randint(1, 8)): # Випадковий предмет від 1 до 8
            subject_id_all = random.sample([1, 2, 3, 4, 5, 6, 7, 8], random.randint(1, 8)) # Випадковий предмет від 1 до 8
            # subject_ids_all = [subject_1.id for subject_1 in subject_id_all]
            # print(f"{subject_ids_all}")
            for subject_id in subject_id_all:
                for _ in range(20):  # Генеруємо 20 оцінок для кожного студента з кожного предмету
                    grade = random.randint(1, 12)  # Випадкова оцінка від 1 до 12
                    grade_date = self.fake.date_of_birth(minimum_age=1, maximum_age=6)  # Випадкова дата в межах 1-6 років
                    grade = Grade(grade=grade, grade_date=grade_date, id_students=student_id, id_subjects=subject_id)
                    grades.append(grade)
        return grades


if __name__ == "__main__":
    generator = DataGenerator()
    students_data = generator.generate_students(50)
    groups_data = generator.generate_groups(3)
    lecturers_data = generator.generate_lecturers(5)
    subjects_data = generator.generate_subjects(8)
    grades_data = generator.generate_grades(len(students_data), len(subjects_data))

    session.add_all(students_data)
    session.add_all(groups_data)
    session.add_all(lecturers_data)
    session.add_all(subjects_data)
    session.add_all(grades_data)

    session.commit()
    session.close()