# -*- coding: utf-8 -*-
import scrapy
import re
from twisted.internet.defer import inlineCallbacks

from src import utils, items, regex


class PagesSpider(scrapy.spiders.SitemapSpider):
    name = 'pages'
    allowed_domains = ['wikidot.com', 'scp-wiki.net']
    sitemap_follow = [r'sitemap_page']

    def __init__(self, site=None, *args, **kwargs):
        super(PagesSpider, self).__init__(*args, **kwargs)

        if site is None:
            raise AssertionError("You must provide a `site` to crawl")

        self.sitemap_urls = [utils.wikidot(site, 'sitemap.xml')]
        self.api = utils.wikidot(site, 'ajax-module-connector.php')

    @inlineCallbacks
    def parse(self, response):
        item = scrapy.loader.ItemLoader(item=items.Page(), response=response)

        # page
        item.add_xpath('lang', '/html/@lang')
        item.add_css('title', 'div#page-title::text')
        item.add_css('tag', 'div.page-tags a::text')

        script = response.xpath(
            '/html/head/script[contains(., "URL")]/text()'
        ).get()

        item.add_value('id', script, re=regex.regex['page_id'])
        item.add_value('site', script, re=regex.regex['site'])
        item.add_value('slug', script, re=regex.regex['slug'])

        item = item.load_item()

        # history
        data, cookie = utils.request(
            'history/PageRevisionListModule',
            page_id=item['id'], perpage="99999"
        )

        response = yield self.request(
            scrapy.FormRequest(self.api,
                               cookies=cookie,
                               formdata=data,
                               priority=2))

        item = scrapy.loader.ItemLoader(item, response=response)

        item.add_xpath('author', '//table/tr[last()]/td/span/a[1]/@onclick',
                       re=regex.regex['user_id'])
        item.add_xpath('created_at', '//table/tr[last()]/td[6]/span/@class',
                       re=regex.regex['timestamp'])
        item.add_xpath('updated_at', '//table/tr[2]/td[6]/span/@class',
                       re=regex.regex['timestamp'])

        item = item.load_item()

        # vote
        data, cookie = utils.request(
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
            ).re_first(regex.regex['user_id'])
            vote = block.css('* + span::text').get().strip()

            pool[user] = vote

        item['rating'] = pool

        return item

    def request(self, request):
        return self.crawler.engine.download(request, self)
