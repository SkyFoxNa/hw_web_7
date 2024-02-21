from conf.db import session
from conf.models import Lecturer, Group


def list_lecturers():
    lecturers = session.query(Lecturer).all()
    return lecturers


def create_lecturers(fullname):
    lecturer = Lecturer(fullname=fullname)
    session.add(lecturer)
    session.commit()
    session.close()


# Lecture
def update_lecturers(id_, fullname):
    lecturer = session.query(Lecturer).filter_by(id=id_).first()
    if lecturer:
        lecturer.fullname = fullname
        session.commit()
    session.close()


def remove_lecturers(id_):
    lecturer = session.query(Lecturer).filter_by(id=id_).first()
    if lecturer:
        session.delete(lecturer)
        session.commit()
        return lecturer
    session.close()


# Group
def list_group():
    groups = session.query(Group).all()
    return groups


def create_group(fullname):
    group = Group(name=fullname)
    session.add(group)
    session.commit()
    session.close()


def update_group(id_, fullname):
    group = session.query(Group).filter_by(id=id_).first()
    if group:
        group.name = fullname
        session.commit()
    session.close()


def remove_group(id_):
    group = session.query(Group).filter_by(id=id_).first()
    if group:
        session.delete(group)
        session.commit()
        return group
    session.close()
