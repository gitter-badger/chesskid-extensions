# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class Game(Item):
    id = Field()
    opponent = Field()
    opponentRanking = Field()
    date = Field()
    result = Field()
