from sqlalchemy import Column, ForeignKey, Integer, String, Date, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    id_groups = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    students = relationship('Student')


class Lecturer(Base):
    __tablename__ = 'lecturers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    id_groups = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    subjects = relationship('Subject')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(170), nullable=False)
    id_lecturer = Column(Integer, ForeignKey('lecturers.id', ondelete='CASCADE'))
    grades = relationship('Grade')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, CheckConstraint('grade >= 1 AND grade <= 12'))
    grade_date = Column(Date, nullable=False)
    id_students = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    id_subjects = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'))

