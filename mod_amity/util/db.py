from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import ChoiceType

Base = declarative_base()


class RoomDB(Base):
    __tablename__ = 'rooms'

    TYPES = [("living space", "Living Space"),
             ("office", "Office")]

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(ChoiceType(TYPES))


class FellowDB(Base):
    __tablename__ = 'fellows'
    id = Column(Integer, primary_key=True)
    fellow_id = Column(String)
    fellow_name = Column(String)
    fellow_office = Column(String)
    fellow_living_space = Column(String)


class StaffDB(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    staff_id = Column(String)
    staff_name = String(String)
    staff_office = String(String)


engine = create_engine('sqlite:///amity.sqlite')

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
