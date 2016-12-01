import unittest

from mod_amity.models import Staff, Role
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
