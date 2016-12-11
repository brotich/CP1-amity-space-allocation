from mod_amity.models import Office, LivingSpace, Fellow, Staff


class Amity(object):
    offices = {
        "available": [],
        "unavailable": []
    }
    living_space = {
        "available": [],
        "unavailable": []
    }
    fellows = []
    staff = []
    people = fellows + staff

    def create_office(self, name):
        self.offices["available"].append(Office(name))

    def create_living_space(self, name):
        self.living_space["available"].append(LivingSpace(name))

    def create_fellow(self, name):
        self.fellows.append(Fellow(name))

    def create_staff(self, name):
        self.staff.append(Staff(name))

    def get_unallocated_person(self):
        pass

    def get_rooms(self, room_name=None):
        pass
