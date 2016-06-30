# coding: utf-8
from gettext import gettext

def _(text, args=None):
    text = gettext(text)
    if args is not None:
        text %= args
    return text
