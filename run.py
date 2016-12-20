#!/usr/bin/env python2

"""
Usage:
    amity create_room (living|office) <room_name>...
    amity add_person <first_name> <last_name> (fellow|staff) [<wants_accomodation>]
    amity reallocate_person <person_id> <new_room_name>
    amity load_people <filename>
    amity print_allocations [-o <filename>]
    amity print_unallocated [-o <filename>]
    amity print_room <room_name>
    amity (-i | --interactive)
    amity (-h | --help)
Options:
    -o, --output  Save to a txt file
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

from __future__ import print_function, unicode_literals
from docopt import docopt, DocoptExit
import sys
import os
import cmd

from clint.textui import indent, puts

from tabulate import tabulate

from mod_amity.amity import Amity
from mod_amity.models import Constants


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


amity = Amity()


class AmityRun(cmd.Cmd):
    intro = 'Welcome to Amity' \
            + ' (type help for a list of commands.)'
    prompt = '(amity) '

    @docopt_cmd
    def do_add_person(self, args):
        """
        Usage: add_person <first_name> <last_name> <role> [<wants_accommodation>]
        """
        name = "{} {}".format(args["<first_name>"], args["<last_name>"])
        role = args["<role>"].upper()

        if role not in ["FELLOW", "STAFF"]:
            print("Invalid: role should STAFF or FELLOW")
            return

        accommodation = args['<wants_accommodation>'].upper() if args['<wants_accommodation>'] else None

        try:

            person = amity.add_person(name, role, accommodation)

            print("{} {} created successfully".format(person.role, person.name))
            if person.office is not None:
                print("allocated office space at {} ".format(person.office))
            else:
                print("No vacant office to allocate")
            if person.role == Constants.FELLOW and person.accommodation == 'Y':
                if person.living_space is None:
                    print("allocate living space at {} ".format(person.living_space))
                else:
                    print("No vacant living spaces")
        except Exception as ex:
            puts("Error: "+ex.message)

    @docopt_cmd
    def do_create_room(self, args):
        """
            Usage: create_room <room_type> <room_names>...
        """
        room_type = args["<room_type>"].upper()

        if room_type not in ["LIVING", "OFFICE"]:
            print("Invalid Command: valid room names 'LIVING', 'OFFICE']")
            return

        room_names = args['<room_names>']

        try:

            if room_type == "LIVING":
                for room_name in room_names:
                    amity.create_living_space(room_name)
            elif room_type == "OFFICE":
                for room_name in room_names:
                    amity.create_office(room_name)

            print("Created {} rooms: {}".format(room_type, ", ".join(room_names)))
        except Exception as ex:
            puts("Error: " + ex.message)

    @docopt_cmd
    def do_reallocate_person(self, args):
        """
        Usage: reallocate_person <person_id> <new_room_name>
        """
        person_id = args['<person_id>'].upper()
        new_room_name = args['<new_room_name>']

        try:

            relocate_data = amity.relocate_person(person_id, new_room_name)

            print("{} relocated from {} to {}".format(relocate_data['person'], relocate_data['old_room'],
                                                      relocate_data['new_room']))
        except Exception as ex:
            puts("Error: " + ex.message)

    @docopt_cmd
    def do_print_unallocated(self, args):
        """
            Usage: print_unallocated
        """
        try:
            unallocated = amity.get_unallocated_persons()

            puts("Unallocated Persons")
            with indent(4):
                puts("1. Staff")
                with indent(4):
                    if unallocated["staff"]:
                        puts(tabulate([[i + 1, staff.id, staff.name] for i, staff in enumerate(unallocated["staff"])],
                                      headers=['ID', 'NAME'], tablefmt='orgtbl', missingval="---"))
                    else:
                        puts("All Staff Allocated")

            with indent(4):
                puts("2. Fellows")
                with indent(4):
                    if unallocated["fellows"]:
                        puts(tabulate([[i + 1, fellow.id, fellow.name, fellow.office, fellow.living_space] for i, fellow in
                                       enumerate(unallocated["fellows"])],
                                      headers=['ID', 'NAME', 'OFFICE', 'LIVING SPACE'], tablefmt='orgtbl',
                                      missingval="---"))
                    else:
                        puts("All Fellows Allocated")
        except Exception as ex:
            puts("Error: " + ex.message)

    @docopt_cmd
    def do_print_room(self, args):
        """
            Usage: print_room <room_name>
        """
        room_name = args["<room_name>"]

        try:
            room = amity.get_rooms(room_name)

            with indent(4):
                puts("Room: {}({})".format(room.name.upper(), room.type))
                with indent(2):
                    puts("Occupants: ")
                    occupants = [[i + 1, occupant.id, occupant.name, occupant.role] for i, occupant in
                                 enumerate(room.occupants)]
                    puts(tabulate(occupants,
                                  headers=['ID', 'NAME', 'ROLE'], tablefmt='orgtbl', missingval="---"))
        except Exception as ex:
            puts("Error: " + ex.message)

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations
        """
        try:
            rooms = amity.get_rooms()

            puts("Offices")
            with indent(4):
                for office in rooms['offices']:
                    puts(office.name)
                    with indent(4):
                        occupants = [[occupant.id, occupant.name, occupant.role] for occupant in office.occupants]
                        puts(tabulate(occupants,
                                      headers=['ID', 'NAME', 'ROLE'], tablefmt='orgtbl', missingval="---"))

            puts("Living Spaces")
            with indent(4):
                for living_space in rooms['living_spaces']:
                    puts(living_space.name)
                    with indent(4):
                        occupants = [[occupant.id, occupant.name, occupant.role] for occupant in living_space.occupants]
                        puts(tabulate(occupants,
                                      headers=['ID', 'NAME', 'ROLE'], tablefmt='orgtbl', missingval="---"))
        except Exception as ex:
            puts("Error: " + ex.message)

    @docopt_cmd
    def do_load_people(self, args):
        """
        Usage: load_people <file_name>
        """
        file_name = args['<file_name>']

        try:
            loaded_people = amity.load_people(os.path.dirname(os.path.realpath(__file__)) + "/" + file_name)

            puts("Loaded Persons")
            with indent(4):
                puts(
                    tabulate(
                        [[i + 1, person.id, person.name, person.role,
                          person.accommodation if person.role == Constants.FELLOW else None] for i, person in
                         enumerate(loaded_people)],
                        headers=['ID', 'NAME', 'ROLE', 'ACCOMM.'], tablefmt='orgtbl', missingval="----"
                    )
                )
        except Exception as ex:
            puts("Error: " + ex.message)

    @docopt_cmd
    def do_save_state(self, args):
        """
            Usage: save_state [--db=sqlite_database]
        """
        db_name = "amity.sqlite"
        if args['--db']:
            db_name = args['--db']

        try:
            db_path = os.path.dirname(os.path.realpath(__file__)) + "/" + db_name
            if amity.save_state(db_path):
                puts("Successfully saved state to file {}".format(db_name))
        except Exception as ex:
            puts("Error: " + ex.message)

    @docopt_cmd
    def do_load_state(self, args):
        """
            Usage: load_state [--db=sqlite_database]
        """
        db_name = "amity.sqlite"
        if args['--db']:
            db_name = args['--db']

        try:
            db_path = os.path.dirname(os.path.realpath(__file__)) + "/" + db_name
            if amity.load_state(db_path):
                print ("Successfully loaded state from {}".format(db_name))
            else:
                raise Exception("Failed to load data from {}".format(db_name))
        except Exception as ex:
            print (ex.message)

    def do_clear(self, arg):
        """Clears screen>"""

        os.system('clear')

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    AmityRun().cmdloop()
