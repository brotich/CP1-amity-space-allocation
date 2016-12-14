from __future__ import print_function

import random
from unittest import TestCase

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

        self.assertEqual(office_name, self.amity.get_rooms(office_name).name)
        self.assertEqual(living_space_name, self.amity.get_rooms(living_space_name).name)

    def test_raise_error_on_creating_existing_living_space(self):
        living_space_name = "Perl"
        self.amity.create_living_space(living_space_name)

        with self.assertRaises(ValueError) as exception:
            self.amity.create_living_space("Perl")
            self.assertIn("Room with same name exists", exception)

    def test_raise_error_on_creating_existing_office(self):
        office_name = "Krypton"
        self.amity.create_office(office_name)

        with self.assertRaises(ValueError) as exception:
            self.amity.create_office(office_name)
            self.assertIn("Room with same name exists", exception)

    def test_gets_all_rooms(self):
        office_name = "Krypton"
        living_space_name = "Peri"

        self.amity.create_office(office_name)
        self.amity.create_living_space(living_space_name)

        self.assertIn(office_name, [room.name for room in self.amity.get_rooms()["offices"]])
        self.assertIn(living_space_name, [room.name for room in self.amity.get_rooms()["living_spaces"]])

    def test_search_person_by_name(self):
        staff_names = [(fake.first_name() + " " + fake.last_name()) for i in range(3)]
        fellow_names = [(fake.first_name() + " " + fake.last_name()) for i in range(3)]

        for staff_name in staff_names:
            self.amity.create_staff(staff_name)

        for fellow_name in fellow_names:
            self.amity.create_fellow(fellow_name)

        random_staff = random.choice(staff_names)
        random_fellow = random.choice(fellow_names)

        self.assertIn(random_staff, [person.name for person in self.amity.find_person_by_name(random_staff)])
        self.assertIn(random_fellow, [person.name for person in self.amity.find_person_by_name(random_fellow)])
        self.assertEqual([], self.amity.find_person_by_name("Kimani Johns"))

    def test_relocate_fellow(self):
        office_names = ["Krypton", "Carmelot"]
        living_space_names = ["Peri", "Perl"]
        fellow_name = fake.first_name() + " " + fake.last_name()

        for office_name in office_names:
            self.amity.create_office(office_name)
        for living_space_name in living_space_names:
            self.amity.create_living_space(living_space_name)

        fellow = self.amity.create_fellow(fellow_name, accommodation='Y')
        office_names.remove(fellow.office)
        living_space_names.remove(fellow.living_space)

        new_office = office_names.pop()
        new_living_space = living_space_names.pop()

        self.amity.relocate_person(fellow.id, new_office)
        self.amity.relocate_person(fellow.id, new_living_space)

        self.assertEqual(new_office, fellow.office)
        self.assertEqual(new_living_space, fellow.living_space)


