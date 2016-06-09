from scrapy.exceptions import DropItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
import csv
import os.path

games_file = 'games.csv'


class DuplicatesPipeline(object):

    def __init__(self):
        self.duplicates = set()

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


class CsvExportPipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}
        self.exporter = None

    def spider_opened(self, spider):
        g_file = open(games_file, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(g_file, include_headers_line=False)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.files.pop(spider).close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
