import argparse
import re
from os import environ
from sys import exit
from time import sleep

import meilisearch
import queries
from dotenv import load_dotenv

load_dotenv()

SELECT_PAGE = """
    SELECT ARRAY_AGG(ROW_TO_JSON(t)) as data FROM (
        SELECT usr.username as author, page.id, title, subtitle, preview, tags, (branch.url || page.slug) AS url
            FROM public.page
            INNER JOIN public.branch ON page.branch_id = branch.id
            LEFT JOIN public.user as usr ON page.created_by = usr.id
    ) t;
"""
URI = queries.uri(
    host=environ['PG_HOST'],
    port=environ['PG_PORT'],
    dbname=environ['PG_DBNAME'],
    user=environ['PG_USER'],
    password=environ['PG_PASSWORD']
)
ITEM_CHOICES = ['member']
LOCALE_CHOICES = ['fr', 'en', 'int']
TITLE_REGEX = re.compile(r"SCP-(\d+)$")

parser = argparse.ArgumentParser(
    prog="Meilisearch util",
    description="CLI to interact with the Meilisearch database",
    epilog="Because everyone love Meilisearch"
)

parser.add_argument("action", choices=['upload'])
parser.add_argument("--item", choices=ITEM_CHOICES, nargs="+", required=True)
parser.add_argument("--locale", choices=LOCALE_CHOICES,
                    nargs="+", required=True)

print("""
 ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄▄ ▄▄▄     ▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄   ▄▄▄▄▄▄▄ ▄▄   ▄▄
█  █▄█  █       █   █   █   █   █       █       █      █   ▄  █ █       █  █ █  █
█       █    ▄▄▄█   █   █   █   █  ▄▄▄▄▄█    ▄▄▄█  ▄   █  █ █ █ █       █  █▄█  █
█       █   █▄▄▄█   █   █   █   █ █▄▄▄▄▄█   █▄▄▄█ █▄█  █   █▄▄█▄█     ▄▄█       █
█       █    ▄▄▄█   █   █▄▄▄█   █▄▄▄▄▄  █    ▄▄▄█      █    ▄▄  █    █  █   ▄   █
█ ██▄██ █   █▄▄▄█   █       █   █▄▄▄▄▄█ █   █▄▄▄█  ▄   █   █  █ █    █▄▄█  █ █  █
█▄█   █▄█▄▄▄▄▄▄▄█▄▄▄█▄▄▄▄▄▄▄█▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄█ █▄▄█▄▄▄█  █▄█▄▄▄▄▄▄▄█▄▄█ █▄▄█

\tA tool for Sherlock
""")

args = parser.parse_args()

uri = "http://{host}:{port}".format(
    host=environ['MEILISEARCH_HOST'],
    port=environ['MEILISEARCH_PORT']
)
client = meilisearch.Client(uri, environ['MEILISEARCH_KEY'])

try:
    info = client.get_version()
    print(f'Meilisearch v{info["pkgVersion"]}', end="\n\n")
except:
    print('[ERROR] > it is likely that the connection to the specified Meilisearch instance is impossible.')
    exit(1)


def configure_index(index: meilisearch.client.Index):
    if index.uid.endswith("page"):
        index.update_settings({
            "rankingRules": [
                "typo",
                "words",
                "proximity",
                "exactness",
                "attribute",
                "wordsPosition"
            ],
            "searchableAttributes": [
                "title",
                "title:code",
                "subtitle",
                "preview",
                "author"
            ],
            "displayedAttributes": [
                "id",
                "title",
                "subtitle",
                "preview",
                "url",
                "author",
                "tags"
            ]
        })


def title_extraction(item: dict):
    title = item.get('title')
    match = TITLE_REGEX.match(title)

    if match:
        item['title:code'] = match.group(1)

    return item


if args.action == "upload":
    session = queries.Session(URI)

    for item in args.item:
        print(f'> Initialization of the upload for `{item}`', end="\n\n")

        for locale in args.locale:
            print(f'[{item}] > Getting index for `{locale}`...', end="\n\n")

            name = f'{locale}_{item}'
            index = client.get_index(name)

            try:
                index.info()
            except:
                print(f'[{name}] > `{name}` does not seem to exist. Please wait...')

                client.create_index(name, {'primaryKey': 'id'})
                sleep(5)

                configure_index(index)

                print(f'[{name}] > `{name}` created. Resuming procedure...')

            print(f'[{name}] > Fetching raw data from database...')

            result = session.query(SELECT_PAGE).as_dict()['data']

            print(f'[{name}] > Inserting data into Meilisearch...')

            result = list(map(title_extraction, result))
            update = index.add_documents(result)['updateId']

            print(f'[{name}] > Update in progress ({name}/{update})', end="\n\n")

    session.close()
