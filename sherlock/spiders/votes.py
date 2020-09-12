import scrapy
import queries

from sherlock.utils import Config, regex, wikidot, database
from sherlock.items import VoteItem

import pprint


class VotesSpider(scrapy.Spider):
    name = 'votes'
    allowed_domains = ['wikidot.com']

    def __init__(self, site=None, *args, **kwargs):
        super(VotesSpider, self).__init__(*args, **kwargs)

        self.info = Config.get_config(site)

    def start_requests(self):
        with database.get_session() as session:
            for row in session.query("SELECT id FROM public.page WHERE branch_id = %s"):
                pprint.pprint(row)

    def parse(self, response):
        for block in response.css('span.printuser:not(.deleted)'):
            vote = block.css('* + span::text').get().strip()
            user = block.css(
                'a:first-child::attr(onclick)').re_first(regex['user_id'])

            yield VoteItem(user_id=user, page_id=response['meta']['page_id'], vote=vote)
