# -*- coding: utf-8 -*-
import scrapy

from sherlock import items
from sherlock.lib import Config, Wikidot, regex


class MembersSpider(scrapy.Spider):
    name = 'members'
    allowed_domains = ['wikidot.com']

    def __init__(self, site=None, *args, **kwargs):
        super(MembersSpider, self).__init__(*args, **kwargs)

        Config.check(site)

        self.info = {
            "branch_id": str(Config.get(site, 'id'))
        }

        self.api = Wikidot.path(site, 'ajax-module-connector.php')

    def start_requests(self):
        data, cookie = Wikidot.request(
            'membership/MembersListModule', per_page=1000000)
        yield scrapy.FormRequest(self.api,
                                 cookies=cookie,
                                 formdata=data,
                                 callback=self.analyze_members_list)

    def analyze_members_list(self, response):
        total = response.css('.pager .target:nth-last-child(2) a::text').get()

        # we analyze the pagination to find the total number of pages
        for page in range(0, int(total)):
            data, cookie = Wikidot.request(
                'membership/MembersListModule',
                page=page + 1,
                per_page=1000000
            )

            yield scrapy.FormRequest(self.api, cookies=cookie, formdata=data)

    def parse(self, response):
        for row in response.xpath('//div/table/tr'):

            user = row.xpath('./td[1]/span/a[1]')
            item = scrapy.loader.ItemLoader(item=items.Member(), selector=user)

            item.add_value('branch_id', self.info['branch_id'])
            item.add_xpath('user_id', '@onclick', re=regex['user_id'])
            item.add_xpath('slug', '@href', re=regex['user_slug'])
            item.add_xpath('username', './img/@alt')

            since = row.xpath('./td[2]/span/@class').get()
            item.add_value('member_since', since, re=regex['timestamp'])

            yield item.load_item()
