# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4


class ReadAndWrite:

    def __init__(self, filename):
        self.file = filename
        self.total = {}
        self.value = 'NOK'

    def open_file(self):
        with open(self.file, 'r', encoding='utf8') as file:
            return file.readlines()

    def get_data(self):
        file = self.open_file()
        for line in file:
            if self.value in line:
                new_string = self.formatted_string(line)
                self.sorting_data(new_string)

    def formatted_string(self, string_for_formatting):
        new_string = f'[{string_for_formatting[1:17]}]'
        return new_string

    def sorting_data(self, new_string):
        if new_string in self.total:
            self.total[new_string] += 1
        else:
            self.total[new_string] = 1

    def write_data(self, filename_to_write):
        self.get_data()
        with open(filename_to_write, 'w', encoding='utf8') as file:
            for line in self.total:
                count = self.total[line]
                date_and_count = f'{line} {count}\n'
                file.write(date_and_count)


# После зачета первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году

class ReadAndWriteHour(ReadAndWrite):

    def formatted_string(self, string_for_formatting):
        new_string = f'[{string_for_formatting[1:14]}]'
        return new_string


class ReadAndWriteMonth(ReadAndWrite):

    def formatted_string(self, string_for_formatting):
        new_string = f'[{string_for_formatting[1:8]}]'
        return new_string


class ReadAndWriteYear(ReadAndWrite):

    def formatted_string(self, string_for_formatting):
        new_string = f'[{string_for_formatting[1:5]}]'
        return new_string


run = ReadAndWriteHour(filename='events.txt')
run.write_data('out.txt')
