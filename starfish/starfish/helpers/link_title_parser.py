import html.parser
import logging

import requests

logger = logging.getLogger(__name__)


def get_title_from_url(url):
    return url and LinkTitleParser(url).title_content


class LinkTitleParser(html.parser.HTMLParser):
    last_content = ''
    title_content = ''

    def __init__(self, url):
        super().__init__()
        self.url = url
        try:
            response = requests.get(self.url, allow_redirects=True, timeout=5)
            if 199 < response.status_code < 300:
                logger.debug(f'Fetched {len(response.content)} bytes from {self.url}')
                self.feed(response.text)
        except requests.exceptions.RequestException:
            logger.warning(f'Could not fetch html for {self.url}')

    def handle_starttag(self, tag, attrs):
        self.last_content = ''

    def handle_endtag(self, tag):
        if tag == 'title' and self.title_content == '':
            self.title_content = self.last_content
            logger.debug(f'Finished parsing and got title {self.title_content}')

    def handle_data(self, data):
        self.last_content += data
