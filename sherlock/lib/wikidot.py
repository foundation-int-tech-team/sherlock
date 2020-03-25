import posixpath
import random
import string
from datetime import datetime


class Wikidot:
    """Wikidot utility"""

    @staticmethod
    def path(site=None, component=None):
        """Build Wikidot URL for specific wiki"""

        site = site if site else 'scp-wiki'
        url = f'http://{site}.wikidot.com/'

        if component:
            url = posixpath.join(url, component)

        return url

    @staticmethod
    def request(module: str, **kwargs):
        """Format cookies and data to make a request to the Wikidot API"""

        token = ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=6)
        )
        cookies = {'wikidot_token7': token}
        formdata = {
            'callbackIndex': '1',
            'wikidot_token7': token,
            'moduleName': module,
            **dict([a, str(x)] for a, x in kwargs.items())
        }

        return formdata, cookies

    @staticmethod
    def time_to_iso(timestamp):
        """Timestamp date to ISO format"""

        return datetime.utcfromtimestamp(int(timestamp)).isoformat()

    @staticmethod
    def compute_vote(votes, without="0"):
        i = 0
        for (user, vote) in votes.items():
            if user == without:
                continue

            if vote == '+':
                i += 1
            elif vote == '-':
                i -= 1

        return i
