#!/usr/bin/env python3
# -*- coding: utf-8  -*-#
# author: https://github.com/vladiscripts
#
# Библиотека общих функций:
# работа с файлами в utf-8
#
from sys import version_info

PYTHON_VERSION = version_info.major
if PYTHON_VERSION == 3:
    from urllib.parse import urlsplit, parse_qs, parse_qsl, unquote, quote, urljoin, urlencode, quote_plus, urldefrag
else:
    from urllib import urlencode, quote  # python 2.7


# import codecs


# ----------

def filepaths_of_directory(directory, filename_ext):
    # filename_ext = '.xlsx'
    filenames = filter(lambda x: x.endswith(filename_ext), os.listdir(directory))
    full_files_paths = [os.path.join(DIRECTORY, filename) for filename in filenames]
    return full_files_paths


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
    import csv
    with open(filename) as f:
        if return_dict:
            reader = csv.DictReader(f)
        else:
            reader = csv.reader(f)
        if csv_skip_firstline:
            next(reader)
        return tuple(row for row in reader)


def csv_read_dict(filename, delimiter=','):
    import csv
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return tuple(row for row in reader)


def csv_save(path, list_str, delimiter=','):
    import csv
    with open(path, "w", newline="") as f:
        writer = csv.writer(f, delimiter)
        for row in list_str:
            writer.writerow(row)


def csv_save_dict(path, dic, fieldnames=None, delimiter=',', headers=True):
    """Writes a CSV file using DictWriter"""
    import csv
    if not fieldnames:
        fieldnames = dic[0].keys()
    with open(path, "w", newline='') as f:
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


def remove_empty_lines(lst):
    """чистка от пустых строк"""
    return [x for x in lst if x]


def delete_element_in_dictlist(dic, key):
    """Удалить ключ из списка словарей"""
    for i in dic:
        if key in i:
            del i[key]


def rename_key_in_listdict(dic, key_old, key_new, value_if_none=None):
    for i in dic:
        i[key_new] = i.get(key_old, value_if_none)
        if key_old in i:
            del i[key_old]


def list_of_uniques(lst):
    """чистка списка от дубликатов"""
    o = []
    for i in lst:
        if i not in o:
            o.append(i)
    return o


def listdic_pop(lst, key, val, ignorecase=False):
    """pop из списка словарей по значению ключа"""
    i = None
    for d in lst:
        if ignorecase:
            if d[key].lower() == val.lower():
                i = lst.index(d)
                break
        else:
            if d[key] == val:
                i = lst.index(d)
                break
    if i:
        return lst.pop(i)


def sort_list_of_dict(list_to_be_sorted, key):
    return sorted(list_to_be_sorted, key=lambda k: k[key])


def type_str2list(string):
    """Строку в список"""
    return [string] if isinstance(string, str) else string


def str2list(string):
    return list_clean_empty_strs(string.splitlines())


def list_clean_empty_strs(lst):
    """Чистка пустых строк в списке"""
    # Тестировано: import timeit; timeit.timeit(test_func, number=10000)
    # return [p.strip() for p in lst.splitlines() if p.strip() != '']
    # return [lst.remove(v) for v in lst if v == '' and v.isspace()]
    # return [v.strip() for v in lst if not v.isspace() and v != '']

    # filter(lambda x: x.strip() != '', k)
    return [p.strip() for p in lst if p.strip() != '']


def list2str_qouted(delimiter, list_str, normalizations=False):
    from wikiapi import normalization_pagename
    if normalizations:
        return delimiter.join(['"' + normalization_pagename(s) + '"' for s in list_str])
    else:
        return delimiter.join(['"' + s + '"' for s in list_str])


def lines2list(text):
    return list_clean_empty_strs(text.splitlines())


def lines_two_elements2list(text):
    """like:
    email@gmail.com ; password
    6666;3dg """
    text = [p.partition(';')[0::2] for p in text.splitlines()]
    return [[s[0].strip(), s[1].strip()] for s in text if s[0].strip() != '']


