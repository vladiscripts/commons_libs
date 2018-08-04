#!/usr/bin/env python3
# -*- coding: utf-8  -*-#
# author: https://github.com/vladiscripts
#
# Библиотека общих функций
#
from sys import version_info

PYTHON_VERSION = version_info.major
if PYTHON_VERSION == 3:
    from urllib.parse import urlsplit, parse_qs, parse_qsl, unquote, quote, urljoin, urlencode, quote_plus, urldefrag
else:
    from urllib import urlencode, quote  # python 2.7
from lxml.html import fromstring
import re
# import html5lib
from urllib.parse import urlparse, parse_qs, parse_qsl, unquote, quote


# import codecs

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


def join_and_strip(lststr, skipemptystr=False, sep=''):
    """join() списка, со strip() его элементов - чисткой пробелов, и пустых строк"""
    return sep.join(self.striplist(lststr, skipemptystr=skipemptystr)).replace('  ', ' ').strip()


def striplist(lststr, skipemptystr=False):
    """strip() значений списка"""
    if skipemptystr:
        r = [s.strip() for s in lststr if s.strip()]
    else:
        r = [s.strip() for s in lststr]
    return r


def regex(regex, text):
    """возвращает найденный regex group(1), иначе пустую строку"""
    if regex:
        s = re.search(regex, text)
        r = s.group(1) if s else ''
        return r


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
