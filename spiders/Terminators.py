import scrapy
import requests
import xml.etree.ElementTree as etree
import json
from enum import Enum
from helper import get_details

# 1.Forward
# 2.Bidirectional
# 3.Reverse
# 4.Yeast
# 5.Eukaryotic


class Type(Enum):
    Forward = 1
    Bidirectional = 2
    Reverse = 3
    Yeast = 4
    Eukaryotic = 5


class TerminatorSpider(scrapy.Spider):
    name = "Terminator Spider"

    def start_requests(self):
        yield scrapy.Request(url='http://parts.igem.org/Terminators/Catalog', callback=self.parse_webpage)

    def parse_webpage(self, response):
        tables = response.xpath('//table[@id="assembly_plasmid_table"]')
        for table_index, table in enumerate(tables, start=0):
            biobricks = table.xpath('tr')
            for bb in biobricks[1:]:
                bb_res = dict()
                bb_res['name'] = bb.xpath('td').xpath(
                    'a/text()').extract_first()
                bb_res['part'] = 'Terminator'
                if table_index == 0:
                    bb_res['type'] = 'Forward'
                elif table_index == 1:
                    bb_res['type'] = 'Bidirectional'
                elif table_index == 2:
                    bb_res['type'] = 'Reverse'
                elif table_index == 3:
                    bb_res['type'] = 'Yeast'
                elif table_index == 4:
                    bb_res['type'] = 'Eukaryotic'
                bb_res['forward'] = "".join(
                    bb.xpath('td[@class="c_4"]/descendant-or-self ::*/text()').extract())
                bb_res['reverse'] = "".join(
                    bb.xpath('td[@class="c_5"]/descendant-or-self ::*/text()').extract())
                bb_res['length'] = "".join(
                    bb.xpath('td[@class="c_7"]/descendant-or-self ::*/text()').extract())
                details = get_details(bb_res['name'])
                bb_res['status'] = details.samplestatus
                bb_res['description'] = details.shortdesc
                bb_res['standards'] = details.standards
                bb_res['rating'] = details.rating
                yield bb_res
