from sqlalchemy import Column, ForeignKey, Integer, String, Table, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


quiz_answer = Table(
    "quiz_answer",
    Base.metadata,
    Column("quiz_id", Integer, ForeignKey("quiz.id")),
    Column("answer_id", Integer, ForeignKey("answer.id")),
)


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)

    quiz_category: Mapped[list["Quiz"] | None] = relationship(back_populates="category")


class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    value: Mapped[int] = mapped_column(Integer, unique=True)


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)

    quiz_question: Mapped[list["Quiz"] | None] = relationship(back_populates="question")


class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))

    category: Mapped["Category"] = relationship(
        back_populates="quiz_category", lazy="selectin"
    )
    answer: Mapped[list[Answer]] = relationship(secondary=quiz_answer, lazy="selectin")
    question: Mapped["Question"] = relationship(
        back_populates="quiz_question", lazy="selectin"
    )


class Result(Base):
    __tablename__ = "result"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    age: Mapped[int] = mapped_column(Integer)
    sex: Mapped[str] = mapped_column(String)
    quiz: Mapped[str] = mapped_column(String)
