from scrapy.http.request import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from datetime import date
from chesskid.items import Game


class GameSpider(BaseSpider):
    name = 'game'
    allowed_domains = ['chesskid.com', '127.0.0.1']
    host = "127.0.0.1:1080"
    # host = "www.chesskid.com"
    start_urls = ['https://' + host + '/home/game_archive.html?member=Pawel&show=live&page=last']

    def is_online(self):
        return self.host == 'www.chesskid.com'

    def parse_games(self, response):
        if self.is_online():
            return self.parse_games_online(response)
        else:
            return self.parse_games_offline(response)

    @staticmethod
    def parse_games_online(response):
        hxs = HtmlXPathSelector(response)
        for gr in hxs.select('//table[@class="recent-games-table main-table"]/tr'):
            game = Game()

            game['opponent'] = gr.select('td[1]/a/text()').extract()[0]

            game['opponentRanking'] = gr.select('td[1]/text()').extract()[0].lstrip().replace('(', '').replace(')', '')

            d = gr.select('td[2]/text()').extract()[0]
            dd = [int(ns) for ns in d.split("/")]
            game['date'] = date(2000 + dd[2], dd[0], dd[1]).isoformat()

            w = gr.select('td[6]/a/@class').extract()[0]
            game['result'] = 1 if w.endswith("win") else -1

            game['id'] = gr.select('td[6]/a/@href').extract()[0].split('=')[1]

            yield game

    @staticmethod
    def parse_games_offline(response):
        hxs = HtmlXPathSelector(response)
        for gr in hxs.select('//table[@class="games-archive-table main-table"]/tbody/tr'):
            game = Game()

            game['opponent'] = gr.select('td/a/text()').extract()[0]

            game['opponentRanking'] = gr.select('td/text()').extract()[0].lstrip().replace('(', '').replace(')', '')

            d = gr.select('td[3]/text()').extract()[0]
            dd = [int(ns) for ns in d.split("/")]
            game['date'] = date(2000 + dd[2], dd[0], dd[1]).isoformat()

            w = gr.select('td[7]/a/@class').extract()[0]
            game['result'] = 1 if w.endswith("win") else -1

            game['id'] = gr.select('td[7]/a/@href').extract()[0].split('=')[1]

            yield game

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        self.parse_games(response)

        last_page = int(hxs.select('//a[@class="paginator_page"]/text()').extract()[-1])

        for page in range(1, last_page):
            yield Request(self.page_url(page), callback=self.parse_games)

    def page_url(self, page):
        return self.start_urls[0].replace("last", str(page))
