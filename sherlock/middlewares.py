# -*- coding: utf-8 -*-
import json
import re

from scrapy import exceptions

forbidden = re.compile(r'\/(_|nav:|admin:|system:|css:|forum:?|search:|test:)')


class SherlockDownloaderMiddleware(object):
    def process_request(self, request, spider):
        """Prohibit incompatible URL"""
        url = request.url

        if forbidden.search(url):
            raise exceptions.IgnoreRequest('{} is blacklisted'.format(url))

    def process_response(self, request, response, spider):
        """Format Wikidot response"""

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

        # if the response is coming from Wikidot API
        if url.endswith('ajax-module-connector.php'):
            data = json.loads(response.text)

            if data['status'] != 'ok':
                raise exceptions.IgnoreRequest(
                    'status != ok for {}'.format(url))

            response = response.replace(body=data['body'])

        return response
