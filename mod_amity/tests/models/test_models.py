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

        self.assertListEqual([self.staff_name, office], [staff.name, staff.office])


class FellowClassTestCase(unittest.TestCase):

    def setUp(self):
        self.fellow_name1 = fake.first_name() + " " + fake.last_name()
        self.fellow_name2 = fake.first_name() + " " + fake.last_name()

    def test_it_create_fellow(self):
        fellow1 = Fellow(self.fellow_name1)
        fellow2 = Fellow(self.fellow_name2, accommodation='Y')

        self.assertListEqual([self.fellow_name1, 'N'], [fellow1.name, fellow1.accommodation])
        self.assertListEqual([self.fellow_name2, 'Y'], [fellow2.name, fellow2.accommodation])