# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from scrapy.exporters import JsonItemExporter
from CrawlPractice.items import UserBookItem, BookInfoItem, UserInfoItem, FollowInfoItem


class UserInfoItemPipeline(object):
    def __init__(self):
        self.fp = open("users.json", 'wb')
        self.exporter = JsonItemExporter(self.fp,
                                         ensure_ascii=False,
                                         encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, UserInfoItem):
            self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()


class UserBookItemPipeline(object):
    def __init__(self):
        self.fp = open("user-book.json", 'wb')
        self.exporter = JsonItemExporter(self.fp,
                                         ensure_ascii=False,
                                         encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, UserBookItem):
            self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()


class BookInfoItemPipeline(object):
    def __init__(self):
        self.fp = open("books.json", 'wb')
        self.exporter = JsonItemExporter(self.fp,
                                         ensure_ascii=False,
                                         encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, BookInfoItem):
            self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()
