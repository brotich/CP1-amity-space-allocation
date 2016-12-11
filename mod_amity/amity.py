from mod_amity.models import Office, LivingSpace


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
        pass

    def create_living_space(self, name):
        pass

    def create_fellow(self, name):
        pass

    def create_staff(self, name):
        pass

    def get_unallocated(self):
        pass

    def get_rooms(self, room_name=None):
        pass
