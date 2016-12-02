# -*- coding: utf-8 -*-
import scrapy
from techeu.items import TecheuItem
import json


class TecheubasicSpider(scrapy.Spider):
    name = "techeucompaniesbasic"
    rotate_user_agent = True

    def start_requests(self):
        headers = {
            'accept': "*/*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.8",
            'connection': "keep-alive",
            'content-type': "application/json",
            'host': "api.dealroom.co",
            'origin': "https://app.tech.eu",
            'referer': "https://app.tech.eu/investors",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            'x-dealroom-app-id': "310816027",
            'x-requested-with': "XMLHttpRequest",
            'cache-control': "no-cache"
        }
        count = 1000
        offset = 0
        keyword = "software.should"
        payload = "{\"fields\":\"name,path,tagline,images,industries,growth_stage,address,performance,type," \
                  "employees,traffic_summary,total_funding,revenues,company_status," \
                  "fundings,investors,client_focus,models,hq_locations,angellist_url,website_url,twitter_url," \
                  "facebook_url,linkedin_url,crunchbase_url,tg_locations,company_status,ownerships\",\"limit\":"+str(count)+",\"offset\"" \
                  ":"+str(offset)+",\"form_data\":{},\"keyword\":\""+keyword+"\"}"

        url = "https://api.dealroom.co/api/v2/companies"
        yield scrapy.Request(url=url,method='POST',body=payload,callback=self.parse,headers=headers,meta = {'count':count,'keyword':keyword,'offset':offset})


    def parse(self, response):
        count,keyword, offset= response.meta['count'],response.meta['keyword'],response.meta['offset']
        item = TecheuItem()
        json_data = json.loads(response.body_as_unicode())

        for everycompany in json_data["items"]:
            try:
                industry, icon_url, revenue, hqlocation = [], [], [], []
                item['company_name'] = everycompany["name"]
                item['company_description'] = everycompany["tagline"]
                item['website_url'] = everycompany["website_url"]
                item['pagelink'] = "https://app.tech.eu/companies/" + everycompany["path"]
                for everyindustry in everycompany["industries"]:
                    everyindustryname = everyindustry["name"]
                    industry.append(everyindustryname)
                item['listindustry'] = '\n'.join(industry)
                employees = (everycompany["employees"])
                if employees is not None:
                    item['employees'] = employees.replace('-', ' to ')
                item['city'] = everycompany["address"]["city"]
                for everysize in everycompany["images"]:
                    everyicon_url = everycompany["images"][everysize]
                    icon_url.append(everyicon_url)
                item['listicon_url'] = '\n'.join(icon_url)
                item['growth_stage'] = everycompany["growth_stage"]
                item['full_address'] = everycompany["address"]["full_address"]
                item['coordinate'] = "(" + str(everycompany["address"]["lat"]) + "," + str(everycompany["address"]["lon"]) + ")"
                item['company_type'] = everycompany["type"]
                total_funding = everycompany["total_funding"]
                if total_funding != 0:
                    item['total_funding'] = str(everycompany["total_funding"]) + " million Euro"

                for everyrevenue in everycompany["revenues"]:
                    revenue_name = everyrevenue["name"]
                    revenue.append(revenue_name)
                item['listrevenue'] = '\n'.join(revenue)
                item['company_status'] = everycompany["company_status"]
                investor = []
                for everyinvestor in everycompany["investors"]["items"]:
                    investor_name = everyinvestor["name"]
                    investor.append(investor_name)
                item['listinvestor'] = '\n'.join(investor)

                for everyhqlocation in everycompany["hq_locations"]:
                    if everyhqlocation["lat"] is not None or everyhqlocation["lon"]is not None:
                        hqaddress = everyhqlocation["address"]
                        hqcoordinate = "(" + str(everyhqlocation["lat"]) + "," + str(everyhqlocation["lon"]) + ")"
                        newformhqlocation = hqaddress + "," + str(hqcoordinate)
                        hqlocation.append(newformhqlocation)
                    else:
                        hqlocation.append('')
                item['listhqlocation'] = '\n'.join(hqlocation)
                item['angellist_url'] = everycompany["angellist_url"]
                item['twitter_url'] = everycompany["twitter_url"]
                item['facebook_url'] = everycompany["facebook_url"]
                item['crunchbase_url'] = everycompany["crunchbase_url"]
                item['linkedn_url'] = everycompany["linkedin_url"]
                yield item
            except:
                pass
        total = json_data["total"]
        offset = offset + count
        if offset< total:
            headers = {
                'accept': "*/*",
                'accept-encoding': "gzip, deflate, br",
                'accept-language': "en-US,en;q=0.8",
                'connection': "keep-alive",
                'content-type': "application/json",
                'host': "api.dealroom.co",
                'origin': "https://app.tech.eu",
                'referer': "https://app.tech.eu/companies?keyword=software.should",
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
                'x-dealroom-app-id': "310816027",
                'x-requested-with': "XMLHttpRequest",
                'cache-control': "no-cache"
            }

            payload = "{\"fields\":\"id,name,path,tagline,images,industries,growth_stage,address,performance,type," \
                      "employees,traffic_summary,is_editorial,total_funding,kpi_valuation,kpi_revenues,revenues,company_status," \
                      "fundings,investors,is_verified,client_focus,models,hq_locations,angellist_url,website_url,twitter_url," \
                      "facebook_url,linkedin_url,crunchbase_url,tg_locations,company_status,ownerships\",\"limit\":" + str(count) + \
                      ",\"offset\":"+str(offset)+",\"form_data\":{},\"keyword\":\"" + keyword + "\"}"

            url = "https://api.dealroom.co/api/v2/companies"
            yield scrapy.Request(url=url, method='POST', body=payload, callback=self.parse, headers=headers,meta={'count': count,'keyword':keyword,'offset':offset})

