from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .db import Base

problem_tag_association = Table(
    'problem_tag',
    Base.metadata,
    Column('problem_id', Integer, ForeignKey('problems.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Contest(Base):
    __tablename__ = 'contests'

    id = Column(Integer, primary_key=True)
    contest_id = Column(Integer, unique=True)
    problems = relationship('Problem', back_populates='contest')


class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    contest_id = Column(Integer, ForeignKey('contests.contest_id'))
    name = Column(String)
    rating = Column(Integer)
    solved_count = Column(Integer)
    index = Column(String)

    contest = relationship('Contest', back_populates='problems')
    tags = relationship('Tag', secondary=problem_tag_association, back_populates='problems')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    problems = relationship('Problem', secondary=problem_tag_association, back_populates='tags')