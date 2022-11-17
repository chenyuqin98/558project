import scrapy
import time
from ..items import HearthstoneDesk

class DeskSpider(scrapy.Spider):
    name = 'desk'
    # allowed_domains = ['www.hearthstonetopdecks.com']
    # start_urls = ['https://www.hearthstonetopdecks.com/decks/']

    def start_requests(self):
        # urls = ['https://www.hearthstonetopdecks.com/decks/'] # this is for test
        base = 'https://www.hearthstonetopdecks.com/decks/page/'
        urls = [base+str(i)+'/' for i in range(100)]
        for url in urls:
            # time.sleep(1.5)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        names = response.xpath("//td/h4/a/text()").getall()
        desk_urls = response.xpath("//td/h4/a/@href").getall()
        prices = response.xpath("//tr/td[4]/text()").getall()
        scores = response.xpath("//tr/td[6]/text()").getall()
        print('desk info: ', names, desk_urls, prices, scores)
        if len(names) == len(desk_urls):
            for i in range(len(names)):
                request = scrapy.Request(url=desk_urls[i], callback=self.parse2, cb_kwargs=dict(main_url=response.url))
                request.cb_kwargs['name'] = names[i]
                request.cb_kwargs['price'] = prices[i].replace(',', '')
                request.cb_kwargs['score'] = scores[i]
                request.cb_kwargs['desk_url'] = desk_urls[i]
                yield request

    def parse2(self, response, main_url, name, price, score, desk_url):
        card_names = response.xpath("//li/a/span/text()").getall()
        print('card_names', card_names)
        yield HearthstoneDesk(url=desk_url, name=name, price=price, score=score, cards=card_names)