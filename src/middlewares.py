# -*- coding: utf-8 -*-
import json
import re

from scrapy import exceptions, signals


forbidden = re.compile(r'\/(_|nav:|admin:|system:|css:|forum:?|search:)')


class SherlockDownloaderMiddleware(object):

    def process_request(self, request, spider):
        """Prohibit incompatible URL"""
        url = request.url

        if forbidden.search(url):
            raise exceptions.IgnoreRequest('{} is blacklisted'.format(url))

    def process_response(self, request, response, spider):
        """Format Wikidot API response"""

        #  Wikidot famous
        #      ⊂_ヽ
        #     　 ＼＼ HTML in
        #     　　 ＼( ͡° ͜ʖ ͡°)
        #     　　　 >　 ヽ
        #     　　　/ 　 へ＼
        #     　　 /　　/　＼＼JSON
        #     　　 ﾚ　ノ　　 ヽ_つ
        #     　　/　/
        #     　 /　/|
        #     　(　(ヽ
        #     　|　|、＼
        #     　| 丿 ＼ ⌒)
        #     　| |　　) /
        #     ノ )　　Lﾉ
        #    (_／

        url = response.url
        if url.endswith('ajax-module-connector.php'):
            data = json.loads(response.text)

            if data['status'] != 'ok':
                raise exceptions.IgnoreRequest(
                    'status != ok for {}'.format(url))

            response = response.replace(body=data['body'])

        return response
