from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import *

from sqlalchemy.orm import *

from main import *


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=true)
    name = Column(String(40), unique=true)
    password = Column(String(8))


class Role(db.Model):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=true)
    identification1 = Column(String(30))
    identification2 = Column(String(30))
    identification3 = Column(String(30))
    ForeignKey(User.id, User)
