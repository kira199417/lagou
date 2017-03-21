#!/usr/bin/env python3
"""
Crawl the employ info of python in Guangzhou at lagou.com.
"""

__author__ = 'kira'

import json

import requests
from pymongo import MongoClient
from scrapy import Selector


URL = ('https://www.lagou.com/jobs/positionAjax.json?'
    'city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false')

HEADERS = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection':'keep-alive',
    'Content-Length':'25',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':('JSESSIONID=7D9E9E0AB805E4213F24955AD2F487E7; '
            'user_trace_token=20170225234047-c704c5cb-fb70-11e6'
            '-9019-5254005c3644; LGUID=20170225234047-c704c83b-f'
            'b70-11e6-9019-5254005c3644; index_location_city=%E5'
            '%B9%BF%E5%B7%9E; _ga=GA1.2.471612121.1488037245; LG'
            'SID=20170225234047-c704c6d0-fb70-11e6-9019-5254005c'
            '3644; LGRID=20170226000508-2dad8815-fb74-11e6-8cb5-5'
            '25400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6='
            '1488037246; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6='
            '1488038707; TG-TRACK-CODE=search_code; SEARCH_ID=38ba'
            '9bba666046cc852d9c09793321b0'),
    'Host':'www.lagou.com',
    'Origin':'https://www.lagou.com',
    'Referer':'https://www.lagou.com',
    'User-Agent':('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.'
                '2924.87 Safari/537.36'),
    'X-Anit-Forge-Code':'0',
    'X-Anit-Forge-Token':'None',
    'X-Requested-With':'XMLHttpRequest',
}

# mongodb settings
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB = 'lagou'


def crawl(url):
    data = {'first':'false', 'pn':1, 'kd':'python'}
    while True:
        r = requests.post(url=url, headers=HEADERS, data=data)
        result = json.loads(r.text)
        jobs = result['content']['positionResult']['result']
        if not jobs:
            break
        for j in jobs:
            yield j
        data['pn'] += 1
#    selector = Selector(text=r.text)
#    for div in selector.xpath('//li[contains(@class, "con_list_item")]'):
#        job_id = div.xpath('./@data-positionid').extract_first()
#        salary = div.xpath('./@data-salary').extract_first()
#        company = div.xpath('/@data-company').extract_first()
#        job_name = div.xpath('/@data-positionname').extract_first()
#        yield dict(job_id=job_id, salary=salary, company=company, job_name=job_name)


def main():
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[MONGO_DB]
    for job in crawl(URL):
        db['jobs'].insert_one(job)
    mongo_client.close()

if __name__ == '__main__':
    main()