def split_list_per_line_count(lst, chunk_size):
    """Разделение списка на части по числу строк."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def find_str_in_el_of_list_and_select(lst, search_str):
    """Ищет подстроку в строковых элементах списка, и возвращает найденный элемент."""
    # return [s for s in lst if type(s) == str and s.find(search_str) >= 0][0]
    for s in lst:
        if isinstance(s, str) and search_str in s:
            return s


class Dict2class(object):
    """Преобразует атрибутов словаря в своства класса, для более удобного обращения к ним.
    https://stackoverflow.com/questions/1639174/creating-class-instance-properties-from-a-dictionary/1639249
    Инициализация:
    instance = dict2class(dictionary)
    instance.field
    """

    def __init__(self, dictionary):
        self.__dict__.update(dictionary)


class Dictprop(dict):
    """Дополняет атрибуты словаря, использованием как свойствами класса, для более удобного обращения к ним.
    https://stackoverflow.com/questions/1639174/creating-class-instance-properties-from-a-dictionary/1639249
    Инициализация:
    instance = dictprop(dictionary)
    instance.field
    """

    def __getattr__(self, name):
        return self[name]


def re_compile_list(re_groups):
    """Регулярные выражения: компиляция по списку.

    Список типа: letter_groups = ['[АБВГДЕЁЖЗ]', '[ИКЛМНО]', '[ПH]', '[СТУФХЦЧШЩЪЫЬЭЮЯ]', r'[.]']
    """
    import re
    groups = []
    for g in re_groups:
        c = re.compile(g, re.I + re.U)
        groups.append(c)
    return groups


def re_compile_dict(re_groups, flags=False):
    """Регулярные выражения: компиляция по словарю.

    Принимает словарь типа:
    {'АБВГДЕЁЖЗ': '[АБВГДЕЁЖЗ]', 'other': r'.'}

    Возващает типа:
        groups = [
        {'name': 'АБВГДЕЁЖЗ', 're': '[АБВГДЕЁЖЗ]', 'c': re.compiled},
        {'name': 'other', 're': r'.', 'c': re.compiled},
    ]
    """
    import re
    flags = re.I + re.U if not flags else flags
    groups = []
    for g in re_groups:
        string = {}
        string['name'] = g
        string['re'] = re_groups[g]
        string['c'] = re.compile(re_groups[g], flags)
        groups.append(string)
    return groups


def byte2utf(string):
    import urllib.parse
    string = urllib.parse.quote_from_bytes(string)
    string = urllib.parse.unquote(string, encoding='utf8')
    return string


# Wiki ---

def label_interpages(number, string_chet, str_nechet):
    # возвращает строку в зависимости чётная ли страница
    return str(string_chet) if not int(number) % 2 else str(str_nechet)


def wiki_colontitul(c1='', c2='', c3=''):
    return '{{колонтитул|%s|%s|%s}}' % (c1, c2, c3)


# Internet ---
def send_email_toollabs(subject, text, email='tools.vltools@tools.wmflabs.org'):
    # Не работает из скрипа, из консоли - да
    # https://wikitech.wikimedia.org/wiki/Help:Tool_Labs#Mail_from_tools
    #
    import subprocess
    cmd = 'echo -e "Subject: ' + subject + r'\n\n' + text + '" | /usr/sbin/exim -odf -i ' + email
    subprocess.call(cmd, shell=True)


def url_params_str_to_dict(url, unquote=True):
    """Парсинг параметров url: str > dict.
    ! Одинакоые ключи затираются. Использовать url_params_str_to_list() на основе urllib.parse.parse_qsl() !
    unquote: декодировать percent-encoded символы строки"""
    import urllib.parse
    if unquote:
        url = urllib.parse.unquote(url)
    d = urllib.parse.parse_qs(url, keep_blank_values=True)
    return {k: v[0] for k, v in d.items()}


def url_params_str_to_list(url, unquote=True):
    """Парсинг параметров url: str > dict.
    unquote: декодировать percent-encoded символы строки"""
    import urllib.parse
    if unquote:
        url = urllib.parse.unquote(url)
    d = urllib.parse.parse_qsl(url, keep_blank_values=True)
    return {k: v[0] for k, v in d.items()}


def change_url_param(url, param, newvalue):
    parsed = urlsplit(url)
    query_dict = parse_qs(parsed.query)
    query_dict[param][0] = newvalue
    query_new = urlencode(query_dict, doseq=True)
    parsed = parsed._replace(query=query_new)
    url_new = parsed.geturl()
    return url_new


# def replace_element_to_text(etree_, elem, textnew):
# """!удаляет текст элементов"""
# 	"""lxml: замена элемента на текст"""
# 	from lxml import etree
# 	for r in etree_.cssselect(elem):
# 		r.tail = textnew + r.tail if r.tail else textnew
# 	etree.strip_elements(etree_, elem, with_tail=False)

# def replace_element_to_text(etree_, elem, textnew):
# """html-теги: замена элемента на текст"""
# 	from lxml.html import fromstring, tostring
# 	import re
# 	# w = fromstring('<h1><strong>ДЕТСТВО</strong> <strong>——</strong> <strong>ЮНОШЕСКИЕ</strong> <strong>ОПЫТЫ</strong></h1>')
# 	# e = 'strong'
# 	# textnew = "''"
# 	x = tostring(etree_, encoding='unicode')
# 	v = re.sub('<{elem}[^>]*>(.*?)</{elem}>'.format(elem=elem), textnew + r'\1' + textnew, x, flags=re.DOTALL)
# 	return fromstring(v)


# alpha version ---
def ssh_connect(host, user, passw, port=22):
    import paramiko
    # host = 'tools-login.wmflabs.org'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=user, password=passw, port=port)
    stdin, stdout, stderr = ssh.exec_command('ls -l')
    data = stdout.read() + stderr.read()
    ssh.close()
    #
    print(str(data))


# ---------------- Excel
def get_rows_from_sheet(ws):
    rows_listdicts = []
    for row in ws.iter_rows(min_row=1, min_col=1, max_row=ws.max_row, max_col=ws.max_column):
        rows_listdicts.append([cell.value for cell in row])
    return rows_listdicts
