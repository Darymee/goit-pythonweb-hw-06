from __future__ import annotations

import argparse
from datetime import datetime
from typing import Any

from database import SessionLocal
from models import Grade, Group, Student, Subject, Teacher

MODEL_MAP = {
    "Teacher": Teacher,
    "Group": Group,
    "Student": Student,
    "Subject": Subject,
    "Grade": Grade,
}


def parse_grade_date(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Дата має бути у форматі YYYY-MM-DD"
        ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CRUD CLI для роботи з базою даних")
    parser.add_argument(
        "-a",
        "--action",
        required=True,
        choices=["create", "list", "update", "remove"],
    )
    parser.add_argument("-m", "--model", required=True, choices=MODEL_MAP.keys())
    parser.add_argument("--id", type=int, help="ID запису")
    parser.add_argument("-n", "--name", help="Назва або ім'я")
    parser.add_argument("--group_id", type=int, help="ID групи")
    parser.add_argument("--teacher_id", type=int, help="ID викладача")
    parser.add_argument("--student_id", type=int, help="ID студента")
    parser.add_argument("--subject_id", type=int, help="ID предмета")
    parser.add_argument("--grade", type=int, help="Оцінка")
    parser.add_argument(
        "--grade_date",
        type=parse_grade_date,
        help="Дата оцінки у форматі YYYY-MM-DD",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    required_by_action_and_model = {
        ("create", "Teacher"): ["name"],
        ("create", "Group"): ["name"],
        ("create", "Student"): ["name", "group_id"],
        ("create", "Subject"): ["name", "teacher_id"],
        ("create", "Grade"): ["student_id", "subject_id", "grade", "grade_date"],
        ("update", "Teacher"): ["id"],
        ("update", "Group"): ["id"],
        ("update", "Student"): ["id"],
        ("update", "Subject"): ["id"],
        ("update", "Grade"): ["id"],
        ("remove", "Teacher"): ["id"],
        ("remove", "Group"): ["id"],
        ("remove", "Student"): ["id"],
        ("remove", "Subject"): ["id"],
        ("remove", "Grade"): ["id"],
    }

    missing = [
        field
        for field in required_by_action_and_model.get((args.action, args.model), [])
        if getattr(args, field) is None
    ]
    if missing:
        fields = ", ".join(missing)
        raise ValueError(f"Для дії '{args.action}' над моделлю '{args.model}' потрібні поля: {fields}")

    if args.model == "Grade" and args.grade is not None and not 0 <= args.grade <= 100:
        raise ValueError("Оцінка має бути в діапазоні від 0 до 100")

    if args.action == "update":
        editable_fields = [
            args.name,
            args.group_id,
            args.teacher_id,
            args.student_id,
            args.subject_id,
            args.grade,
            args.grade_date,
        ]
        if all(value is None for value in editable_fields):
            raise ValueError("Для оновлення потрібно передати хоча б одне поле для зміни")


def create_entity(model_name: str, args: argparse.Namespace) -> Any:
    if model_name == "Teacher":
        return Teacher(fullname=args.name)
    if model_name == "Group":
        return Group(name=args.name)
    if model_name == "Student":
        return Student(fullname=args.name, group_id=args.group_id)
    if model_name == "Subject":
        return Subject(name=args.name, teacher_id=args.teacher_id)
    if model_name == "Grade":
        return Grade(
            student_id=args.student_id,
            subject_id=args.subject_id,
            grade=args.grade,
            grade_date=args.grade_date,
        )
    raise ValueError(f"Невідома модель: {model_name}")


def update_entity(entity: Any, model_name: str, args: argparse.Namespace) -> None:
    if model_name == "Teacher" and args.name is not None:
        entity.fullname = args.name
    elif model_name == "Group" and args.name is not None:
        entity.name = args.name
    elif model_name == "Student":
        if args.name is not None:
            entity.fullname = args.name
        if args.group_id is not None:
            entity.group_id = args.group_id
    elif model_name == "Subject":
        if args.name is not None:
            entity.name = args.name
        if args.teacher_id is not None:
            entity.teacher_id = args.teacher_id
    elif model_name == "Grade":
        if args.student_id is not None:
            entity.student_id = args.student_id
        if args.subject_id is not None:
            entity.subject_id = args.subject_id
        if args.grade is not None:
            entity.grade = args.grade
        if args.grade_date is not None:
            entity.grade_date = args.grade_date


def main() -> None:
    try:
        args = parse_args()
        validate_args(args)
        model = MODEL_MAP[args.model]

        with SessionLocal() as session:
            if args.action == "create":
                entity = create_entity(args.model, args)
                session.add(entity)
                session.commit()
                session.refresh(entity)
                print(f"Створено: {entity}")

            elif args.action == "list":
                entities = session.query(model).all()
                if not entities:
                    print("Записи відсутні")
                    return
                for item in entities:
                    print(item)

            elif args.action == "update":
                entity = session.get(model, args.id)
                if not entity:
                    print("Запис не знайдено")
                    return
                update_entity(entity, args.model, args)
                session.commit()
                session.refresh(entity)
                print(f"Оновлено: {entity}")

            elif args.action == "remove":
                entity = session.get(model, args.id)
                if not entity:
                    print("Запис не знайдено")
                    return
                session.delete(entity)
                session.commit()
                print(f"Видалено: {entity}")
    except ValueError as exc:
        print(f"Помилка: {exc}")


if __name__ == "__main__":
    main()
