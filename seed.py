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
MIN_STUDENTS = 30
MAX_STUDENTS = 50
MIN_TEACHERS = 3
MAX_TEACHERS = 5
MIN_SUBJECTS = 5
MAX_SUBJECTS = 8
MIN_GRADES_PER_STUDENT = 10
MAX_GRADES_PER_STUDENT = 20
MIN_GRADE = 60
MAX_GRADE = 100


def random_date(start_days_ago: int = 180, end_days_ago: int = 1):
    start_date = datetime.now() - timedelta(days=start_days_ago)
    end_date = datetime.now() - timedelta(days=end_days_ago)
    delta_days = (end_date - start_date).days
    return (start_date + timedelta(days=random.randint(0, max(delta_days, 1)))).date()


def seed_database() -> None:
    with SessionLocal() as session:
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

            teachers = [Teacher(fullname=fake.name()) for _ in range(random.randint(MIN_TEACHERS, MAX_TEACHERS))]
            session.add_all(teachers)
            session.commit()

            subject_count = random.randint(MIN_SUBJECTS, MAX_SUBJECTS)
            chosen_subjects = random.sample(SUBJECT_NAMES, subject_count)
            subjects = [
                Subject(name=name, teacher_id=random.choice(teachers).id)
                for name in chosen_subjects
            ]
            session.add_all(subjects)
            session.commit()

            students = [
                Student(fullname=fake.name(), group_id=random.choice(groups).id)
                for _ in range(random.randint(MIN_STUDENTS, MAX_STUDENTS))
            ]
            session.add_all(students)
            session.commit()

            grades: list[Grade] = []
            for student in students:
                # Гарантуємо хоча б по одній оцінці з кожного предмета.
                for subject in subjects:
                    grades.append(
                        Grade(
                            student_id=student.id,
                            subject_id=subject.id,
                            grade=random.randint(MIN_GRADE, MAX_GRADE),
                            grade_date=random_date(),
                        )
                    )

                extra_grades_count = random.randint(
                    max(MIN_GRADES_PER_STUDENT - len(subjects), 0),
                    max(MAX_GRADES_PER_STUDENT - len(subjects), 0),
                )
                for _ in range(extra_grades_count):
                    subject = random.choice(subjects)
                    grades.append(
                        Grade(
                            student_id=student.id,
                            subject_id=subject.id,
                            grade=random.randint(MIN_GRADE, MAX_GRADE),
                            grade_date=random_date(),
                        )
                    )

            session.add_all(grades)
            session.commit()
            print("Базу даних успішно заповнено тестовими даними.")
            print(
                f"Груп: {len(groups)}, викладачів: {len(teachers)}, предметів: {len(subjects)}, "
                f"студентів: {len(students)}, оцінок: {len(grades)}"
            )
        except Exception as exc:
            session.rollback()
            print(f"Помилка при seed: {exc}")
            raise


if __name__ == "__main__":
    seed_database()
