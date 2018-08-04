# -*- coding: utf-8  -*-
#
# author: https://github.com/vladiscripts
#
import re
import mwparserfromhell


def listtpls(wikicode, tplname):
    return [tpl for tpl in wikicode.filter_templates() if tpl.name.matches(tplname)]


def tpl_add_param(tpl, param, value):
    if not param in tpl:
        tpl.add(param, value)


def removeTplParameters(tpl, keys):
    # if type(keys) == str: keys = (keys,)
    for k in keys:
        if tpl.has(k): tpl.remove(k)


def remove_parameters(wikicode, tplname, keys):
    for tpl in listtpls(wikicode, tplname):
        for k in keys:
            if tpl.has(k): tpl.remove(k)
    return wikicode


def parametersNamesList(tpl):
    return [p.name.strip() for p in tpl.params]


def parametersValuesList(tpl):
    return [p.value.strip() for p in tpl.params]


def removeTplParametersExceptThis(tpl, keys):
    pnamelist = parametersNamesList(tpl)
    toRemoveList = [p for p in pnamelist if p not in keys]
    removeTplParameters(tpl, toRemoveList)


def renameParam(tpl, name, newname):
    if tpl.has(name):
        tpl.get(name).name = newname


def renameTemlate(tpl, newname):
    tpl.name = newname


def isTplInPage(wikicode, tplname):
    for tpl in wikicode.filter_templates():
        if tpl.name.matches(tplname):
            return True


def delete_tpl(wikicode, tplname):
    for tpl in wikicode.filter_templates():
        if tpl.name.matches(tplname):
            wikicode.remove(tpl)


def findLink(tpl, link2remove, linkparameters=('',)):
    linkparameters = ('ссылка', 'url', 'часть', 'ссылка часть', 'часть ссылка') + linkparameters
    # print (linkparameters)
    for p in linkparameters:
        if not tpl.has(p): continue
        s = str(tpl.get(p).value)
        if re.search(link2remove, s):
            return True


def findAndDeleteLink(tpl, link2remove, linkparameters=('',)):
    linkparameters = ('ссылка', 'url', 'ссылка часть', 'часть ссылка') + linkparameters
    # print (linkparameters)
    for p in linkparameters:
        if not tpl.has(p): continue
        s = str(tpl.get(p).value)
        if re.search(link2remove, s):
            tpl.remove(p, True)
            return True


def deleteParamArhiveurlDateIfWebarchive(tpl):
    l = 'web.archive.org'
    p = 'archiveurl'
    if not tpl.has(p): return
    s = str(tpl.get(p).value)
    if re.search(l, s):
        removeTplParameters(tpl, ('archiveurl', 'archivedate'))


# Конвертация ссылки типа '[https?://url title]' в шаблон. reRemoveFromTitles - список литералов-регэкспов для вычистки из заголовка.
def link2template(code, regexpSearchLink, newTplName, TplUrlParameter, TplLinktitleParameter, reRemoveFromTitles,
                  rePageTitleFromLink):
    # code = mwparserfromhell.parse(text)
    reLink = re.compile(regexpSearchLink)
    for link in code.filter_external_links():
        if not reLink.search(str(link.url)): continue
        tpl = mwparserfromhell.nodes.template.Template(newTplName)
        tpl.add(TplUrlParameter, link.url)
        if reRemoveFromTitles:
            for r in reRemoveFromTitles:
                link.title = re.sub(r, '', str(link.title))
        t = str(link.title)
        if t and not re.match('^\s*$', t):
            t = t.strip()
            tpl.add(TplLinktitleParameter, t)
        else:
            paramValueFromLinkOrPagename(tpl, TplLinktitleParameter, TplUrlParameter, rePageTitleFromLink)
        findAndDeleteLink(tpl, regexpSearchLink)
        deleteEmptyParam(tpl, (TplUrlParameter,))
        # else: print('hh')
        # newstr = '{{' + newTplName + '|' + TplUrlParameter + '=' + str(link.url) + '|name=' + str(link.title) + '}}'
        code.replace(link, str(tpl))


# print(str(tpl))
# return str(code)


def paramValueFromLinkOrPagename(tpl, paramtitle, paramlink, rePageTitleFromLink):
    title = getPagenameFromLink(tpl, paramlink, rePageTitleFromLink)
    if not title: return
    tpl.add(paramtitle, title)


def getPagenameFromLink(tpl, paramlink, reTitleFromLink):
    paramlinks = ('ссылка', 'url', 'ссылка часть', paramlink)
    for plink in paramlinks:
        if tpl.has(plink):
            import urllib.request
            url = str(tpl.get(plink).value)
            titleFromLink = pagenameFromUrl(reTitleFromLink, url)
            if titleFromLink is None: return ''
            urldecodedTitleFromLink = urllib.request.unquote(titleFromLink)
            return urldecodedTitleFromLink


def deleteEmptyParam(tpl, keys):
    for k in keys:
        if tpl.has(k) and re.match('^\s*$', str(tpl.get(
                k).value)):  # and re.match('^(?:\s*|БСЭ|Большая советская энциклопедия)$', str(tpl.get(k).value)):
            tpl.remove(k)


def removeSpacesBreaks(tpl):
    # удаление лишних пробелов
    p = tpl.params

    reBr = re.compile(r'\n *')
    reSp = re.compile(' {2,}')
    for i in range(len(p)):
        s = str(p[i])
        s = reBr.sub('', s)
        s = reSp.sub(' ', s)
        p[i] = s


def replaceParamValue(tpl, parameter, rePattern, repl):
    if tpl.has(parameter):
        s = str(tpl.get(parameter).value)
        tpl.get(parameter).value = re.sub(rePattern, repl, s)


def paramIsEmpty(tpl, parameter):
    if re.match('^\s*$', str(tpl.get(parameter).value)):
        return True


def pagenameFromUrl(regexp, url):
    title = re.findall(regexp, url)
    if title:
        title = title[0]
        if not re.match('^[\d\s]+$', title): return title


def parse_tagpages(tag):
    # section
    from collections import namedtuple
    tagPages = {
        'index': tag.get('index').value,
        'from': tag.get('from').value,
        'to': tag.get('to').value,
        'onlysection': tag.get('onlysection').value,
        'fromsection': tag.get('fromsection').value,
        'tosection': tag.get('tosection').value
    }
    return namedtuple('Parts', tagPages.keys())(**tagPages)


# если в "часть=" ссылка, то разделить на заглавие в "часть=" и ссылку в "ссылка часть="
def separateLinkFromPartParameter(tpl):
    part = 'часть'
    link = 'ссылка часть'
    regexp = r'\[(http[^]\s]+)\s+(.+?)\]'
    if tpl.has(part):
        s = str(tpl.get(part).value)
        n = re.findall(regexp, s)
        if n:
            tpl.add(link, n[0][0])
            tpl.get(part).value = n[0][1]


# ---------


def getparameters_aliases(tpl, list_parameters_to_search):
    for p in list_parameters_to_search:
        if tpl.has(p):
            return tpl.get(p).value
