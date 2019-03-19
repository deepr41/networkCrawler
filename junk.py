import scrapy
from scrapy.crawler import CrawlerProcess
import logging
from scrapy.http import Request
class WebSpider(scrapy.Spider):
    name = 'webspider'
    #start_urls = ['https://www.google.com/']
    def __init__(self):
        logging.getLogger('scrapy').setLevel(logging.ERROR)

        self.start_urls=['https://www.google.com','https://www.youtube.com','https://www.reddit.com','https://www.facebook.com','https://www.yahoo.com','https://www.gmail.com','https://www.netflix.com']
    
    # def make_requests_from_url(self, url):
    #     item = MyItem()

    #     # assign url
    #     item['start_url'] = url
    #     request = Request(url, dont_filter=True)

    #     # set the meta['item'] to use the item in the next call back
    #     request.meta['item'] = item
    #     return request



        # access and do something with the item in parse
        

    def start_requests(self):
        for i,u in enumerate(self.start_urls):
            request = Request(u, callback=self.parse, dont_filter=True)
            #request.meta['req_url'] = u
            yield request            

        

    def parse(self, response):
        url = response.meta['req_url']
        print("****************",response.request.url,url)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',

})

process.crawl(WebSpider)
process.start()