from sqlalchemy import Column, Integer, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    a_price = Column(Float)
    a_url = Column(Text)
    n_price = Column(Float)
    n_url = Column(Text)
    popularity = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(Text, unique=True)
    password = Column(Text)
