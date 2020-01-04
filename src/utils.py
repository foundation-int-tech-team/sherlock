# -*- coding: utf-8 -*-
import random
import re
import string
from datetime import datetime
from posixpath import join

import scrapy


def wikidot(site=None, component=None):
    """Build Wikidot API URL for specific wiki"""
    site = site if site else 'scp-wiki'
    url = 'http://{}.wikidot.com/'.format(site)

    if component:
        url = join(url, component)

    return url


def request(module: str, **kwargs):
    """Format cookies and data to make a request to the Wikidot API"""
    token = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=6))
    cookies = {'wikidot_token7': token}
    formdata = {
        'callbackIndex': '1',
        'wikidot_token7': token,
        'moduleName': module,
        **dict([a, str(x)] for a, x in kwargs.items())
    }
    return formdata, cookies


def time_to_iso(timestamp):
    """Timestamp date to ISO format"""
    return datetime.utcfromtimestamp(int(timestamp)).isoformat()


def memoize(f):
    """Memoize"""
    memo = {}

    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper
