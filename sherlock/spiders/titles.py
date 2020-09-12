import scrapy

from sherlock import items, loaders
from sherlock.utils import Config, database, wikidot, regex


class TitlesSpider(scrapy.Spider):
    name = 'titles'
    allowed_domains = ['wikidot.com']

    def __init__(self, site=None, *args, **kwargs):
        super(TitlesSpider, self).__init__(*args, **kwargs)

        self.info = Config.get_config(site)

        index = Config.get(site, 'index')
        self.start_urls = [wikidot.path(site, slug) for slug in index]

    def parse(self, response):
        for title in response.css('.content-panel ul a:not(.newpage)'):
            item = loaders.TitleLoader(items.TitleItem(), selector=title)

            item.add_value('branch_id', self.info['branch_id'])
            item.add_xpath('subtitle', 'string(./ancestor::li)',
                           re=regex['scp_subtitle'])
            item.add_css('slug', '::attr(href)')

            yield item.load_item()
