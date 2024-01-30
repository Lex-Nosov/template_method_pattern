# -*- coding: utf-8 -*-

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4

import zipfile

zip_file = 'voyna-i-mir.txt.zip'


class LetterStatistics:

    def __init__(self, filename):
        self.filename = filename
        self.sequence = 'А'
        self.stats = {}

    def unzip(self):
        zfile = zipfile.ZipFile(self.filename, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename)
            self.filename = filename

    def open_file(self):
        if self.filename.endswith('.zip'):
            self.unzip()
        with open(self.filename, 'r', encoding='cp1251') as file:
            return file.read()

    def get_data(self):
        file = self.open_file()
        for char in file:
            if char.isalpha():
                if self.sequence in self.stats:
                    self.stats[self.sequence] += 1
                else:
                    self.stats[self.sequence] = 1
                self.sequence = char

    def sorted_stats(self):
        self.get_data()
        total_stats = sorted(self.stats.items(), key=lambda kv: kv[1], reverse=True)
        return total_stats

    def output(self):
        total_count = 0
        stats = self.sorted_stats()
        print(f'+---------+------------+')
        print(f'|  буква  | частота    |')
        print(f'+---------+------------+')
        for elem in stats:
            total_count += elem[1]
            print(f'|    {elem[0]}    |   {elem[1]:7d}  |')
        print(f'+---------+------------+')
        print(f'|  итого  |   {total_count}  |')
        print(f'+---------+------------+')


letter_statistics = LetterStatistics(filename=zip_file)
letter_statistics.output()


# После зачета первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию

class SortAscending(LetterStatistics):

    def sorted_stats(self):
        self.get_data()
        total_stats = sorted(self.stats.items(), key=lambda value: value[1])
        return total_stats


class SortAlphabetically(LetterStatistics):  # буква Ё неправильно сортируется

    def sorted_stats(self):
        self.get_data()
        total_stats = sorted(self.stats.items(), key=lambda letter: letter[0])
        return total_stats


class SortAlphabeticallyAscending(LetterStatistics):  # буква Ё неправильно сортируется

    def sorted_stats(self):
        self.get_data()
        total_stats = sorted(self.stats.items(), key=lambda letter: letter[0], reverse=True)
        return total_stats
