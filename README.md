# 📚 Student Database

Проєкт для домашнього завдання з SQLAlchemy, Alembic, PostgreSQL, Faker та CLI CRUD.

## 🚀 Запуск PostgreSQL у Docker

```bash
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

## ⚙️ Налаштування підключення

За замовчуванням проєкт використовує:

- `DB_USER=postgres`
- `DB_PASSWORD=mysecretpassword`
- `DB_HOST=localhost`
- `DB_PORT=5432`
- `DB_NAME=postgres`

За потреби можна створити `.env` файл:

```env
DB_USER=postgres
DB_PASSWORD=mysecretpassword
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
```

## 🗄️ Схема БД

```text
groups   -> id, name
teachers -> id, fullname
students -> id, fullname, group_id -> groups.id
subjects -> id, name, teacher_id -> teachers.id
grades   -> id, student_id -> students.id, subject_id -> subjects.id, grade, grade_date
```

## 📦 Встановлення залежностей

```bash
pip install -r requirements.txt
```

## 🔄 Міграції Alembic

Застосувати міграції:

```bash
alembic upgrade head
```

Створити нову міграцію:

```bash
alembic revision --autogenerate -m "message"
```

## 🌱 Наповнення даними

```bash
python seed.py
```

Скрипт створює:

- 3 групи
- 3–5 викладачів
- 5–8 предметів
- 30–50 студентів
- 10–20 оцінок у кожного студента
- щонайменше 1 оцінку з кожного предмета для кожного студента

## 📊 Запити

У файлі `my_select.py` реалізовано:

- `select_1 ... select_10` — основне завдання
- `select_11, select_12` — додаткові запити

Для швидкої перевірки:

```bash
python my_select.py
```

## 🧪 CLI CRUD

### Створити

```bash
python main.py -a create -m Teacher -n "Boris Jonson"
python main.py -a create -m Group -n "AD-101"
python main.py -a create -m Student -n "Jane Doe" --group_id 1
python main.py -a create -m Subject -n "Math" --teacher_id 1
python main.py -a create -m Grade --student_id 1 --subject_id 1 --grade 90 --grade_date 2024-10-01
```

### Показати

```bash
python main.py -a list -m Teacher
python main.py -a list -m Student
```

### Оновити

```bash
python main.py -a update -m Teacher --id 3 -n "Taras Shevchenko"
python main.py -a update -m Student --id 7 --group_id 2
python main.py -a update -m Grade --id 12 --grade 95 --grade_date 2024-11-15
```

### Видалити

```bash
python main.py -a remove -m Teacher --id 3
python main.py -a remove -m Grade --id 12
```

## 📁 Структура проєкту

```text
models.py
database.py
seed.py
my_select.py
main.py
alembic/
alembic.ini
requirements.txt
README.md
```
