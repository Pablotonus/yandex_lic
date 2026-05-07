import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Club(SqlAlchemyBase):
    __tablename__ = 'clubs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    schedule = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    teacher = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    classroom = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    enrollments = orm.relationship('Enrollment', back_populates='club')

