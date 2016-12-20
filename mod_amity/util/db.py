from __future__ import print_function, unicode_literals

from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import ChoiceType

from mod_amity.models import Constants, LivingSpace, Office, Staff, Fellow

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
    fellow_id = Column(String)
    fellow_name = Column(String)
    fellow_office = Column(String)
    fellow_living_space = Column(String)
    fellow_need_accommodation = Column(String)

    def __init__(self, fellow_id, name, office, living_space, need_accommodation):
        self.fellow_id = fellow_id
        self.fellow_name = name
        self.fellow_office = office
        self.fellow_living_space = living_space
        self.fellow_need_accommodation = need_accommodation


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

        engine = create_engine('sqlite:///{}'.format(db_path))
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
                FellowDB(fellow_id=fellow.id, name=fellow.name, office=fellow.office, living_space=fellow.living_space,
                         need_accommodation=fellow.accommodation),
                _warn=False
            )

        for staff in people['staff']:
            self.db.add(StaffDB(staff_id=staff.id, name=staff.name, office=staff.office), _warn=False)

        self.db.commit()

        return True

    def load_state(self):
        """
        loads the state of db to amity
        :return:
        """
        offices = {}
        living_spaces = {}
        fellows_list = []
        staff_list = []

        max_staff_id = 0
        max_fellow_id = 0

        rooms_db = self.db.query(RoomDB.name, RoomDB.type).all()

        # retrieve and create rooms from db
        for room in rooms_db:
            if room.type == Constants.LIVING_SPACE:
                living_space = LivingSpace(str(room.name))
                living_spaces[living_space.name] = living_space

            elif room.type == Constants.OFFICE:
                office = Office(str(room.name))
                offices[office.name] = office

        # get staff members
        staff_db = self.db.query(StaffDB).all()
        for staff_data in staff_db:
            staff = Staff(staff_data.staff_name, id=staff_data.staff_id, office=staff_data.staff_office)
            staff_list.append(staff)

            if staff.office:
                if staff.office in offices:
                    offices[staff.office].allocate_space(staff)

            if not max_staff_id or max_staff_id < staff.id:
                max_staff_id = str(staff.id)

        # get fellows members
        fellow_db = self.db.query(FellowDB).all()
        for fellow_data in fellow_db:
            fellow = Fellow(fellow_data.fellow_name, id=fellow_data.fellow_id,
                            accommodation=fellow_data.fellow_need_accommodation,
                            office=fellow_data.fellow_office,
                            living_space=fellow_data.fellow_living_space)

            fellows_list.append(fellow)

            if not max_fellow_id or max_fellow_id < fellow.id:
                max_fellow_id = str(fellow.id)

            if fellow.office:
                if fellow.office in offices:
                    offices[fellow.office].allocate_space(fellow)

            if fellow.living_space:
                if fellow.living_space in living_spaces:
                    living_spaces[fellow.living_space].allocate_space(fellow)

        max_ids = {'(fellow': [int(max_fellow_id[2:])], 'staff': [int(max_staff_id[2:])]}

        return {'fellows': fellows_list, 'staff': staff_list, 'offices': offices.values(),
                'living_spaces': living_spaces.values(), 'current_ids': max_ids}
