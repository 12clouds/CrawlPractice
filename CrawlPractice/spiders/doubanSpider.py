# -*- coding: utf-8 -*-
import scrapy
import re
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
    cookie = {'Cookie': '_vwo_uuid_v2=D49E02E5D37D4D6A1A6FBD7EEE590D1B2|975b38a112c303c90bb0c55c4fff76ef; '
                        'gr_user_id=e4b350e5-fdae-41f3-8e37-c5e3f438ea65; douban-fav-remind=1; '
                        'viewed="24715686_27170538_3920144_30316403_30302117"; douban-profile-remind=1; '
                        '_ga=GA1.2.1613762438.1552199665; push_noty_num=0; push_doumail_num=0; __utmv=30149280.18787; '
                        'll="118130"; bid=KQqb8BCR098; ct=y; ap_v=0,6.0; __utmc=30149280; '
                        '__utmz=30149280.1585658736.10.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; '
                        'dbcl2="187870662:Fm9lWjvFkPs"; ck=k_0F; '
                        '_pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1585662522%2C%22https%3A%2F%2Faccounts.douban.com'
                        '%2Fpassport%2Flogin%22%5D; _pk_ses.100001.8cb4=*; '
                        '__utma=30149280.1613762438.1552199665.1585658736.1585662529.11; __utmt=1; '
                        '__utmb=30149280.2.10.1585662529; '
                        '_pk_id.100001.8cb4=b4c2098c24811d3d.1564404182.51.1585662563.1585658715.'}
    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=False),
    )

    def start_requests(self):
        i = 187870662
        url = self.users_urls + '/' + str(i) + '/'
        yield scrapy.Request(url=url,
                             cookies=self.cookie,
                             callback=self.parse_users)
        # data = {
        #     'username': '18813138710',
        #     'password': 'lzy098511'
        # }
        # yield scrapy.FormRequest(url=self.login_url,
        #                          meta={"cookiejar": 1},
        #                          callback=self.after_login)

    def after_login(self, response):
        i = 1000001
        # for i in range(1000001, 999999999):
        url = self.users_urls + '/' + str(i) + '/rev_contacts'
        yield scrapy.Request(url=url,
                             meta={'cookiejar': response.meta['cookiejar']},
                             callback=self.parse_follows)

    def parse_users(self, response):
        # 爬取用户基本信息
        info = response.xpath("//div[@id='db-usr-profile']/div")
        name = info.xpath(".//h1/text()").get().strip()
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

    def parse_follows(self, response):
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
