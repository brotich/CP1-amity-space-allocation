
class Role(object):
    STAFF = 0
    FELLOW = 1


class Person(object):

    def __init__(self, name, id=None):

        if isinstance(name, str):
            raise TypeError("name should be string")

        if len(name) == 0:
            raise ValueError("name cannot empty")

        self.name = name
        self.office = None
        self.role = None
        self.id = id

    def assign_office(self, office):
        self.office = office

    def get_role(self):
        return self.role


class Staff(Person):

    def __init__(self, name, id=None):
        super(self.__class__, self).__init__(name, id=id)
        self.role = Role.STAFF


class Fellow(Person):

    def __init__(self, name, accommodation='N', id=None):
        super(self.__class__, self).__init__(name, id=id)
        self.accommodation = accommodation
        self.living_space = None
        self.role = Role.FELLOW

    def assign_living_space(self, living_space):
        if self.accommodation == 'N':
            raise ValueError("Fellow didn't request living space")
        self.living_space = living_space


class Room(object):

    name = None
    occupants = []
    capacity = None

    def __init__(self, name,  capacity=None):
        if not isinstance(name, str):
            raise TypeError("string expected")
        if len(name) == 0:
            raise ValueError("name cannot be empty")

        self.name = name
        self.occupants = []
        self.capacity = capacity

    def allocate_space(self, person):
        if not len(self.occupants) < self.capacity:
            raise ValueError("Room is full")
        if not isinstance(person, Person):
            raise TypeError("office assigned to fellow or staff")

        self.occupants.append(person)

    def get_capacity(self):
        return self.capacity

    def is_full(self):
        return len(self.occupants) >= self.capacity


class Office(Room):

    def __init__(self, name):
        super(self.__class__, self).__init__(name, 6)


class LivingSpace(Room):

    def __init__(self, name):
        super(self.__class__, self).__init__(name, 4)



