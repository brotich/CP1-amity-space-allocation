from __future__ import print_function, unicode_literals
import os


class FileUtil(object):

    @staticmethod
    def read_from_file(file_name):
        people_data = []

        if not os.path.isfile(file_name):
            raise ValueError("cannot open file {} ".format(file_name))

        with open(file_name) as file_handle:
            file_data = file_handle.readlines()

            while file_data:
                people_data.append(file_data.pop().strip().split())

        return people_data

    @staticmethod
    def write_to_file(file_name, data):

        with open(file_name, mode='rw') as file_handle:
            file_handle.writelines(data)
