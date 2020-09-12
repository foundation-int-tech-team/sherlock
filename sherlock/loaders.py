from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from scrapy.loader import ItemLoader
from sherlock.utils import regex, wikidot


class MemberLoader(ItemLoader):
    default_output_processor = TakeFirst()

    member_since_in = MapCompose(wikidot.time_to_iso)


class PageLoader(ItemLoader):
    default_output_processor = TakeFirst()

    title_in = MapCompose(str.strip)
    preview_in = MapCompose(str.strip)
    tags_out = Identity()
    created_at_in = MapCompose(wikidot.time_to_iso)
    updated_at_in = MapCompose(wikidot.time_to_iso)


class TitleLoader(ItemLoader):
    default_output_processor = TakeFirst()

    subtitle_in = MapCompose(str.strip)
    slug_in = MapCompose(lambda slug: slug[1:])
