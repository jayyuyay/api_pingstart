# -*-coding:utf-8-*-

import requests
from lxml import html
import sys
import tornado.gen
import tornado.httpclient
from tornado.web import asynchronous
reload(sys)
sys.setdefaultencoding('utf-8')


def get_from_gp(pkg):
    head = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            }
    url = 'https://play.google.com/store/apps/details?id=' + pkg + '&hl=en'
    page = requests.get(url, timeout=5, headers=head, verify=False)
    if page.status_code == 200:
        tree_page = html.fromstring(page.content)
        try:
            app_version = tree_page.xpath("//div[@itemprop='softwareVersion']/text()")[0].strip()
        except IndexError:
            app_version = ''
        return {'pkg': pkg, 'version': app_version}