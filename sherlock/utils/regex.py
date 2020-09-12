import re

regex = {
    'page_id': re.compile(r".pageId = (?P<page>\d+);"),
    'user_id': re.compile(r".userInfo\((?P<user>\d+)\);"),
    'branch_id': re.compile(r".siteId = (?P<branch>\d+);"),
    'page_slug': re.compile(r".requestPageName = \"(?P<page>.+)\";"),
    'timestamp': re.compile(r"time_(?P<time>\d+) "),
    'user_slug': re.compile(r"user:info\/(?P<username>\S+)"),
    'scp_subtitle': re.compile(r"SCP-.+?-(?P<subtitle>.+)")
}
