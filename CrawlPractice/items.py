# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    face = scrapy.Field()


class FollowInfoItem(scrapy.Item):
    name = scrapy.Field()
    followers = scrapy.Field()


class MovieInfoItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    pic = scrapy.Field()
    info = scrapy.Field()
