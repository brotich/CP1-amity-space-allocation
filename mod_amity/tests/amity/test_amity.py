from __future__ import print_function
from unittest import TestCase

import mock

from mod_amity.amity import Amity
from mod_amity.tests.amity import fake


class AmityTestCase(TestCase):
    def setUp(self):
        self.amity = Amity()

    def test_create_office(self):
        self.amity.create_office("Summer")

        self.assertGreater(len(self.amity.offices["available"]), 0)
        self.assertEqual("Summer", self.amity.offices["available"][0].name)

    def test_create_living_space(self):
        self.amity.create_living_space("Winter")

        self.assertGreater(len(self.amity.living_spaces["available"]), 0)
        self.assertEqual("Winter", self.amity.living_spaces["available"][0].name)

    def test_create_fellow(self):
        name = fake.first_name() + " " + fake.last_name()
        self.amity.create_living_space("Shell")
        self.amity.create_office("Hogwarts")
        fellow = self.amity.create_fellow(name)

        self.assertGreater(len(self.amity.fellows), 0)
        self.assertEqual(name, self.amity.fellows[0].name)

        self.assertIsNone(fellow.living_space)
        self.assertEqual("Hogwarts", fellow.office)

    def test_create_fellow_with_accommodation(self):
        name = fake.first_name() + " " + fake.last_name()
        self.amity.create_living_space("Shell")
        self.amity.create_office("Hogwarts")
        fellow = self.amity.create_fellow(name, accommodation='Y')

        self.assertEqual("Shell", fellow.living_space)
        self.assertEqual("Hogwarts", fellow.office)

    def test_create_staff(self):
        name = fake.first_name() + " " + fake.last_name()
        self.amity.create_living_space("Shell")
        self.amity.create_office("Hogwarts")

        staff = self.amity.create_staff(name)

        self.assertGreater(len(self.amity.staff), 0)
        self.assertEqual(name, staff.name)
        self.assertEqual("Hogwarts", staff.office)

    def test_adds_unallocated_persons(self):
        staff_name = fake.first_name() + " " + fake.last_name()
        fellow_name = fake.first_name() + " " + fake.last_name()

        staff = self.amity.create_staff(staff_name)
        fellow = self.amity.create_fellow(fellow_name)

        self.assertDictEqual({"fellows": [fellow], "staff": [staff]}, self.amity.get_unallocated_persons())

    def test_return_room_object_on_existing_room(self):
        office_name = "Krypton"
        living_space_name = "Peri"
        self.amity.create_office(office_name)
        self.amity.create_living_space(living_space_name)

        self.assertEqual(office_name, self.amity.get_room(office_name).name)
        self.assertEqual(living_space_name, self.amity.get_room(living_space_name).name)

    def test_raise_error_on_creating_existing_living_space(self):
        living_space_name = "Perl"

        self.amity.create_living_space("Perl")

        self.amity.create_living_space("Perl")



