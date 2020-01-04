# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from src import utils


class Page(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    lang = scrapy.Field(output_processor=TakeFirst())
    site = scrapy.Field(output_processor=TakeFirst())
    slug = scrapy.Field(output_processor=TakeFirst())
    author = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field()
    tag = scrapy.Field()
    preview = scrapy.Field()
    updated_at = scrapy.Field(
        input_processor=MapCompose(utils.time_to_iso),
        output_processor=TakeFirst()
    )
    created_at = scrapy.Field(
        input_processor=MapCompose(utils.time_to_iso),
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )


class Member(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    username = scrapy.Field(output_processor=TakeFirst())
    site = scrapy.Field(output_processor=TakeFirst())
    pseudo = scrapy.Field(output_processor=TakeFirst())
    member_since = scrapy.Field(
        input_processor=MapCompose(utils.time_to_iso),
        output_processor=TakeFirst()
    )
