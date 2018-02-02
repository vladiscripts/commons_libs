#!/usr/bin/env python3
# -*- coding: utf-8  -*-#
# кроссплатформенное решение. возможны варианты с другими модулями, но их надо доустанавливать.
# http://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard-on-windows-using-python/3429034

from tkinter import Tk
import time

def CopyToClipboard(txt):
	r = Tk()
	r.withdraw()
	r.clipboard_clear()
	r.clipboard_append(txt)

	# protect from freeze
	r.update()
	time.sleep(.2)
	r.update()

	r.destroy()

def CopyFromClipboard():
	r = Tk()
	r.withdraw()
	s = r.clipboard_get()
	r.update()
	r.destroy()
	return s

txt = 'jkjkолодо'
CopyToClipboard(txt)
print (CopyFromClipboard())
