import scrapy
from scrapy.http import Request
from scrapy import Selector
import pandas as pd
import datetime
import json


class SjSpider(scrapy.Spider):
    name = 'san_jacinto_prop'
    #allowed_domains = ['propaccess.trueautomation.com']
    start_urls = ['https://propaccess.trueautomation.com/ClientDB/PropertySearch.aspx?cid=22']

    def parse(self, response):
        df=pd.read_excel('Sj.xlsx')
        lists_url=list(df['APN'])

        for urls in lists_url:
            url=f"https://propaccess.trueautomation.com/ClientDB/Property.aspx?cid=22&prop_id={urls}"

            yield Request(url, callback=self.parse_category)

    def parse_category(self,response):
        APN=response.xpath('//*[contains(text(),"Property ID:")]/following::td[1]/text()').extract_first()
        name=response.xpath('//*[contains(text(),"Name:")]/following::td[1]/text()').extract_first()
        state="TX"
        county="SAN_JACINTO"
        address=response.xpath('//*[contains(text(),"Mailing Address:")]/following::td[1]/text()').extract()
        acerage=response.xpath('//*[@summary="Land Details"]/tbody/tr[2]/td[4]/text()').extract_first()
        market_value=response.xpath('//*[@summary="Roll Value History"]/tr[3]/td[3]/text()').extract_first()
        assessed_value=response.xpath('//*[@summary="Roll Value History"]/tr[3]/td[7]/text()').extract_first()

        yield{
                'APN':APN,
                'name':name,
                'state':state,
                'county':county,
                'address':address,
                'acerage':acerage,
                'market_value':market_value,
                'assessed_value':assessed_value





            }

