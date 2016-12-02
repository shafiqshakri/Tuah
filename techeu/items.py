# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TecheuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()
    company_description = scrapy.Field()
    website_url = scrapy.Field()
    pagelink = scrapy.Field()
    listindustry = scrapy.Field()
    employees = scrapy.Field()
    city = scrapy.Field()
    listicon_url = scrapy.Field()
    growth_stage = scrapy.Field()
    full_address = scrapy.Field()
    coordinate = scrapy.Field()
    company_type = scrapy.Field()
    total_funding = scrapy.Field()
    listrevenue = scrapy.Field()
    company_status = scrapy.Field()
    listinvestor = scrapy.Field()
    listhqlocation = scrapy.Field()
    twitter_url = scrapy.Field()
    facebook_url = scrapy.Field()
    linkedn_url = scrapy.Field()
    crunchbase_url = scrapy.Field()
    angellist_url = scrapy.Field()
