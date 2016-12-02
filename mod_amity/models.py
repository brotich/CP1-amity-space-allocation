
class Role(object):
    STAFF = 0
    FELLOW = 1


class Person(object):
    role = None

    def __init__(self, name):

        if isinstance(name, str):
            raise TypeError("name should be string")

        if len(name) == 0:
            raise ValueError("name cannot empty")

        self.name = name
        self.office = None

    def assign_office(self, office):
        self.office = office

    def get_role(self):
        return self.role


class Staff(Person):
    role = Role.STAFF


class Fellow(Person):
    role = Role.FELLOW
    living_space = None

    def __init__(self, name, accommodation='N'):
        super(self.__class__, self).__init__(name)
        self.accommodation = accommodation

    def assign_living_space(self, living_space):
        if self.accommodation == 'N':
            raise ValueError("Fellow didn't request living space")
        self.living_space = living_space


class Room(object):
    capacity = None
    occupants = []

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("string expected")
        if len(name) == 0:
            raise ValueError("name cannot be empty")
        self.name = name
        self.occupants = []

    def allocate_space(self, person):
        if not isinstance(person, Person):
            raise TypeError("office assigned to fellow or staff")
        if len(self.occupants) > 4:
            raise ValueError("Room is full")
        self.occupants.append(person)

    def get_capacity(self):
        return self.capacity


class Office(Room):
    capacity = 6


class LivingSpace(Room):
    capacity = 4



