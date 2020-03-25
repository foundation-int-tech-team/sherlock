# -*- coding: utf-8 -*-
import re
from typing import Dict

import scrapy
from twisted.internet.defer import inlineCallbacks

from sherlock import items
from sherlock.lib import Config, Foundation, Wikidot, regex

Response = scrapy.http.response.html.HtmlResponse


class PagesSpider(scrapy.spiders.SitemapSpider):
    name = 'pages'
    # allowed_domains = ['wikidot.com']
    sitemap_follow = [r'sitemap_page']

    api: str = None
    info: Dict[str, str] = {"branch_id": None, "language": None}

    def __init__(self, site=None, *args, **kwargs):
        super(PagesSpider, self).__init__(*args, **kwargs)

        Config.check(site)

        self.info = {
            "branch_id": Config.get(site, 'id'),
            "language": Config.get(site, 'language')
        }

        self.sitemap_urls = [Wikidot.path(site, 'sitemap.xml')]
        self.api = Wikidot.path(site, 'ajax-module-connector.php')

    @inlineCallbacks
    def parse(self, response: Response):
        """
            Retrieves all information related to the current page

            Wikidot serves some metadata (history, vote...) of the page only via its API 
            and loads it on their page via AJAX. We must therefore simulate these calls. 
        """

        item = scrapy.loader.ItemLoader(items.Page(), response)

        item.add_css('title', 'div#page-title::text')
        item.add_css('tag', 'div.page-tags a::text')

        item.add_value('preview', Foundation.preview(
            response, language=self.info['language']))

        # Some informations is given by Wikidot in Javascript in the page, in a <script> tag
        script = response.xpath(
            '/html/head/script[contains(., "URL")]/text()').get()
        item.add_value('id', script, re=regex['page_id'])
        item.add_value('branch_id', script, re=regex['site_id'])
        item.add_value('slug', script, re=regex['page_slug'])

        item = item.load_item()

        # Some information is loaded on-demand via an XHR request that we simulate here
        data, cookie = Wikidot.request(
            'history/PageRevisionListModule',
            page_id=item['id'], perpage=99999
        )

        response = yield self.request(
            scrapy.FormRequest(self.api,
                               cookies=cookie,
                               formdata=data,
                               priority=2))

        item = scrapy.loader.ItemLoader(item, response)

        item.add_xpath('created_by', '//table/tr[last()]/td/span/a[1]/@onclick',
                       re=regex['user_id'])
        item.add_xpath('created_at', '//table/tr[last()]/td[6]/span/@class',
                       re=regex['timestamp'])
        item.add_xpath('updated_at', '//table/tr[2]/td[6]/span/@class',
                       re=regex['timestamp'])

        item = item.load_item()

        data, cookie = Wikidot.request(
            'pagerate/WhoRatedPageModule',
            pageId=item['id']
        )

        response = yield self.request(
            scrapy.FormRequest(self.api,
                               cookies=cookie,
                               formdata=data,
                               priority=1))

        pool = dict()
        for block in response.css('div > span.printuser:not(.deleted)'):
            user = block.css(
                'a:first-child::attr(onclick)'
            ).re_first(regex['user_id'])
            vote = block.css('* + span::text').get().strip()

            pool[user] = vote

        item['rating'] = pool

        return item

    def request(self, request):
        return self.crawler.engine.download(request, self)
