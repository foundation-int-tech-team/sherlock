# -*- coding: utf-8 -*-
import scrapy

from src import utils, items, regex


class MembersSpider(scrapy.Spider):
    name = 'members'
    allowed_domains = ['wikidot.com']

    site = None

    def __init__(self, site=None, *args, **kwargs):
        super(MembersSpider, self).__init__(*args, **kwargs)

        if site is None:
            raise AssertionError("You must provide a `site` to crawl")

        self.api = utils.wikidot(site, 'ajax-module-connector.php')
        self.site = site

    def start_requests(self):
        data, cookie = utils.request('membership/MembersListModule')
        yield scrapy.FormRequest(self.api,
                                 cookies=cookie,
                                 formdata=data,
                                 callback=self.analyze_members_list)

    def analyze_members_list(self, response):
        total = response.css('.pager .target:nth-last-child(2) a::text').get()

        for page in range(0, int(total)):
            data, cookie = utils.request(
                'membership/MembersListModule',
                page=page + 1
            )

            yield scrapy.FormRequest(self.api, cookies=cookie, formdata=data)

    def parse(self, response):
        for row in response.xpath('//div/table/tr'):

            user = row.xpath('./td[1]/span/a[1]')
            item = scrapy.loader.ItemLoader(item=items.Member(), selector=user)

            item.add_value('site', self.site)
            item.add_xpath('username', '@href', re=regex.regex['username'])
            item.add_xpath('id', '@onclick', re=regex.regex['user_id'])
            item.add_xpath('pseudo', './img/@alt')

            since = row.xpath('./td[2]/span/@class').get()
            item.add_value('member_since', since, re=regex.regex['timestamp'])

            yield item.load_item()
