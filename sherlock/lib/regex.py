import re

regex = {
    'page_id': re.compile(r".pageId = (?P<page_id>\d+);"),
    'user_id': re.compile(r".userInfo\((?P<user_id>\d+)\);"),
    'site_id': re.compile(r".siteId = (?P<site>\d+);"),
    'page_slug': re.compile(r".requestPageName = \"(?P<slug>.+)\";"),
    'timestamp': re.compile(r"time_(?P<time>\d+) "),
    'user_slug': re.compile(r"user:info\/(?P<username>\S+)"),
    'scp_title': re.compile(r"SCP-(.*) ?-")
}
