from __future__ import annotations

import random
from datetime import datetime, timedelta
from faker import Faker

from database import SessionLocal
from models import Grade, Group, Student, Subject, Teacher

fake = Faker("uk_UA")

GROUP_NAMES = ["AD-101", "BD-102", "CD-103"]
SUBJECT_NAMES = [
    "Математика",
    "Фізика",
    "Хімія",
    "Інформатика",
    "Історія",
    "Біологія",
    "Англійська мова",
    "Філософія",
]


def random_date(start_days_ago: int = 180, end_days_ago: int = 1):
    start_date = datetime.now() - timedelta(days=start_days_ago)
    end_date = datetime.now() - timedelta(days=end_days_ago)
    delta_days = (end_date - start_date).days
    return (start_date + timedelta(days=random.randint(0, max(delta_days, 1)))).date()


def seed_database() -> None:
    session = SessionLocal()
    try:
        session.query(Grade).delete()
        session.query(Student).delete()
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(Group).delete()
        session.commit()

        groups = [Group(name=name) for name in GROUP_NAMES]
        session.add_all(groups)
        session.commit()

        teachers = [Teacher(fullname=fake.name()) for _ in range(random.randint(3, 5))]
        session.add_all(teachers)
        session.commit()

        subject_count = random.randint(5, 8)
        chosen_subjects = random.sample(SUBJECT_NAMES, subject_count)
        subjects = [
            Subject(name=name, teacher_id=random.choice(teachers).id)
            for name in chosen_subjects
        ]
        session.add_all(subjects)
        session.commit()

        students = [
            Student(fullname=fake.name(), group_id=random.choice(groups).id)
            for _ in range(random.randint(30, 50))
        ]
        session.add_all(students)
        session.commit()

        grades: list[Grade] = []
        for student in students:
            grade_count = random.randint(10, 20)
            for _ in range(grade_count):
                subject = random.choice(subjects)
                grades.append(
                    Grade(
                        student_id=student.id,
                        subject_id=subject.id,
                        grade=random.randint(60, 100),
                        grade_date=random_date(),
                    )
                )

        session.add_all(grades)
        session.commit()
        print("Базу даних успішно заповнено тестовими даними.")
    except Exception as exc:
        session.rollback()
        print(f"Помилка при seed: {exc}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
