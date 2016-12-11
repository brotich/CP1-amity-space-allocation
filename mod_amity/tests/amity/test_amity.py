from __future__ import print_function
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
        self.amity.create_fellow(name)

        self.assertGreater(len(self.amity.fellows), 0)
        self.assertEqual(name, self.amity.fellows[0].name)

        self.assertIsNone(self.amity.fellows[0].living_space)
        self.assertEqual("Hogwarts", self.amity.fellows[0].office)

    def test_create_staff(self):
        name = fake.first_name() + " " + fake.last_name()
        self.amity.create_living_space("Shell")
        self.amity.create_office("Hogwarts")

        self.amity.create_staff(name)

        self.assertGreater(len(self.amity.staff), 0)
        self.assertEqual(name, self.amity.staff[0].name)
        self.assertEqual("Hogwarts", self.amity.staff[0].office)

