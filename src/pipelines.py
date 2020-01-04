# -*- coding: utf-8 -*-
from scrapy import exceptions
from src import items


class SherlockPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, items.Page):
            self.process_page(item)

        return item

    def process_page(self, item):
        """Process page item"""
        item.setdefault('tag', [])
        item.setdefault('author', None)

        if "admin" in item['tag']:
            raise exceptions.DropItem(
                'admin tag in found {}'.format(item['id']))

        if item['slug'] == "main":
            raise exceptions.DropItem('main page should not be saved')
