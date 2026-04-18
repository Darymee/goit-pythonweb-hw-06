# 📚 Student Database

## 🗄️ Схема БД

```
groups — id, name
teachers — id, fullname
students — id, fullname, group_id → groups
subjects — id, name, teacher_id → teachers
grades — id, student_id → students, subject_id → subjects, grade, date_of
```

## 🔄 Міграції (Alembic)

Застосувати міграції:

```bash
alembic upgrade head
```

Створити нову міграцію:

```bash
alembic revision --autogenerate -m "message"
```

---

## 🌱 Наповнення даними

```bash
python seed.py
```

Створює:

- 3 групи
- 3–5 викладачів
- 5–8 предметів
- 30–50 студентів
- до 20 оцінок на студента

---

## 📊 Запити

Виконати всі запити:

```bash
python my_select.py
```

Доступні функції:

```
select_1 ... select_10
```

---

## 🧪 CLI (CRUD)

### Створити

```bash
python main.py -a create -m Teacher -n "Boris Jonson"
python main.py -a create -m Group -n "AD-101"
python main.py -a create -m Student -n "Jane Doe" --group-id 1
python main.py -a create -m Subject -n "Math" --teacher-id 1
python main.py -a create -m Grade --student-id 1 --subject-id 1 --grade 90 --date 2024-10-01
```

---

### Показати

```bash
python main.py -a list -m Teacher
```

---

### Оновити

```bash
python main.py -a update -m Teacher --id 3 -n "Taras Shevchenko"
```

---

### Видалити

```bash
python main.py -a remove -m Teacher --id 3
```

---

## 📁 Файли проєкту

```
models.py
seed.py
my_select.py
main.py
alembic/
alembic.ini
requirements.txt
README.md
```
