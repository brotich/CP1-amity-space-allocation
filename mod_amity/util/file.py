class FileUtil(object):

    @staticmethod
    def read_from_file(file_name):
        people_data = []
        with open(file_name) as file_handle:
            file_data = file_handle.readlines()

            while file_data:
                people_data.append(file_data.pop().strip().split())

        return people_data
