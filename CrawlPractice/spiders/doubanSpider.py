# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from CrawlPractice.items import UserInfoItem
from CrawlPractice.items import FollowInfoItem
from CrawlPractice.items import BookInfoItem, UserBookItem


class DoubanspiderSpider(CrawlSpider):
    name = 'doubanSpider'
    allowed_domains = ['douban.com']
    login_url = 'https://accounts.douban.com/j/mobile/login/basic' # 'https://accounts.douban.com/passport/login'
    users_urls = 'https://www.douban.com/people'
    book_urls = 'https://book.douban.com/people'

    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=False),
    )

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.fp = open("BigV.txt", 'a')

    def start_requests(self):
        # url = self.users_urls + '/' + str(i) + '/'
        # yield scrapy.Request(url=url,
        #                      cookies=self.cookie,
        #                      callback=self.parse_users)
        data = {
            'name': '18813138710',
            'password': '980511'
        }
        yield scrapy.FormRequest(url=self.login_url,
                                 meta={"cookiejar": 1},
                                 formdata=data,
                                 callback=self.after_login)

    def after_login(self, response):
        print(response.text)
        for i in range(1000001, 1010000):
            # url = self.users_urls + '/' + str(i) + '/' # + '/rev_contacts'
            # yield scrapy.Request(url=url,
            #                      meta={'cookiejar': response.meta['cookiejar']},
            #                      callback=self.parse_users)
            # url = self.users_urls + '/' + str(i) + '/rev_contacts'
            # yield scrapy.Request(url=url,
            #                      meta={'cookiejar': response.meta['cookiejar']},
            #                      callback=self.parse_fans)
            # url = self.users_urls + '/' + str(i) + '/contacts'
            # yield scrapy.Request(url=url,
            #                      meta={'cookiejar': response.meta['cookiejar']},
            #                      callback=self.parse_follows)
            url = self.book_urls + '/' + str(i) + '/collect'
            yield scrapy.Request(url=url,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 callback=self.parse_books)
        # self.fp.close()

    def parse_users(self, response):
        # 爬取用户基本信息
        # user_id = response.xpath("//div[@class='user-opt']/a/@id").get()
        user_id = response.xpath("//div[@class='user-info']/div/text()").get().strip()
        info = response.xpath("//div[@id='db-usr-profile']/div")
        name = info.xpath(".//h1/text()").get().strip()
        face = info.xpath(".//a/img/@src").get()
        item = UserInfoItem(id=user_id, name=name, face=face)
        yield item

    def parse_books(self, response):
        books = response.xpath("//li[@class='subject-item']")
        for book in books:
            pic = book.xpath(".//div[@class='pic']/a/img/@src").get()
            title = book.xpath(".//div[@class='info']/h2/a/@title").get()
            book_id = book.xpath(".//div[@class='pic']/a/@href").get().split('t/')[1].split('/')[0]
            user_id = response.xpath("//ul[@class='nav-list']/li/a/@href").get().split('e/')[1].split('/')[0]
            info = book.xpath(".//div[@class='pub']/text()").get().strip()
            book_item = BookInfoItem(id=book_id, title=title, pic=pic, info=info)
            yield book_item
            user_book_item = UserBookItem(user_id=user_id, book_id=book_id)
            yield user_book_item
        next = response.xpath("//span[@class='next']/a/@href").get()
        if next is not None:
            url = 'https://book.douban.com' + next
            yield scrapy.Request(url=url,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 callback=self.parse_books)

    def parse_follows(self, response):
        # head = response.xpath("//div[@class='info']/h1/text()").get().strip()
        # print(head)
        next_page = response.xpath("//span[@class='next']/a/@href").get()
        user = response.xpath("//div[@class='info']/ul/li/a/@href").get()
        self_id = user.split('/people/')[1].split('/')[0]
        if next_page is None:
            followers = response.xpath("//div[@class='article']/dl")
            for follower in followers:
                user_id = follower.xpath(".//dt/a/@href").get()
                follower_id = user_id.split('e/')[1].split('/')[0]
                item = FollowInfoItem(id=self_id, followers=follower_id)
                yield item
        else:
            self.fp.write(self_id + '\n')

    def parse_fans(self, response):
        head = response.xpath("//div[@class='info']/h1/text()").get().strip()
        print(head)

    def parse_item(self, response):
        # name = response.xpath("//div[@id='content']/h1/text()").get().strip()
        # print(name)
        item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
