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
	from urllib.parse import urlencode, quote  # python 3
else:
	from urllib import urlencode, quote  # python 2.7
# import codecs


# ----------


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

	# чистка пустых строк
	for v in arr_strings:
		if v.isspace() or v == '':
			arr_strings.remove(v)
	return arr_strings


def file_readlines_in_list_interlines(filename):
	r = [
		# ["line1", "line2"],
		# ["line3", "line4"],
	]
	listlines = file_readlines(filename)
	i = 0
	while i <= len(listlines) - 1:
		r.append([listlines[i], listlines[i + 1]])
		i += 2
	return r


def json_store_to_file(filename, data):
	import json
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))
	pass


def json_data_from_file(filename):
	import json
	with open(filename, 'r', encoding='utf-8') as f:
		data = json.load(f)
	return data


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


def read_csv(csv_filename_wordlists, csv_colnum, csv_skip_firstline):
	import csv
	with open(csv_filename_wordlists) as csvfile:
		reader = csv.reader(csvfile)  # reader = csv.DictReader(csvfile)
		if csv_skip_firstline: next(reader)
		return [row[csv_colnum] for row in reader]


def str2list(string):
	"""Строку в список"""
	return [string] if isinstance(string, str) else string


def list2str_qouted(delimiter, list_str, normalizations=False):
	from wikiapi import normalization_pagename
	if normalizations:
		return delimiter.join(['"' + normalization_pagename(s) + '"' for s in list_str])
	else:
		return delimiter.join(['"' + s + '"' for s in list_str])


def split_list_per_line_count(lst, chunk_size):
	"""Разделение списка на части по числу строк."""
	return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


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


def label_interpages(number, string_chet, str_nechet):
	# возвращает строку в зависимости чётная ли страница
	return str(string_chet) if not int(number) % 2 else str(str_nechet)


def wiki_colontitul(c1='', c2='', c3=''):
	return '{{колонтитул|%s|%s|%s}}' % (c1, c2, c3)


# ---
def send_email_toollabs(subject, text, email='tools.vltools@tools.wmflabs.org'):
	# Не работает из скрипа, из консоли - да
	# https://wikitech.wikimedia.org/wiki/Help:Tool_Labs#Mail_from_tools
	#
	import subprocess
	cmd = 'echo -e "Subject: ' + subject + r'\n\n' + text + '" | /usr/sbin/exim -odf -i ' + email
	subprocess.call(cmd, shell=True)


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
