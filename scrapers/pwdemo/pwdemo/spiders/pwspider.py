import scrapy


class PwspiderSpider(scrapy.Spider):
    name = 'pwspider'
    allowed_domains = ['test.com']
    start_urls = ['http://test.com/']

    def parse(self, response):
        pass
