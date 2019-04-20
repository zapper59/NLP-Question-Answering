import scrapy


class MarketWatchSpider(scrapy.Spider):
    name = "market_watch"

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        f = open("../MarketWatchURLs.txt")
        urls = [url.strip() for url in f.readlines()]
        f.close()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'title': response.css('h1#article-headline::text').get(),
            'article': response.xpath('string(//div[@id="article-body"]/p)').get()
        }