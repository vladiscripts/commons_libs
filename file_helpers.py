#!/usr/bin/env python3
# -*- coding: utf-8  -*-#
# author: https://github.com/vladiscripts
#
# Библиотека общих функций:
# работа с файлами в utf-8
#
from sys import version_info
import os
import errno
import csv

PYTHON_VERSION = version_info.major
if PYTHON_VERSION == 3:
    from urllib.parse import urlsplit, parse_qs, parse_qsl, unquote, quote, urljoin, urlencode, quote_plus, urldefrag
else:
    from urllib import urlencode, quote  # python 2.7
from vladi_commons.vladi_helpers import list_clean_empty_strs
# from vladi_commons.vladi_commons import csv_save_dict_fromListWithHeaders, json_store_to_file, json_data_from_file
import sqlite3
import json
from lxml.html import fromstring
import re
# import html5lib
from urllib.parse import urlparse, parse_qs, parse_qsl, unquote, quote


def filepaths_of_directory(directory, filename_ext):
    """Список файлов директории с фильтром по расширению"""
    # filename_ext = '.xlsx'
    filenames = filter(lambda x: x.endswith(filename_ext), os.listdir(directory))
    full_files_paths = [os.path.join(directory, filename) for filename in filenames]
    return full_files_paths


''


def make_directory(path, normalize=True):
    if normalize:
        path = os.path.normpath(path)
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def save_file_text_makedir(path, pagename, text, normalize=True):
    """ Save main to html """
    make_directory(path, normalize=True)
    if normalize:
        pagename = os.path.normpath(pagename)
    fpath = os.path.join(path, pagename)
    file_savetext(fpath, text)


def save_file_bin_makedir(path, pagename, data, normalize=True):
    """ Save main to html """
    make_directory(path, normalize=True)
    if normalize:
        pagename = os.path.normpath(pagename)
    fpath = os.path.join(path, pagename)
    file_save(fpath, data)


def file_savelines(filename, strlist, append=False):
    mode = 'a' if append else 'w'
    text = '\n'.join(strlist)
    with open(filename, mode, encoding='utf-8') as f:
        f.write(text)


def file_savetext(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


def file_readtext(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def file_readlines(filename):
    if PYTHON_VERSION == 3:
        with open(filename, 'r', encoding='utf-8') as f:
            arr_strings = f.read().splitlines()
    else:
        import codecs
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            arr_strings = f.read().splitlines()
    return list_clean_empty_strs(arr_strings)


def file_readlines_in_list_interlines(filename):
    # r = [["line1", "line2"], ["line3", "line4"], ]
    listlines = file_readlines(filename)
    return read_list_interlines(listlines)


def read_list_interlines(listlines, strip_lines=False):
    # r = [["line1", "line2"], ["line3", "line4"], ]
    r = []
    i = 0
    while i <= len(listlines) - 1:
        if strip_lines:
            r.append([listlines[i].strip(), listlines[i + 1].strip()])
        else:
            r.append([listlines[i], listlines[i + 1]])
        i += 2
    return r


def json_store_to_file(filename, data):
    import json, io
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))


def json_data_from_file(filename):
    import json, io
    with io.open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def jsonlines_from_file(filename):
    """Чтение JSONlines (.jl) в список словарей"""
    import json
    lst = file_readlines(filename)
    d = [json.loads(i) for i in lst]
    return d


def json_element_of_listdicts_to_file(filename, dic, elem):
    """Запись элемента из списка словарей в json-файл"""
    list_elements = [i[elem] for i in dic]
    json_store_to_file(filename, list_elements)


def save_error_log(filename, text):
    import datetime
    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%Y %H:%M")
    file_savelines(filename, text, True)


def file_save(filepath, data):
    with open(filepath, 'wb') as f:
        f.write(data)


def pickle_store_to_file(filename, data):
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def pickle_data_from_file(filename):
    import pickle
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data


def csv_read(filename, csv_skip_firstline=False, return_dict=False):
    with open(filename, encoding='utf-8') as f:
        if return_dict:
            reader = csv.DictReader(f)
        else:
            reader = csv.reader(f)
        if csv_skip_firstline:
            next(reader)
        return tuple(row for row in reader)


def csv_read_dict(filename, delimiter=','):
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return tuple(row for row in reader)


def csv_save(path, list_str, delimiter=','):
    with open(path, "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f, delimiter)
        for row in list_str:
            writer.writerow(row)


def csv_save_dict(path, dic, fieldnames=None, delimiter=',', headers=True):
    """Writes a CSV file using DictWriter"""
    import csv
    if not fieldnames:
        fieldnames = dic[0].keys()
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=fieldnames)
        if headers:
            writer.writeheader()
        for row in dic:
            writer.writerow(row)


def csv_save_dict_fromListWithHeaders(path, data):
    """ ключи в первой строке списка"""
    # my_list = []
    fieldnames = data[0]
    # for values in data[1:]:
    # 	inner_dict = dict(zip(fieldnames, values))
    # 	my_list.append(inner_dict)
    inner_dic = (dict(zip(fieldnames, values)) for values in data[1:])
    csv_save_dict(path, inner_dic, fieldnames=data[0], headers=True)


def csv_split_to_files_per_line_count(file_in, rows_chunk_size: int):
    """ разбиение файла csv по числу строк, в новый файл.
    file_out_tpl - f-string
    При больших файлах занимает много памяти. Если надо, можно попробовать записывать части сразу, не храня.
    Или найти способ не загружать в память весь входной файл.
    Или грузить его как список, а не словарь, взяв заголовки из первой строки в список.

    на Doogle Drive в таблицах лимит 2.000.000 ячеек (делить на число столбцов). Может влезть больше если ячейки пустые
    https://support.google.com/drive/answer/37603?visit_id=636698732475200834-4208785419&rd=1
    на Excel лимит на листе 1 048 576 строк и 16 384 столбца
    https://support.office.com/en-us/article/1672b34d-7043-467e-8e27-269d656771c3
    """
    from vladi_helpers import split_list_per_line_count
    # from file_helpers import csv_read_dict, csv_save_dict
    lst = csv_read_dict(file_in)
    # save on split without store
    # for i in range(0, len(lst), rows_chunk_size):
    #     z = lst[i:i + chunk_size]
    #     csv_save_dict(f, z)
    splitted = split_list_per_line_count(lst, rows_chunk_size)
    for i, z in enumerate(splitted):
        # # path_sep = os.path.
        # fpath, _, fname = file_in.rpartition('/')
        # ffname, _, fext = fname.rpartition('.')
        # fname_new = f'{fpath}/{ffname}{i}.{fext}'
        i += 1
        f = f'/tmp/result{i}.csv'
        csv_save_dict(f, z)


# Excel ----------------
def get_rows_from_sheet(ws):
    rows_listdicts = []
    for row in ws.iter_rows(min_row=1, min_col=1, max_row=ws.max_row, max_col=ws.max_column):
        rows_listdicts.append([cell.value for cell in row])
    return rows_listdicts
