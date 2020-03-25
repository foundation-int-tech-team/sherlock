import scrapy
from nltk import data, tokenize
from w3lib.html import remove_tags, remove_tags_with_content
from unicodedata import normalize

Response = scrapy.http.response.html.HtmlResponse

data.path.append('./data/nltk_data')


class Foundation:
    @staticmethod
    def preview(response: Response, language: str):
        """extract a preview from the page if possible"""

        # try to find a block with 'preview' as class
        preview = response.css(".preview p::text").get()
        if preview:
            return preview

        # else fallback to the description field
        description = response.xpath(
            "//strong[contains(text(), 'Description')]/ancestor::p").get()

        if not description:
            return None

        description = Foundation._sanitize(description)

        sentences = []
        try:
            # if the language is supported by nltk, we split the frst 450 chars of the description in correct sentences
            sentences = tokenize.sent_tokenize(description[:400], language)
        except LookupError:
            # fallback to the first 199 + '…' chars of the description
            return description[:149] + '…'

        # if the description contains only one sentence and less
        # than 15 chars, we will consider that there is no preview.
        if len(sentences) == 1:
            return None if len(sentences[0]) <= 15 else sentences[0]

        # the last sentence is eliminated because it is probably incomplete...
        return ' '.join(sentences[:-1])

    @staticmethod
    def _sanitize(text):
        text = remove_tags(remove_tags_with_content(
            text, which_ones=("sup",)))

        return normalize('NFKD', text)
