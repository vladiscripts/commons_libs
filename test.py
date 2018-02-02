# marker_page_start = '{{-start-}}'
# marker_page_end = '{{-end-}}'
# header = """
# Список статей, с перечнями их сносок, в которых указаны некорректные викиссылки.
#
# Элементы списка автоподставляются в перечисленных статьях в шаблон {{t|Нет полных библиографических описаний}}.
# (Это служебная таблица даных для подстановок, поэтому с этой страницы ссылки на сноски не работают.)
#
# Список обновляется ботом.
#
# """  # в шапку шаблон {{координационный список}} не нужен, ибо это не список, а подстраница данных скрипта
# bottom = '[[Категория:Википедия:Подстраницы шаблонов]][[Категория:Шаблоны:Подстраницы Нет полных библиографических описаний|{{SUBPAGENAME}}]]'
# pagename = 'lllllllll'
# wikilist_refs_entries = 'kjkkkkkk\n\hhhhhhhh\mnnn\nhhhhhhhhhhhhhh'
#
#
# wikilist = "{start}\n'''{pagename}'''\n{header}\n{refs_entries}\n{footer}\n{end}\n\n".format(
# 		start=marker_page_start, end=marker_page_end,
# 		pagename=pagename, header=header, footer=bottom,
# 		refs_entries=wikilist_refs_entries)
# print(wikilist)
#
#
# wikilist = marker_page_start \
# 						   + "\n'''" + pagename + "'''\n" \
# 						   + header \
# 						   + '\n' + wikilist_refs_entries \
# 						   + "\n" + bottom \
# 						   + "\n" + marker_page_end + "\n\n"
# print(wikilist)

k = None
u = lambda k: k
print (lambda k: k)
p = [
	(lambda k: '-simulate' if k else '')(k),
]
print(p)

# from wikiapi import wdb_query  # contents parameters: api_user, api_pw, wdb_user, wdb_pw
# sql = """SELECT page_title
# 		FROM page
# 		JOIN templatelinks ON tl_from = page_id
# 			WHERE tl_namespace = 10
# 			AND tl_title = '%s'
# 			AND page_namespace = 0""" % 'Любкер'
# print(wdb_query(sql))
