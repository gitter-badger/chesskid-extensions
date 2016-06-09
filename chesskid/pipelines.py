from scrapy.exceptions import DropItem
import csv
import os.path


class DuplicatesPipeline(object):

    def __init__(self):
        self.duplicates = set()
        games_file = 'games.csv'

        if os.path.isfile(games_file):
            with open(games_file, 'rb') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    self.duplicates.add(row[1])

    def process_item(self, item, spider):
        if item['id'] in self.duplicates:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.duplicates.add(item['id'])
            return item
