from __future__ import print_function, unicode_literals

from sqlalchemy import Column, String, Integer
from sqlalchemy import Unicode
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import ChoiceType

from mod_amity.models import Constants, LivingSpace, Office

Base = declarative_base()


class RoomDB(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    type = Column(String)

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

    def load_state(self):
        """
        loads the state of db to amity
        :return:
        """
        rooms = dict(offices=[], living_space=[])
        fellows = []

        rooms_db = self.db.query(RoomDB.name, RoomDB.type).all()

        for room in rooms_db:
            if room.type == Constants.LIVING_SPACE:
                rooms['living_space'].append(LivingSpace(room.name))
            elif room.type == Constants.OFFICE:
                rooms['offices'].append(Office(room.name))

