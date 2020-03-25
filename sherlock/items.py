# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

from sherlock.lib import Wikidot


class Member(scrapy.Item):
    user_id = scrapy.Field(output_processor=TakeFirst())
    slug = scrapy.Field(output_processor=TakeFirst())
    branch_id = scrapy.Field(output_processor=TakeFirst())
    username = scrapy.Field(output_processor=TakeFirst())
    member_since = scrapy.Field(
        input_processor=MapCompose(Wikidot.time_to_iso),
        output_processor=TakeFirst()
    )


class Page(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    preview = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    branch_id = scrapy.Field(output_processor=TakeFirst())
    slug = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field()
    tag = scrapy.Field()
    created_by = scrapy.Field(output_processor=TakeFirst())
    updated_at = scrapy.Field(
        input_processor=MapCompose(Wikidot.time_to_iso),
        output_processor=TakeFirst()
    )
    created_at = scrapy.Field(
        input_processor=MapCompose(Wikidot.time_to_iso),
        output_processor=TakeFirst()
    )


class Title(scrapy.Item):
    branch_id = scrapy.Field(output_processor=TakeFirst())
    subtitle = scrapy.Field(output_processor=TakeFirst())
    slug = scrapy.Field(output_processor=TakeFirst())
