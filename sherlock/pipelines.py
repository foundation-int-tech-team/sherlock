# -*- coding: utf-8 -*-
from os import getenv

import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv
from scrapy import exceptions

from sherlock import items
from sherlock.lib import Wikidot


class SherlockPipeline(object):
    """Various check for items"""

    title_seen = set()

    def process_item(self, item, spider):
        if isinstance(item, items.Title):
            if item['subtitle'] in self.title_seen:
                raise exceptions.DropItem('subtitle is already included')

            self.title_seen.add(item['subtitle'])

        if isinstance(item, items.Page):
            item.setdefault('tag', [])

            if 'admin' in item['tag']:
                raise exceptions.DropItem('"admin" tag found')

            if 'main' == item['slug']:
                raise exceptions.DropItem('main page should not be included')

        return item


INSERT_PASS = """
    INSERT INTO public.pass (branch_id, subject) VALUES (%(branch_id)s, %(subject)s)
        RETURNING id;
"""

UPDATE_PASS = """
    UPDATE public.pass SET 
        ended_at = NOW(),
        pending = %(pending)s,
        successful = %(successful)s 
        WHERE id = %(id)s; 
"""

UPSERT_PAGE = """
    INSERT INTO public.page (id, title, preview, branch_id, slug, vote, tag, created_at, created_by, pass_id)
        VALUES (%(id)s, %(title)s, %(preview)s, %(branch_id)s, %(slug)s, %(vote)s, %(tag)s, %(created_at)s, %(created_by)s, %(pass_id)s)
    ON CONFLICT (id) DO UPDATE SET
        pass_id = EXCLUDED.pass_id,
        preview = EXCLUDED.preview,
        title = EXCLUDED.title,
        slug = EXCLUDED.slug,
        vote = EXCLUDED.vote;
"""

UPSERT_MEMBERSHIP_AND_USER = """
    WITH data (user_id, branch_id, pass_id, member_since, username, slug) AS (
        VALUES (integer %(user_id)s, integer %(branch_id)s, integer %(pass_id)s, timestamp with time zone %(member_since)s, text %(username)s, text %(slug)s)
    ),

        inserted_user AS (
            INSERT INTO public.user (id, username, slug)
                SELECT user_id, username, slug FROM data
                    ON CONFLICT (id) DO UPDATE SET
                        username = EXCLUDED.username,
                        slug = EXCLUDED.slug
        )

    INSERT INTO public.membership (user_id, branch_id, pass_id, member_since)
        SELECT user_id, branch_id, pass_id, member_since FROM data
            ON CONFLICT (user_id, branch_id) DO UPDATE SET
                pass_id = EXCLUDED.pass_id;
"""

UPDATE_PAGE_SUBTITLE = """
    UPDATE public.page SET subtitle = %(subtitle)s WHERE slug = %(slug)s;
"""


class SherlockStoragePipeline(object):
    """Store item in Database"""

    pass_id: int = None
    connection = None
    cursor = None

    def __init__(self):
        load_dotenv()

        connection = psycopg2.connect(
            host=getenv('PG_HOST'),
            database=getenv('PG_DATABASE'),
            user=getenv('PG_USER'),
            password=getenv('PG_PASSWORD')
        )

        connection.autocommit = True

        self.connection = connection

    def process_item(self, item, spider):
        if isinstance(item, items.Page):
            data = {
                **item,
                'created_by': item.get('created_by', None),
                'preview': item.get('preview', None),
                'vote': Wikidot.compute_vote(item.get('rating'), without=item.get('created_by')),
                'pass_id': self.pass_id
            }

            self.cursor.execute(UPSERT_PAGE, data)

        if isinstance(item, items.Member):
            data = {
                **item,
                'pass_id': self.pass_id
            }

            self.cursor.execute(UPSERT_MEMBERSHIP_AND_USER, data)

        if isinstance(item, items.Title):
            self.cursor.execute(UPDATE_PAGE_SUBTITLE, item)

        return item

    def open_spider(self, spider):
        cursor = self._get_cursor()

        # keep tacks of the analyses performed (useful for data invalidation)
        cursor.execute(INSERT_PASS,
                       {
                           'branch_id': spider.info['branch_id'],
                           'subject': spider.name
                       })

        # attach the current pass id to this pipeline
        self.pass_id = str(cursor.fetchone()['id'])
        self.cursor = cursor

    def close_spider(self, spider):
        data = {
            'id': self.pass_id,
            'pending': False,
            'successful': True
        }

        self.cursor.execute(UPDATE_PASS, data)

        self.cursor.close()
        self.connection.close()

    def _get_cursor(self):
        return self.connection.cursor(
            cursor_factory=extras.DictCursor)
