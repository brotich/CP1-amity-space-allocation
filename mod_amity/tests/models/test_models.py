from unittest import TestCase

from mod_amity.models import Staff, Role, Fellow, Office, LivingSpace
from mod_amity.tests import fake


class StaffClassTestCase(TestCase):
    def setUp(self):
        self.staff_name = fake.first_name() + " " + fake.last_name()

    def test_it_create_staff(self):
        staff = Staff(name=self.staff_name, id="ST001")
        self.assertEqual(self.staff_name, staff.name)
        self.assertEqual(Role.STAFF, staff.get_role())

    def test_it_assigns_office(self):
        office = "Narnia"
        staff = Staff(name=self.staff_name, id="ST001")
        staff.assign_office(office)

        self.assertEqual(office, staff.office)


class FellowClassTestCase(TestCase):
    def setUp(self):
        self.fellow_name1 = fake.first_name() + " " + fake.last_name()
        self.fellow_name2 = fake.first_name() + " " + fake.last_name()

    def test_it_create_fellow(self):
        fellow1 = Fellow(name=self.fellow_name1, id="FL001")
        fellow2 = Fellow(name=self.fellow_name2, id="FL002", accommodation='Y')

        self.assertListEqual([self.fellow_name1, 'N'], [fellow1.name, fellow1.accommodation])
        self.assertListEqual([self.fellow_name2, 'Y'], [fellow2.name, fellow2.accommodation])
        self.assertEqual(Role.FELLOW, fellow2.get_role())

    def test_it_assigns_office(self):
        fellow = Fellow(name=self.fellow_name1)
        office = "Narnia"

        fellow.assign_office(office)

        self.assertEqual(office, fellow.office)

    def test_it_assigns_living_space(self):
        fellow1 = Fellow(name=self.fellow_name1, id="FL001", accommodation='Y')
        fellow2 = Fellow(name=self.fellow_name2, id="FL001")

        living_space = "Shell"

        fellow1.assign_living_space(living_space)

        self.assertEqual(living_space, fellow1.living_space)
        with self.assertRaises(ValueError) as exception:
            fellow2.assign_living_space(living_space)
            self.assertIn("Fellow didn't request living space", exception)


class OfficeClassTestCase(TestCase):

    def setUp(self):
        self.office_name = "Hogwarts"
        self.staff = [Staff(name=fake.first_name() + " " + fake.last_name())] * 2
        self.fellow = [Fellow(name=fake.first_name() + " " + fake.last_name())] * 7
        self.people = self.fellow + self.staff

    def test_it_create_new_room_instance(self):
        office = Office(self.office_name)

        self.assertEqual(self.office_name, office.name)
        self.assertEqual(6, office.get_capacity())
        self.assertRaises(TypeError, Office, 123)
        self.assertRaises(ValueError, Office, "")

    def test_it_assigns_staff(self):
        office = Office(self.office_name)
        for staff in self.staff:
            office.allocate_space(staff)

        self.assertListEqual(self.staff, office.occupants)

    def test_it_assigns_fellows(self):
        office3 = Office(self.office_name)
        for fellow in self.fellow[:4]:
            office3.allocate_space(fellow)

        self.assertEqual(4, len(office3.occupants))

    def test_error_assign_more_than_6_persons(self):
        office = Office(self.office_name)

        with self.assertRaises(ValueError) as exception:
            for person in self.people:
                office.allocate_space(person)

            self.assertIn("Room is full", exception)


class LivingSpaceTestCase(TestCase):

    def setUp(self):
        self.living_space_name = "Shell"
        self.staff = Staff(name=fake.first_name() + " " + fake.last_name())
        self.fellows = [Fellow(name=fake.first_name() + " " + fake.last_name())] * 7

    def test_it_creates_new_living_space_instance(self):
        living_space = LivingSpace(self.living_space_name)

        self.assertEqual(self.living_space_name, living_space.name)
        self.assertEqual(4, living_space.capacity)

        with self.assertRaises(TypeError) as exception:
            LivingSpace([])
            LivingSpace(123)
            self.assertIn("string expected", exception)

        with self.assertRaises(ValueError) as exception:
            LivingSpace("")
            self.assertIn("name cannot be empty", exception)

    def test_it_assigns_fellow(self):
        living_space = LivingSpace(self.living_space_name)
        living_space.allocate_space(self.fellows[0])

        self.assertEqual(self.fellows[0], living_space.occupants[0])

    def test_it_raises_error_assign_staff(self):
        living_space = LivingSpace(self.living_space_name)

        with self.assertRaises(TypeError) as exception:
            living_space.allocate_space(self.staff)
            self.assertIn("Staff cannot be allocate Living Space", exception)

    def test_error_assign_more_than_4_fellows(self):
        living_space = LivingSpace(self.living_space_name)

        with self.assertRaises(ValueError) as exception:
            for fellow in self.fellows:
                living_space.allocate_space(fellow)

            self.assertIn("Room is full", exception)

