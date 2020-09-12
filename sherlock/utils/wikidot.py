import random
import string
from datetime import datetime
from posixpath import join
from unicodedata import normalize

from nltk import data, tokenize
from w3lib.html import remove_tags, remove_tags_with_content

data.path.append('./data/nltk_data')


def path(site=None, component=None):
    """Build Wikidot URL for a specific wiki"""

    url = f'http://{site}.wikidot.com/'

    if component:
        url = join(url, component)

    return url


def request(module: str, **kwargs):
    """Format cookies and data to make a request to the Wikidot API"""

    token = ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=6)
    )
    cookies = {'wikidot_token7': token}
    data = {
        'callbackIndex': '1',
        'wikidot_token7': token,
        'moduleName': module,
        **dict([a, str(x)] for a, x in kwargs.items())
    }

    return data, cookies


def time_to_iso(timestamp):
    """Timestamp date to ISO format"""

    return datetime.utcfromtimestamp(int(timestamp)).isoformat()


def compute_vote(votes, excluded="0"):
    i = 0
    for (user, vote) in votes.items():
        if user == excluded:
            continue

        if vote == '+':
            i += 1
        elif vote == '-':
            i -= 1

        return i


def get_preview(response, language: str):
    """extract a preview if possible"""

    # try to find a block with 'preview' as class
    preview = response.css(".preview p::text").get()

    if preview:
        return preview

    # else fallback to the description field
    description = response.xpath(
        "//strong[contains(text(), 'Description')]/ancestor::p").get()

    if not description:
        return None

    description = normalize('NFKD', remove_tags(remove_tags_with_content(
        description, which_ones=("sup",))))

    sentences = []

    try:
        # if the language is supported by nltk, we split the frst 450 chars of the description in correct sentences
        sentences = tokenize.sent_tokenize(description[:450], language)
    except LookupError:
        # fallback to the first 149 + '…' chars of the description
        return description[:149] + '…'

    # if the description contains only one sentence and less
    # than 15 chars, we will consider that there is no preview.
    if len(sentences) == 1:
        return None if len(sentences[0]) <= 15 else sentences[0]

    # last sentence is eliminated because it is probably incomplete...
    return ' '.join(sentences[:-1])
