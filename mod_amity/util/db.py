
from __future__ import print_function, unicode_literals
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy import Unicode
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import ChoiceType


Base = declarative_base()


class RoomDB(Base):
    __tablename__ = 'rooms'

    TYPES = [("living_space", "Living Space"),
             ("office", "Office")]

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True)
    type = Column(ChoiceType(TYPES))

    def __init__(self, name, room_type):
        self.name = name
        self.type = room_type


class FellowDB(Base):
    __tablename__ = 'fellows'
    id = Column(Integer, primary_key=True)
    fellow_id = Column(String, unique=True)
    fellow_name = Column(String)
    fellow_office = Column(String)
    fellow_living_space = Column(String)

    def __init__(self, fellow_id, name, office, living_space):
        self.fellow_id = fellow_id
        self.fellow_name = name
        self.fellow_office = office
        self.fellow_living_space = living_space


class StaffDB(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    staff_id = Column(String, unique=True)
    staff_name = Column(String)
    staff_office = Column(String)

    def __init__(self, staff_id, name, office):
        self.staff_id = staff_id
        self.staff_name = name
        self.staff_office = office


class DbUtil(object):
    def __init__(self, db_path):

        engine = create_engine('sqlite:///{}'.format(db_path), convert_unicode=True)
        Base.metadata.create_all(engine)
        self.db = Session(bind=engine)

    def save_to_db(self, rooms, people):
        """
        write staff, fellows, staff to database
        """
        for room in rooms:
            self.db.add(RoomDB(room.name, room.type), _warn=False)

        for fellow in people['fellows']:
            self.db.add(
                FellowDB(fellow_id=fellow.id, name=fellow.name, office=fellow.office, living_space=fellow.living_space),
                _warn=False
            )

        for staff in people['staff']:
            self.db.add(StaffDB(staff_id=staff.id, name=staff.name, office=staff.office), _warn=False)

        self.db.commit()

    def load_state(self, db_path):
        """
        loads the state of db to amity
        :param db_path:
        :return:
        """

        rooms = RoomDB.all()

        print (rooms)
