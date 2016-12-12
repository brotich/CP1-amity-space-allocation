from __future__ import print_function
import random

from mod_amity.models import Office, LivingSpace, Fellow, Staff, Role


class Amity(object):
    def __init__(self):
        self.living_spaces = dict(available=[], unavailable=[])

        self.offices = dict(available=[], unavailable=[])
        self.fellows = []
        self.staff = []
        self.ids = dict(fellow=[0], staff=[0])

        self.allocated_staff = []
        self.allocated_fellows = []

    def create_office(self, name):
        if self.get_rooms(name) is not None:
            raise ValueError("Room with same name exists")
        self.offices["available"].append(Office(name))

    def create_living_space(self, name):
        if self.get_rooms(name) is not None:
            raise ValueError("Room with same name exists")
        self.living_spaces["available"].append(LivingSpace(name))

    def create_fellow(self, name, accommodation='N'):
        fellow = Fellow(name, accommodation=accommodation, id=self.get_fellow_id())
        self.fellows.append(fellow)
        self.allocate_person(fellow)

        return fellow

    def create_staff(self, name):
        staff = Staff(name, id=self.get_staff_id())
        self.staff.append(staff)
        self.allocate_person(staff)

        return staff

    def allocate_person(self, person):

        office = random.choice(self.offices["available"]) if len(self.offices["available"]) > 0 else None
        living_space = random.choice(self.living_spaces["available"]) \
            if len(self.living_spaces["available"]) > 0 else None

        if office is not None:
            office.allocate_space(person)
            person.assign_office(office.name)

            if office.is_full():
                self.offices["unavailable"].append(office)
                self.offices["available"].remove(office)

        if person.role == Role.FELLOW:
            if living_space is not None and person.accommodation == 'Y':
                living_space.allocate_space(person)
                person.assign_living_space(living_space.name)

                if living_space.is_full():
                    self.living_spaces["unavailable"].append(living_space)
                    self.living_spaces["available"].remove(living_space)

        self.check_person_allocation(person)

    def get_unallocated_persons(self):
        return dict(staff=list(set(self.staff) - set(self.allocated_staff)),
                    fellows=list(set(self.fellows) - set(self.allocated_fellows)))

    def get_rooms(self, room_name=None):
        offices = self.offices["unavailable"] + self.offices["available"]
        living_spaces = self.living_spaces["unavailable"] + self.living_spaces["available"]
        rooms = offices + living_spaces
        if room_name is not None:
            for room in rooms:
                if room.name == room_name:
                    return room
        else:
            return dict(living_spaces=living_spaces, offices=offices)

    def get_staff_id(self):
        staff_id = self.ids["staff"][0] + 1
        self.ids["staff"][0] = staff_id
        return "ST{0}".format(str(staff_id).rjust(3, '0'))

    def get_fellow_id(self):
        staff_id = self.ids["fellow"][0] + 1
        self.ids["fellow"][0] = staff_id
        return "FL{0}".format(str(staff_id).rjust(3, '0'))

    def check_person_allocation(self, person):
        if person.role == Role.STAFF:
            if person.office is not None:
                self.allocated_staff.append(person)

        elif person.role == Role.FELLOW:
            if person.living_space is not None and person.office is not None:
                self.allocated_fellows.append(person)

    def find_person(self, name):
        match = []
        for person in (self.fellows + self.staff):
            if name in person.name:
                match.append(person)
        return match

    def relocate_person(self, person_id, new_room):
        pass
