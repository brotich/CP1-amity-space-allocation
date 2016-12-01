
class Role(object):
    STAFF = 0
    FELLOW = 1


class Person(object):
    role = None

    def __init__(self, name):

        if type(name) == str:
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


class Office(Room):
    pass
