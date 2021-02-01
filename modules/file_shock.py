import csv
import os
import json

class FileLocal:

    def check_file_exist(self, filename: str):
        try:
            if filename:
                return os.path.isfile(filename)
            else:
                return None
        except Exception as err:
            print('Error: {}'.format(err))

    def open_file(self, filename: str, mode: str):
        try:
            if filename:
                return open(filename, mode, encoding="utf8")
            else:
                return None
        except Exception as err:
            print('Error: {}'.format(err))

    def open_get_lines(self, filename: str):
        try:
            data = self.open_file(filename, 'r')
            if data:
                return data.readlines()
            else:
                return None
        except IOError as err:
            print('Error: {}'.format(err))

    def save_result(self, str_value: str, filename: str):
        try:
            data_return = self.open_file(filename, 'a+')
            data_return.writelines(str_value)
            data_return.close()
        except IOError as err:
            print('Error: {}'.format(err))

    def open_file_csv(self, filename: str, mode: str):
        try:
            data_file = self.open_file(filename, mode)
            if data_file:
                data_return = csv.DictReader(data_file)
                return data_file, data_return
            else:
                return None
        except IOError as err:
            print('Error: {}'.format(err))

    def open_file_json(self, filename:str):
        try:
            myFile = self.open_file(filename, 'r')
            myFile = json.load(myFile)
            return myFile
        except IOError as err:
            print('Error: {}'.format(err))
