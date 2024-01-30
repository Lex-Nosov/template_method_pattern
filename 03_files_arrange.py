# -*- coding: utf-8 -*-

import os
import shutil
import time
import zipfile


# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени последней модификации файла
# (время создания файла берется по разному в разых ОС - см https://clck.ru/PBCAX - поэтому берем время модификации).
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником ОС в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит, см .gitignore в папке ДЗ)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4


class SortedAndCopyFiles:

    def __init__(self, start_folder, source_folder):
        self.start_folder = start_folder
        self.source_folder = source_folder
        self.files = None
        self.path = os.path.dirname(__file__)

    def extracting_files(self):
        with zipfile.ZipFile(self.start_folder, 'r') as zip_file:
            for file_png in zip_file.infolist():
                if not file_png.filename.endswith('/'):
                    path = self.makes_folder_and_path(file_png.date_time)
                    name = file_png.filename.split('/').pop()
                    new_path = os.path.join(path, name)
                    with zip_file.open(name=file_png) as z_file:
                        with open(file=new_path, mode='wb') as path_for_write:
                            shutil.copyfileobj(fsrc=z_file, fdst=path_for_write)
                    # лучше перенести во так
                    meta = time.mktime(file_png.date_time + (0, 0, 0))
                    os.utime(new_path, (meta, meta))

    def makes_folder_and_path(self, modification_date):
        year = str(modification_date[0])
        month = str(modification_date[1])
        path_for_write = os.path.join(self.path, self.source_folder, year, month)
        if not os.path.exists(path_for_write):
            os.makedirs(path_for_write)
        return path_for_write


sort = SortedAndCopyFiles('icons.zip', 'icons_by_year')
sort.extracting_files()

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится только к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html
