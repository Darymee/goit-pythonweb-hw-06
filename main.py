from __future__ import annotations

import argparse
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CRUD CLI для роботи з базою даних")
    parser.add_argument("-a", "--action", required=True, choices=["create", "list", "update", "remove"])
    parser.add_argument("-m", "--model", required=True, choices=MODEL_MAP.keys())
    parser.add_argument("--id", type=int, help="ID запису")
    parser.add_argument("-n", "--name", help="Назва або ім'я")
    parser.add_argument("--group_id", type=int, help="ID групи")
    parser.add_argument("--teacher_id", type=int, help="ID викладача")
    parser.add_argument("--student_id", type=int, help="ID студента")
    parser.add_argument("--subject_id", type=int, help="ID предмета")
    parser.add_argument("--grade", type=int, help="Оцінка")
    parser.add_argument("--grade_date", help="Дата оцінки у форматі YYYY-MM-DD")
    return parser.parse_args()


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
    if model_name == "Teacher" and args.name:
        entity.fullname = args.name
    elif model_name == "Group" and args.name:
        entity.name = args.name
    elif model_name == "Student":
        if args.name:
            entity.fullname = args.name
        if args.group_id:
            entity.group_id = args.group_id
    elif model_name == "Subject":
        if args.name:
            entity.name = args.name
        if args.teacher_id:
            entity.teacher_id = args.teacher_id
    elif model_name == "Grade":
        if args.student_id:
            entity.student_id = args.student_id
        if args.subject_id:
            entity.subject_id = args.subject_id
        if args.grade:
            entity.grade = args.grade
        if args.grade_date:
            entity.grade_date = args.grade_date


def main() -> None:
    args = parse_args()
    model = MODEL_MAP[args.model]

    with SessionLocal() as session:
        if args.action == "create":
            entity = create_entity(args.model, args)
            session.add(entity)
            session.commit()
            print(f"Створено: {entity}")

        elif args.action == "list":
            entities = session.query(model).all()
            for item in entities:
                print(item)

        elif args.action == "update":
            entity = session.get(model, args.id)
            if not entity:
                print("Запис не знайдено")
                return
            update_entity(entity, args.model, args)
            session.commit()
            print(f"Оновлено: {entity}")

        elif args.action == "remove":
            entity = session.get(model, args.id)
            if not entity:
                print("Запис не знайдено")
                return
            session.delete(entity)
            session.commit()
            print(f"Видалено: {entity}")


if __name__ == "__main__":
    main()
