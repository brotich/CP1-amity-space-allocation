#!/usr/bin/env python2

"""
Usage:
    amity create_room <room_name>...
    amity add_person <first_name> <last_name> (Fellow|Staff) [<wants_accomodation>]
    amity reallocate_person <person_name> <new_room_name>
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

import sys
import os
import cmd
from docopt import docopt, DocoptExit

from mod_amity.amity import Amity


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
    file = None

    @docopt_cmd
    def do_add_person(self, args):
        """Usage:
        add_person <first_name> <last_name> <role> [<wants_accommodation>]"""
        name = "{} {}".format(args["<first_name>"], args["<last_name>"])
        role = args["<role>"].upper()

        if role not in ["FELLOW", "STAFF"]:
            print ("Invalid: role should STAFF or FELLOW")
            return

        if role == "STAFF":
            staff = amity.create_staff(name)
            print ("{} created successfully".format(staff.role))
            print ("    ID:   {}".format(staff.id))
            print ("    Name: {}".format(staff.name))
            print (" ")

            if staff.office:
                print ("allocated Office {} ".format(staff.office))
            else:
                print ("No vacant Office to allocate")

        if role == "FELLOW":
            wants_accommodation = args["<wants_accommodation>"].upper() if args["<wants_accommodation>"] else 'N'

            if wants_accommodation not in ["Y", "N"]:
                print ("Invalid: wants_accommodation values are 'Y' or 'N'")
                return

            fellow = amity.create_fellow(name, accommodation='N')

            print ("{} created successfully".format(fellow.role))
            print ("    ID:   {}".format(fellow.id))
            print ("    Name: {}".format(fellow.name))
            print (" ")

            if fellow.office:
                print ("allocated Office {} ".format(fellow.office))
            else:
                print ("No vacant Office to allocate")
            if fellow.living_space:
                print ("allocated Living Space {} ".format(fellow.living_space))
            else:
                print ("No vacant Living Space to allocate")

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_type> <room_names>..."""
        room_type = args["<room_type>"].upper()

        if room_type not in ["LIVING", "OFFICE"]:
            print ("Invalid Command: valid room names 'LIVING', 'OFFICE']")
            return

        room_names = args['<room_names>']

        if room_type == "LIVING":
            for room_name in room_names:
                amity.create_living_space(room_name)
        elif room_type == "OFFICE":
            for room_name in room_names:
                amity.create_office(room_name)

        print ("Created {} rooms: {}".format(room_type, ", ".join(room_names)))

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage:
                reallocate_person <person_id> <new_room_name>
        """
        person_id = args['<person_id>'].upper()
        new_room_name = args['<new_room_name>']

        relocate_data = amity.relocate_person(person_id, new_room_name)

        print ("{} relocated from {} to {}".format(relocate_data['person'], relocate_data['old_room'],
                                                   relocate_data['new_room']))

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated"""

        unallocated = amity.get_unallocated_persons()

        print ("Staff")
        print ("=" * 75)
        if unallocated["staff"]:
            for staff in unallocated["staff"]:
                print ("    {} {}".format(staff.id, staff.name))
        else:
            print ("All Staff Allocated")
        print ("=" * 75)
        print ("")
        print ("Fellow")
        print ("=" * 75)
        if unallocated["fellows"]:
            for fellow in unallocated["fellows"]:
                print ("    {} {}".format(fellow.id, fellow.name))
        else:
            print ("All fellows Allocated")
        print ("=" * 75)

    @docopt_cmd
    def do_print_room(self, args):
        """Usage:
        print_room <room_name>
        """
        room_name = args["<room_name>"]
        room = amity.get_rooms(room_name)

        print ("room: {}".format(room.name))
        print ("=" * 25)
        print ("Allocations: ")
        for i, person in enumerate(room.occupants):
            print ("   {}. {} {}".format(i + 1, person.id, person.name))

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
