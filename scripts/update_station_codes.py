#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapelib
import lxml.html
import os
import json


class StationCodeUpdator:
    ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
    DATA_DIR = os.path.join(ROOT, 'data')
    DATA_FILE = 'station_codes.json'
    DATA_PATH = os.path.join(DATA_DIR, DATA_FILE)

    BASE_URL = 'http://www.denno.net/SFCardFan/index.php?pageID=%s'
    REQ_PER_MIN = 10
    DATA_SCHEME = [
        'area_code', 'section_code', 'station_code',
        'company_name', 'section_name', 'station_name',
        'note'
    ]

    def __init__(self):
        self.data = []
        self.scraper = scrapelib.Scraper(
            requests_per_minute=StationCodeUpdator.REQ_PER_MIN
        )
        self.data_path = StationCodeUpdator.DATA_PATH

    def page_body(self, page=1):
        url = StationCodeUpdator.BASE_URL % page
        res = self.scraper.get(url)
        return res.text

    def dom_from_html(self, html):
        return lxml.html.fromstring(html)

    def text_from_td_node(self, td_node):
        return td_node.text.encode('utf-8') if td_node.text else ''

    def data_from_tr_node(self, tr_node):
        array = [self.text_from_td_node(td) for td in list(tr_node)]
        return dict(zip(StationCodeUpdator.DATA_SCHEME, array))

    def find_data(self, dom):
        trs = dom.xpath('//*[@id="add1"]/center/table/tr')
        data = [self.data_from_tr_node(tr) for tr in trs]
        return data[2:]  # first two rows contains meta data

    def find_max_page(self, dom):
        num = dom.xpath('//*[@id="add1"]/center/table/tr[1]/td/a[last()]')
        return int(num[0].text.translate(None, '[]'))

    def save(self, data):
        with open(self.data_path, 'w') as f:
            json.dump(data, f, sort_keys=False, ensure_ascii=False, indent=2)

    def update(self):
        body_text = self.page_body(page=1)
        dom = self.dom_from_html(body_text)
        max_page = self.find_max_page(dom)
        for i in range(max_page):
            print 'Fetching Page %s/%s..' % (i+1, max_page)
            body_text = self.page_body(page=(i+1))
            dom = self.dom_from_html(body_text)
            self.data.extend(self.find_data(dom))
        print 'Saving data..'
        self.save(self.data)

updator = StationCodeUpdator()
updator.update()
