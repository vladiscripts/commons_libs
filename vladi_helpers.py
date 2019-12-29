# author: https://github.com/vladiscripts
#
# Библиотека общих функций
#
# from sys import version_info
# PYTHON_VERSION = version_info.major
import os
import re
from urllib.parse import urlsplit, urlparse, parse_qs, parse_qsl, unquote, quote, quote_plus, urljoin, urlencode, \
    urldefrag, urlunsplit


def get_item_from_listdict(listdicts, key, value):
    for d in listdicts:
        if key in d and d[key] == value:
            return d


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


def listdict_of_uniques(listdict, key: str):
    """чистка списка словарей от дубликатов, по ключу"""
    uniques = set()
    r = []
    for d in listdict:
        k = d[key]
        if k not in uniques:
            r.append(d)
            uniques.add(k)
    return r


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


def pop_list_by_value(lst, value):
    """pop из списка по значению ключа"""
    for i, k in enumerate(lst):
        if k == value:
            lst.pop(i)


def sort_list_of_dict(list_to_sort, key):
    return sorted(list_to_sort, key=lambda k: k[key])


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
    return [l.strip() for l in lst if l.strip() != '']


def join_and_strip(lststr, skip_empty_str=False, sep=''):
    """join() списка, со strip() его элементов - чисткой пробелов, и пустых строк"""
    striped = striplist(lststr, skip_empty_str=skip_empty_str)
    s = sep.join(striped).replace('  ', ' ').strip()
    return s


def striplist(lststr, skip_empty_str=False):
    """strip() значений списка"""
    if skip_empty_str:
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


# def repl(m):
#     """regex замена, с inline модификацией"""
#     n = int(m.group(2))
#     i = 1
#     if n >= 127 and n <= 179: i = 2
#     return n + i
# ss = re.sub(r(a string)(\d+)', lambda m: f'{m.group(1)}{repl(m)}{m.group(3)}', t)


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


def split_list_per_line_count(lst, rows_chunk_size: int):
    """Разделение списка на части по числу строк."""
    return [lst[i:i + rows_chunk_size] for i in range(0, len(lst), rows_chunk_size)]


def find_str_in_el_of_list_and_select(lst, search_str):
    """Ищет подстроку в строковых элементах списка, и возвращает найденный элемент."""
    # return [s for s in lst if type(s) == str and s.find(search_str) >= 0][0]
    for s in lst:
        if isinstance(s, str) and search_str in s:
            return s


def json_like_to_dict(text):
    """Пример парсера json-like строк из js-скриптов в словарь Python"""
    re_j = re.compile(r"aScriptName\s*=\s*\{(.*?)\}", flags=re.S)
    re_b = re.compile(r"(^|,)(\s*[^\s]+\s*:)", flags=re.S)  # разделитель параметров [,], значений [:]
    # json.loads не работает, значения не обернуты в кавычки
    # json.loads(re.sub("(^|,)(\s*[^\s]+\s*:\s*)'(.*?)'", r'\1\2"\3"', j.group(1).replace('\n', ''), flags=re.S))
    j = re_j.search(text)
    d = {}
    if j:
        params = re_b.sub(r'%#%\2', j.group(1)).split('%#%')  # split параметров, с уст. временн. разделителя
        for p in params:
            if p.strip() != '':
                k, _, v = p.partition(':')
                key = k.strip().strip("'")
                value = v.strip().strip("'")
                d[key] = value


class Dict2class(object):
    """Загружает словарь в атрибуты класса
    https://stackoverflow.com/questions/1639174/creating-class-instance-properties-from-a-dictionary/1639249
    Инициализация:
    instance = dict2class(dictionary)
    instance.field
    """

    # def __init__(self, **dictionary):
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)
        # альтернатива
        # for k, v in dictionary.items():
        #     setattr(self, k, v)


class Dictprop(dict):
    """Дополняет атрибуты словаря, использованием как свойствами класса, для более удобного обращения к ним.
    https://stackoverflow.com/questions/1639174/creating-class-instance-properties-from-a-dictionary/1639249
    Инициализация:
    instance = dictprop(dictionary)
    instance.field
    """

    def __init__(self, dictionary):
        super().__init__()
        self.__dict__.update(dictionary)

    def __getattr__(self, name):
        return self[name]


