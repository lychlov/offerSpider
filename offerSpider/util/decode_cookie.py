# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     decode_cookie
   Description :
   Author :       Lychlov
   date：          2018/9/23
-------------------------------------------------
   Change Activity:
                   2018/9/23:
-------------------------------------------------
"""
import base64
import js2py


def get_cookies(crypto):
    cookies = {}
    decypt = base64.b64decode(crypto).decode()
    decypt = decypt.replace('document.', '').replace(' location.reload();', '')
    js_deal = js2py.eval_js(decypt)
    for pair in js_deal.split(';'):
        cookies[pair.split('=')[0]] = pair.split('=')[1]
    return cookies
