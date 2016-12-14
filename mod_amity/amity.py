from __future__ import print_function
import random

from mod_amity.models import Office, LivingSpace, Fellow, Staff, Role


class Amity(object):
    """
    Amity is the main class
    inherited classes: Room and subclass
                        Person and subclass
    from models.py. It also creates and perform operations to manage allocations on the available rooms in amity
    """
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
        fellow = Fellow(name, accommodation=accommodation, id=self.generate_fellow_id())
        self.fellows.append(fellow)
        self.allocate_person(fellow)

        return fellow

    def create_staff(self, name):
        staff = Staff(name, id=self.get_staff_id())
        self.staff.append(staff)
        self.allocate_person(staff)

        return staff

    def allocate_person(self, person):
        """
        assign space to fellow/staff as requested from the available rooms, as follows
            Staff: Office
            Fellow: Office, Living Space(if requested)
        :param person: created person instance
        :return: person object with allocations, if any
        """
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

        return person

    def get_unallocated_persons(self):
        """
        gets persons not fully allocated spaces
        :return: dict with  fellows and staff
        """
        return dict(staff=list(set(self.staff) - set(self.allocated_staff)),
                    fellows=list(set(self.fellows) - set(self.allocated_fellows)))

    def get_rooms(self, room_name=None):
        """
        gets all offices and living spaces in the allocation pool
        :param room_name: (optional) filter the result by name
        :return: dict of all living_spaces and offices
        """
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
        """
        generate unique ids for staff
        :return: staff id i.e ST001
        """
        staff_id = self.ids["staff"][0] + 1
        self.ids["staff"][0] = staff_id
        return "ST{0}".format(str(staff_id).rjust(3, '0'))

    def generate_fellow_id(self):
        """
        generate unique ids for fellow
        :return: staff id i.e FL001
        """
        staff_id = self.ids["fellow"][0] + 1
        self.ids["fellow"][0] = staff_id
        return "FL{0}".format(str(staff_id).rjust(3, '0'))

    def check_person_allocation(self, person):
        """
        checks if fellow/staff is fully allocated and add to allocated list
        :param person: an instance of fellow or staff
        :return:
        """
        if person.role == Role.STAFF:
            if person.office is not None:
                self.allocated_staff.append(person)

        elif person.role == Role.FELLOW:
            if person.living_space is not None and person.office is not None:
                self.allocated_fellows.append(person)

    def find_person_by_name(self, name):
        """
        Search combined list of fellows and staff for partial match of name
        :param name:
        :return: List of person object matching name
        """
        match = []
        for person in (self.fellows + self.staff):
            if name in person.name:
                match.append(person)
        return match

    def find_person_by_id(self, person_id):
        """
        get staff/fellow matching the id
        :param person_id:
        :return: Fellow/staff object on matching search
        """
        for person in (self.fellows + self.staff):
            if person.id == person_id:
                return person

    def relocate_person(self, person_id, room_name):
        """
        relocate allocated person from current position to new office
        :param person_id: unique id for Staff/fellow
        :param room_name: room to move to
        :return: dict with person and new room
        """

        person = self.find_person_by_id(person_id)
        new_room = self.get_rooms(room_name)

        if not person:
            raise ValueError("Cannot Find person with id" + person_id)

        if new_room.is_full():
            raise ValueError("{} is full. Cannot relocate person".format(room_name))

        old_room = None

        if new_room.type == Role.OFFICE:
            old_room = self.get_rooms(person.office)
        elif new_room.type == Role.LIVING_SPACE:
            old_room = self.get_rooms(person.living_space)

        for occupant in old_room.occupants:
            if occupant.id == person_id:
                old_room.occupants.remove(occupant)
                new_room.allocate_space(occupant)

                if new_room.type == Role.OFFICE:
                    occupant.office = new_room.name
                elif new_room.type == Role.LIVING_SPACE:
                    occupant.living_space = new_room.name

        return dict(person=person, new_room=new_room)








