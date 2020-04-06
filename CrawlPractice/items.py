# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserInfoItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    face = scrapy.Field()


class FollowInfoItem(scrapy.Item):
    id = scrapy.Field()
    followers = scrapy.Field()


class UserBookItem(scrapy.Item):
    user_id = scrapy.Field()
    book_id = scrapy.Field()


class BookInfoItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    pic = scrapy.Field()
    info = scrapy.Field()
