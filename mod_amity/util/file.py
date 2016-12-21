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
    def write_to_file(file_path, data):

        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, mode='w') as file_handle:
            for line in data:
                file_handle.write(line + "\n")
            file_handle.flush()

        return True
