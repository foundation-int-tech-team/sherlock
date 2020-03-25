# -*- coding: utf-8 -*-
from re import sub

import scrapy

from sherlock import items
from sherlock.lib import Config, Wikidot, regex


class TitlesSpider(scrapy.Spider):
    name = 'titles'
    allowed_domains = ['wikidot.com']

    def __init__(self, site=None, *args, **kwargs):
        super(TitlesSpider, self).__init__(*args, **kwargs)

        Config.check(site)

        self.info = {
            "branch_id": Config.get(site, 'id')
        }

        paths = Config.get(site, 'index')
        self.start_urls = [Wikidot.path(site, slug) for slug in paths]

    def parse(self, response):
        for title in response.css('.content-panel ul a:not(.newpage)'):
            item = items.Title(branch_id=self.info['branch_id'])

            item['subtitle'] = sub(regex['scp_title'], '', title.xpath(
                'string(./ancestor::li)').get()).strip()
            item['slug'] = title.css('::attr(href)').get()[1:]

            yield item
