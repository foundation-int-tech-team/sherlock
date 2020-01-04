# -*- coding: utf-8 -*-
import re

regex = {
    'page_id': re.compile(r".pageId = (?P<page_id>\d+);"),
    'user_id': re.compile(r".userInfo\((?P<user_id>\d+)\);"),
    'site': re.compile(r".siteUnixName = \"(?P<site>.+)\";"),
    'slug': re.compile(r".requestPageName = \"(?P<slug>.+)\";"),
    'timestamp': re.compile(r"time_(?P<time>\d+) "),
    'username': re.compile(r"user:info\/(?P<username>\S+)")
}
