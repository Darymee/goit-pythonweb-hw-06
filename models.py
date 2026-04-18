from __future__ import annotations

from datetime import date
from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    students: Mapped[list[Student]] = relationship("Student", back_populates="group")

    def __repr__(self) -> str:
        return f"Group(id={self.id}, name='{self.name}')"


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))

    group: Mapped[Group] = relationship("Group", back_populates="students")
    grades: Mapped[list[Grade]] = relationship(
        "Grade", back_populates="student", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Student(id={self.id}, fullname='{self.fullname}', group_id={self.group_id})"


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150), nullable=False)

    subjects: Mapped[list[Subject]] = relationship("Subject", back_populates="teacher")

    def __repr__(self) -> str:
        return f"Teacher(id={self.id}, fullname='{self.fullname}')"


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"))

    teacher: Mapped[Teacher] = relationship("Teacher", back_populates="subjects")
    grades: Mapped[list[Grade]] = relationship(
        "Grade", back_populates="subject", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    grade_date: Mapped[date] = mapped_column(Date, nullable=False)

    student: Mapped[Student] = relationship("Student", back_populates="grades")
    subject: Mapped[Subject] = relationship("Subject", back_populates="grades")

    def __repr__(self) -> str:
        return (
            f"Grade(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id}, "
            f"grade={self.grade}, grade_date={self.grade_date})"
        )
