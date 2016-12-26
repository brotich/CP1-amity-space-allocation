class Constants(object):
    STAFF = "Staff"
    FELLOW = "Fellow"
    LIVING_SPACE = "Living Space"
    OFFICE = "Office"


class Person(object):
    """
    Boiler-plate class for creating a person instance.
    Its inherited to form Fellows and Staff subclasses
    """

    def __init__(self, name, id=None):
        if name.strip() == " ":
            raise ValueError("name cannot empty")

        self.name, self.id = name, id
        self.office, self.role = None, None

    def assign_office(self, office_name):
        self.office = office_name

    def get_role(self):
        return self.role


class Staff(Person):
    def __init__(self, name, id=None):
        super(Staff, self).__init__(name, id=id)
        self.role = Constants.STAFF
        self.office = None


class Fellow(Person):
    def __init__(self, name, accommodation='N', id=None):
        super(Fellow, self).__init__(name, id=id)
        if accommodation not in ['N', 'Y']:
            raise ValueError("accommodation should be Y or N")
        self.accommodation = accommodation
        self.office, self.living_space = None, None
        self.role = Constants.FELLOW

    def assign_living_space(self, living_space):
        if self.accommodation == 'N':
            raise ValueError("Fellow didn't request living space")
        self.living_space = living_space


class Room(object):
    """
    Boiler plate class for the rooms available in amity.
    It defines the occupants of a room and the capacity of the room
    """

    def __init__(self, name, capacity=None, room_type=None):
        self.room_type = room_type
        if not isinstance(name, str):
            raise TypeError("string expected")
        if len(name) == 0:
            raise ValueError("name cannot be empty")

        self.name = name
        self.occupants = []
        self.capacity = capacity
        self.type = room_type

    def allocate_space(self, person):
        if self.is_full():
            raise ValueError("Room is full")
        if not isinstance(person, Person):
            raise TypeError("Rooms assigned to only fellow or staff")

        self.occupants.append(person)

    def is_full(self):
        return len(self.occupants) >= self.capacity


class Office(Room):
    """
    Office capacity limited to 6 occupants.
    """

    def __init__(self, name):
        super(Office, self).__init__(name, 6, Constants.OFFICE)

    def allocate_space(self, person):
        super(Office, self).allocate_space(person)
        person.office = self.name


class LivingSpace(Room):
    """
    Living space to 4 occupants.
    Constraints: can only be assigned to fellows that requested accommodation
    """

    def __init__(self, name):
        super(LivingSpace, self).__init__(name, 4, Constants.LIVING_SPACE)

    def allocate_space(self, person):
        if not isinstance(person, Fellow):
            raise TypeError("Staff cannot be allocate Living Space")
        super(LivingSpace, self).allocate_space(person)
        person.living_space = self.name
