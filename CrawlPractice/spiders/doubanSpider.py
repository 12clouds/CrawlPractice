# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from CrawlPractice.items import UserInfoItem
from CrawlPractice.items import FollowInfoItem
from CrawlPractice.items import MovieInfoItem


class DoubanspiderSpider(CrawlSpider):
    name = 'doubanSpider'
    allowed_domains = ['douban.com']
    login_url = 'https://accounts.douban.com/passport/login'
    users_urls = 'https://www.douban.com/people'

    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=False),
    )

    def start_requests(self):
        data = {
            'username': '18813138710',
            'password': 'lzy098511'
        }
        yield scrapy.FormRequest(url=self.login_url,
                                 meta={"cookiejar": 1},
                                 callback=self.after_login)

    def after_login(self, response):
        for i in range(1000000, 999999999):
            url = self.users_urls + '/' + str(i) + '/'
            yield scrapy.Request(url=url,

                                 callback=self.parse_users)

    def parse_users(self, response):
        # 爬取用户基本信息
        info = response.xpath("//div[@id='db-usr-profile']/div")
        name = info.xpath(".//h1/text()").get()
        face = info.xpath(".//a/img/@src").get()
        item = UserInfoItem(name=name, face=face)
        yield item

    def parse_movies(self, response):
        # 爬取用户看过的电影
        linkdiv = response.xpath("//div[@id='movie']/h2")
        link = linkdiv.xpath(".//span[@class='pl']/a/@href").get()
        print(link)
        if not link:
            return
        else:
            yield scrapy.Request(url=link, callback=self.parse_movies())
        print(link)

    def parse_item(self, response):
        # name = response.xpath("//div[@id='content']/h1/text()").get().strip()
        # print(name)
        item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
