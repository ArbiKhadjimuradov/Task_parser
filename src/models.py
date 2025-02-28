from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .db import Base

"таблица многие-ко-многим"
problem_tags = Table(
    "problem_tags",
    Base.metadata,
    Column("problem_id", Integer, ForeignKey("problems.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contest_id = Column(Integer, ForeignKey("contests.id"))
    contest = relationship("Contest", back_populates="problems")
    rating = Column(Integer, nullable=True)
    tags = relationship("Tag", secondary=problem_tags, back_populates="problems")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    problems = relationship("Problem", secondary=problem_tags, back_populates="tags")


class Contest(Base):
    __tablename__ = "contests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    problems = relationship("Problem", back_populates="contest")