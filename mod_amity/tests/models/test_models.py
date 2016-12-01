import unittest

from mod_amity.models import Staff, Role, Fellow
from mod_amity.tests import fake


class StaffClassTestCase(unittest.TestCase):
    def setUp(self):
        self.staff_name = fake.first_name() + " " + fake.last_name()

    def test_it_create_staff(self):
        staff = Staff(self.staff_name)
        self.assertEqual(self.staff_name, staff.name)
        self.assertEqual(Role.STAFF, staff.get_role())

    def test_it_assigns_office(self):
        office = "Narnia"
        staff = Staff(self.staff_name)
        staff.assign_office(office)

        self.assertEqual(office, staff.office)


class FellowClassTestCase(unittest.TestCase):
    def setUp(self):
        self.fellow_name1 = fake.first_name() + " " + fake.last_name()
        self.fellow_name2 = fake.first_name() + " " + fake.last_name()

    def test_it_create_fellow(self):
        fellow1 = Fellow(self.fellow_name1)
        fellow2 = Fellow(self.fellow_name2, accommodation='Y')

        self.assertListEqual([self.fellow_name1, 'N'], [fellow1.name, fellow1.accommodation])
        self.assertListEqual([self.fellow_name2, 'Y'], [fellow2.name, fellow2.accommodation])
        self.assertEqual(Role.FELLOW, fellow2.get_role())

    def test_it_assigns_office(self):
        fellow = Fellow(self.fellow_name1)
        office = "Narnia"

        fellow.assign_office(office)

        self.assertEqual(office, fellow.office)

    def test_it_assigns_living_space(self):
        fellow1 = Fellow(self.fellow_name1, accommodation='Y')
        fellow2 = Fellow(self.fellow_name2)

        living_space = "Shell"

        fellow1.assign_living_space(living_space)

        self.assertEqual(living_space, fellow1.living_space)
        with self.assertRaises(ValueError)as exception:
            fellow2.assign_living_space(living_space)
            self.assertEqual("Fellow didn't request living space", exception.exception)


class OfficeClassTestCase(object):

    def test_it_create_new_room(self):
        pass

    def test_max_capacity_4(self):
        pass

    def test_it_assigns_staff(self):
        pass

    def test_it_assigns_fellow(self):
        pass

    def test_error_assign_more_than_4_perons(self):
        pass