class Row(dict):
    """Словарь с точечной нотацией как у класса, и с определёнными атрибутами"""
    __dict__ = 'pid', 'title', 'seller', 'seller_rating', 'seller_reviews', 'category_slug'

    def __setattr__(self, key, value):
        self.__setitem__(key, value)


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


def benchmark(func):
    # декоратор @benchmark
    # считает скорость выполнения функции
    import time

    def wrapper(*kargs, **kwargs):
        start = time.time()
        return_value = func(*kargs, **kwargs)
        end = time.time()
        print(f'[*] Время выполнения: {end - start} секунд.')
        return return_value

    return wrapper


def chunks(lst, count):
    # """Разделить список на число частей."""
    # start = 0
    # for i in range(count):
    #     stop = start + len(lst[i::count])
    #     yield lst[start:stop]
    #     start = stop

    for i in range(0, len(lst), count):
        yield lst[i:i + count]


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
    lst = urllib.parse.parse_qsl(url, keep_blank_values=True)
    # d = dict(p.split('=') for p in s.split('&'))
    return lst


def change_url_param(url, param, newvalue):
    parsed = urlsplit(url)
    query_dict = parse_qs(parsed.query)
    query_dict[param][0] = newvalue
    parsed = parsed._replace(query=urlencode(query_dict, doseq=True))  # path=self.split.path + endpoint,
    url_new = urlunsplit(parsed)
    # url_new = parsed.geturl()
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


# HTML -----------------
# Selenium
def set_attr_selenium(driver, element, ename, value):
    driver.execute_script(f"arguments[0].setAttribute('{ename}','{value}')", element)


def del_attr_selenium(driver, element, ename):
    driver.execute_script(f"arguments[0].removeAttribute('{ename}')", element)


def split_urlfile(url, normalize=True):
    urlparsed = urlparse(url)
    path = urlparsed.path.rpartition('/')[0]
    filename = urlparsed.path.rpartition('/')[2]
    if normalize:
        path, filename = os.path.normpath(path), os.path.normpath(filename)
    return path, filename, urlparsed


def cut_string_with_return_sep(string, sep_string):
    return string.partition(sep_string)[0] + sep_string


# lxml
def remove_empty_tags(tree, convert_to_str: bool = False, tags_ignore: list = None):
    '''Уборка пустых тегов'''
    from lxml.html import fromstring, tostring
    # tags_ignore = ['br', 'img', 'a']

    def recursively_empty(e):
        if tags_ignore and e.tag in tags_ignore \
                or e.text:
            return False
        return all((recursively_empty(c) for c in e.iterchildren()))

    for e in tree:
        if recursively_empty(e):
            parent = e.getparent()
            parent.remove(e)

    if convert_to_str:
        return tostring(tree, encoding='unicode')
    return tree


# Pandas
def parse_pandas(filename=None, fcontent=None):
    import pandas as pd
    import io
    if filename:
        df = pd.read_excel(filename, sheet_name=1, skiprows=[0], header=0)
    elif fcontent:
        df = pd.read_excel(io.BytesIO(fcontent), engine='xlrd', sheet_name=1, skiprows=[0], header=0)
    else:
        exit()
    # df = df.rename(columns={df.columns[0]: 'date'})


def make_dataframe_csv(self, zip_path=None, zip_content=None, csv_path=None, csv_content=None):
    import pandas as pd
    import io
    import logging
    self.df = None
    if zip_path:
        self.df = pd.read_csv(zip_path, compression='zip', sep=',', header=0)
    elif zip_content:
        self.df = pd.read_csv(io.BytesIO(zip_content), compression='zip', sep=',', header=0)
    elif csv_path:
        self.df = pd.read_csv(csv_path)
    elif csv_content:
        self.df = pd.read_csv(io.BytesIO(csv_content), sep=',', header=0)
    else:
        logging.error('No specified the input csv')
        exit()
