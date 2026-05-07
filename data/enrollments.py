import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Enrollment(SqlAlchemyBase):
    __tablename__ = 'enrollments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    club_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('clubs.id'))
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user = orm.relationship('User', back_populates='enrollments')
    club = orm.relationship('Club', back_populates='enrollments')

