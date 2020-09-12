# -*- coding: utf-8 -*-
import re

import scrapy
from twisted.internet.defer import inlineCallbacks

from sherlock import items, loaders
from sherlock.utils import Config, regex, wikidot


class PagesSpider(scrapy.spiders.SitemapSpider):
    name = 'pages'
    sitemap_follow = [r'sitemap_page']

    def __init__(self, site=None, *args, **kwargs):
        super(PagesSpider, self).__init__(*args, **kwargs)

        self.info = Config.get_config(site)

        self.api = wikidot.path(site, 'ajax-module-connector.php')
        self.sitemap_urls = [wikidot.path(site, 'sitemap.xml')]

    def request(self, *args, **kwargs):
        request = scrapy.FormRequest(*args, **kwargs)
        return self.crawler.engine.download(request, self)

    @inlineCallbacks
    def parse(self, response):
        item = loaders.PageLoader(items.PageItem(), response)

        item.add_value('branch_id', self.info['branch_id'])
        item.add_css('title', 'div#page-title::text')
        item.add_css('tags', 'div.page-tags a::text')

        item.add_value('preview', wikidot.get_preview(
            response, language=self.info['language']))

        script = response.xpath(
            '/html/head/script[contains(., "URL")]/text()').get()

        item.add_value('page_id', script, re=regex['page_id'])
        item.add_value('branch_id', script, re=regex['branch_id'])
        item.add_value('slug', script, re=regex['page_slug'])

        item = item.load_item()

        # Some information is loaded on-demand via an XHR request that we need to simulate here
        data, cookie = wikidot.request(
            'history/PageRevisionListModule',
            page_id=item.page_id,
            perpage=99999
        )

        response = yield self.request(self.api,
                                      cookies=cookie,
                                      formdata=data,
                                      )

        item = loaders.PageLoader(item, response)
        item.add_xpath('created_by', '//table/tr[last()]/td/span/a[1]/@onclick',
                       re=regex['user_id'])
        item.add_xpath('created_at', '//table/tr[last()]/td[6]/span/@class',
                       re=regex['timestamp'])
        item.add_xpath('updated_at', '//table/tr[2]/td[6]/span/@class',
                       re=regex['timestamp'])

        return item.load_item()
