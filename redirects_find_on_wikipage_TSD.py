#!/usr/bin/env python
# coding: utf-8
import requests
from urllib.parse import urlencode, quote
# from vladi_commons import vladi_commons
# from vladi_commons.vladi_commons import csv_save_dict_fromListWithHeaders, json_store_to_file, json_data_from_file
import sqlite3
import json
from lxml.html import fromstring
from urllib.parse import urlparse, parse_qs, parse_qsl, unquote, quote
# t = fromstring(r.text)
# urldecode = urllib.parse.unquote(url)

def open_reqsession():
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0',
		# 'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
		# 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/61.0.3163.79 Chrome/61.0.3163.79 Safari/537.36',
		# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		# 'Accept': 'application/json, text/javascript, */*; q=0.01'
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
		# 'Content-Type': 'x-www-form-urlencoded',
		'Content-Type': 'text/plain;charset=UTF-8',
		# 'Host': 'www.site.ru',
		# 'Referer': 'http://www.site.ru/index.html',	    
	}
	proxyDict = {
		"http": 'http://212.161.91.178:65103',
		"https": 'https://212.161.91.178:65103',
		# "http": 'http://92.27.91.253:53281',
		# "https": 'https://92.27.91.253:53281',
		# "ftp"   : ftp_proxy
	}
	s = requests.Session()
	s.headers = headers
	s.proxies.update(proxyDict)
	return s


open_reqsession()

# d = {
# 	"p": "arg",
# }
# r = s.post(url_login, params=login_params, json=d, )
# params = {
# 	"p": "arg",
# }
# r = s.get(url_login, params=login_params)
#
# url =
#
# r = s.get(url)
# # r.text
# urldecode = urllib.parse.unquote(url)
# # r.json()
# #     if r.status_code != 200:
# #         print("r.status_code != 200")
# #     if len(r.json()['GetResultListResult']) < 1:
# #         print("len(r.json()['GetResultListResult']) < 1")



t = """
<li><a href="/wiki/%D0%A2%D0%A1%D0%942/%D0%90%D0%B1%D0%BE/%D0%94%D0%9E" title="ТСД2/Або/ДО">Або</a>&#160;/&#160;<a href="/wiki/%D0%A2%D0%A1%D0%942/%D0%90%D0%B1%D0%BE" class="mw-redirect" title="ТСД2/Або">Або</a></li>
"""

prefix = 'ТСД2'
hxs = fromstring(t)
articles_e = hxs.cssselect('.mw-content-text ol li')

for article_e in articles_e:
	for a in article_e:
		title = a.get('title')
		if not title or not str(title.startswith(prefix)):
			continue
		# href = a.get('href')
		if a.cssselect('[class~=mw-redirect]'):
			title = a.get('title')


	tag_attrs = e.items()
	a = e.get('attribute')
	el_text = a.text



def string_strip(s):
	return str(s).replace('\u200e', '').replace('&lrm;', '').replace('&#8206;', '').strip()