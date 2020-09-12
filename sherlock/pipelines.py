from scrapy import exceptions

from sherlock import items
from sherlock.utils import database
from dataclasses import asdict

from psycopg2 import extras


class SherlockCheckPipeline:
    def process_item(self, item, spider):
        if isinstance(item, items.PageItem):
            if "admin" in item.tags:
                raise exceptions.DropItem("`admin` tag found")

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


class SherlockStoragePipeline:
    id = None
    """Maintains an id representing the current process"""

    session = None

    def __init__(self):
        self.session = database.get_session()

    def open_spider(self, spider):
        cursor = self.session.cursor

        cursor.execute(INSERT_PASS, {
            'branch_id': spider.info['branch_id'],
            'subject': spider.name
        })

        # attach the current pass id to this pipeline
        self.id = cursor.fetchone()['id']

    def close_spider(self, spider):
        self.session.cursor.execute(UPDATE_PASS, {
            'id': self.id,
            'pending': False,
            'successful': True
        })

        self.session.close()

    def process_item(self, item, spider):
        if isinstance(item, items.MemberItem):
            # maybe batch users if possible
            self.session.callproc(
                "add_member", {**asdict(item), 'pass_id': self.id})

        if isinstance(item, items.PageItem):
            self.session.callproc(
                "add_page", {**asdict(item), 'pass_id': self.id})

        if isinstance(item, items.TitleItem):
            self.session.callproc("add_title", asdict(item))

        return item
