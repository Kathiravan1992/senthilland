import scrapy
from scrapy.http import Request
from scrapy import Selector
import pandas as pd
import datetime
import json


class SjSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['sjc-tax.us']
    start_urls = ['https://sjc-tax.us/']

    def parse(self, response):
        df=pd.read_excel('Sj.xlsx')
        lists_url=list(df['APN'])

        for urls in lists_url:
            url=f"https://sjc-tax.us/ProxyT/Search/Properties/?f={urls}%22&ty=2022"

            headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'dnn_IsMobile=False; language=en-US; .ASPXANONYMOUS=B3rsqA6BG7AFz4lyakMejqTwF-eqqRhHbdg9t7Gv2JuPZufcx6e3_uc3Hy_Xf-oDah_FiUNADBgmCcVveEt1fj9zaNWIuA_geBct6y1cUxoN7-Wo0; ASP.NET_SessionId=ofxs45jdhq1hiplnx3q5zzqf',
            'Referer': 'https://sjc-tax.us/Property-Search-Result/searchtext/R76942%22',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-KL-saas-Ajax-Request': 'Ajax_Request',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
            }

            yield Request(url, callback=self.parse_category,headers=headers)

    def parse_category(self,response):
        datas=json.loads(response.text)
        for data in datas['ResultList']:
            owner_id=(data['PropertyQuickRefID'])
            party_id=(data['PartyQuickRefID'])

            yield{
                'owner_id':owner_id,
                'party_id':party_id

            }

