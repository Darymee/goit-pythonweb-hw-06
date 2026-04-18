from __future__ import annotations

from sqlalchemy import desc, func, select

from database import SessionLocal
from models import Grade, Group, Student, Subject, Teacher


def select_1():
    """5 студентів із найбільшим середнім балом з усіх предметів."""
    stmt = (
        select(Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Grade, Grade.student_id == Student.id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    with SessionLocal() as session:
        return session.execute(stmt).all()


def select_2(subject_id: int):
    """Студент із найвищим середнім балом з певного предмета."""
    stmt = (
        select(Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Grade, Grade.student_id == Student.id)
        .where(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    with SessionLocal() as session:
        return session.execute(stmt).first()


def select_3(subject_id: int):
    """Середній бал у групах з певного предмета."""
    stmt = (
        select(Group.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .select_from(Group)
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .where(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .order_by(Group.name)
    )
    with SessionLocal() as session:
        return session.execute(stmt).all()


def select_4():
    """Середній бал на потоці (по всій таблиці оцінок)."""
    stmt = select(func.round(func.avg(Grade.grade), 2))
    with SessionLocal() as session:
        return session.execute(stmt).scalar()


def select_5(teacher_id: int):
    """Які курси читає певний викладач."""
    stmt = select(Subject.name).where(Subject.teacher_id == teacher_id).order_by(Subject.name)
    with SessionLocal() as session:
        return session.execute(stmt).all()


def select_6(group_id: int):
    """Список студентів у певній групі."""
    stmt = select(Student.fullname).where(Student.group_id == group_id).order_by(Student.fullname)
    with SessionLocal() as session:
        return session.execute(stmt).all()


def select_7(group_id: int, subject_id: int):
    """Оцінки студентів у окремій групі з певного предмета."""
    stmt = (
        select(Student.fullname, Grade.grade, Grade.grade_date)
        .join(Grade, Grade.student_id == Student.id)
        .where(Student.group_id == group_id, Grade.subject_id == subject_id)
        .order_by(Student.fullname, Grade.grade_date)
    )
    with SessionLocal() as session:
        return session.execute(stmt).all()


def select_8(teacher_id: int):
    """Середній бал, який ставить певний викладач зі своїх предметів."""
    stmt = (
        select(Teacher.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Subject, Subject.teacher_id == Teacher.id)
        .join(Grade, Grade.subject_id == Subject.id)
        .where(Teacher.id == teacher_id)
        .group_by(Teacher.id)
    )
    with SessionLocal() as session:
        return session.execute(stmt).first()


def select_9(student_id: int):
    """Список курсів, які відвідує певний студент."""
    stmt = (
        select(Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .where(Grade.student_id == student_id)
        .distinct()
        .order_by(Subject.name)
    )
    with SessionLocal() as session:
        return session.execute(stmt).all()


def select_10(student_id: int, teacher_id: int):
    """Список курсів, які певному студенту читає певний викладач."""
    stmt = (
        select(Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .order_by(Subject.name)
    )
    with SessionLocal() as session:
        return session.execute(stmt).all()


# Додаткові запити

def select_11(student_id: int, teacher_id: int):
    """Середній бал, який певний викладач ставить певному студентові."""
    stmt = (
        select(func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Subject, Subject.id == Grade.subject_id)
        .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
    )
    with SessionLocal() as session:
        return session.execute(stmt).scalar()


def select_12(group_id: int, subject_id: int):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    subquery = (
        select(func.max(Grade.grade_date))
        .join(Student, Student.id == Grade.student_id)
        .where(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar_subquery()
    )

    stmt = (
        select(Student.fullname, Grade.grade, Grade.grade_date)
        .join(Grade, Grade.student_id == Student.id)
        .where(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.grade_date == subquery,
        )
        .order_by(Student.fullname)
    )
    with SessionLocal() as session:
        return session.execute(stmt).all()


if __name__ == "__main__":
    print("select_1:", select_1())
    print("select_2(subject_id=1):", select_2(1))
    print("select_3(subject_id=1):", select_3(1))
    print("select_4:", select_4())
    print("select_5(teacher_id=1):", select_5(1))
    print("select_6(group_id=1):", select_6(1))
    print("select_7(group_id=1, subject_id=1):", select_7(1, 1))
    print("select_8(teacher_id=1):", select_8(1))
    print("select_9(student_id=1):", select_9(1))
    print("select_10(student_id=1, teacher_id=1):", select_10(1, 1))
