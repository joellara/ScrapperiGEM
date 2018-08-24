import scrapy
import requests
import json
from enum import Enum
from helper import get_details

    # Constitutive = 1
    # InducibleEColi = 2
    # InducibleBSubtilis = 3
    # InducibleMiscProkaryote = 4
    # InducibleYeast = 5
    # InducibleMiscEukaryote = 6
    # RepressibleEColi = 7
    # RepressibleBSubtilis = 8
    # RepressiblePhageT7 = 9
    # RepressibleYeast = 10
    # RepressibleMiscEukaryote = 11
class Type(Enum):
    Constitutive = 1
    InducibleEColi = 2
    InducibleBSubtilis = 3
    InducibleMiscProkaryote = 4
    InducibleYeast = 5
    InducibleMiscEukaryote = 6
    RepressibleEColi = 7
    RepressibleBSubtilis = 8
    RepressiblePhageT7 = 9
    RepressibleYeast = 10
    RepressibleMiscEukaryote = 11


class PromoterSpider(scrapy.Spider):
    name = "Promoters Spider"

    def start_requests(self):
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/Constitutive', callback=self.parse_constitutive)
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/Ecoli/Positive', callback=self.parse_inducible_ecoli)
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/B._subtilis/Positive', callback=self.parse_inducible_bsubtilis)
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/Prokaryote/Miscellaneous/Positive', callback=self.parse_inducible_miscprokaryote)
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/Yeast/Positive', callback=self.parse_inducible_yeast)
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/Eukaryotic/Positive', callback=self.parse_inducible_misceukaryote)
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/Ecoli/Repressible', callback=self.parse_repressible_ecoli)
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/B._subtilis/Repressible', callback=self.parse_repressible_bsubtilis)
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/T7/Repressible', callback=self.parse_repressible_phageT7)
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/Yeast/Repressible', callback=self.parse_repressible_yeast)
        yield scrapy.Request(url='http://parts.igem.org/Promoters/Catalog/Eukaryotic/Repressible', callback=self.parse_repressible_misceukaryote)


    def parse_webpage(self, response, type):
        tables = response.xpath('//table[@id="assembly_plasmid_table"]')
        num = 0
        for table in tables:
            biobricks = table.xpath('tr')
            for bb in biobricks[1:]:
                bb_res = dict()
                bb_res['name'] = bb.xpath('td').xpath('a/text()').extract_first()
                bb_res['desc'] = "".join(bb.xpath('td[@class="c_2"]/descendant-or-self ::*/text()').extract())
                bb_res['status'] = bb.xpath('td[@class="c_8"]/text()').extract_first()
                if bb_res['status'] != 'In stock':
                    continue
                ### Specific webpage
                if type == Type.Constitutive:
                    self.constitutive(bb_res, num)
                elif type == Type.InducibleEColi:
                    self.inducible_ecoli(bb_res, num)
                elif type == Type.InducibleBSubtilis:
                    self.inducible_bsubtilis(bb_res, num)
                elif type == Type.InducibleMiscProkaryote:
                    self.inducible_miscprokaryote(bb_res, num)
                elif type == Type.InducibleYeast:
                    self.inducible_yeast(bb_res, num)
                elif type == Type.InducibleMiscEukaryote:
                    self.inducible_misceukaryote(bb_res, num)
                elif type == Type.RepressibleEColi:
                    self.repressible_ecoli(bb_res, num)
                elif type == Type.RepressibleBSubtilis:
                    self.repressible_bsubtilis(bb_res, num)
                elif type == Type.RepressiblePhageT7:
                    self.repressible_phageT7(bb_res, num)
                elif type == Type.RepressibleYeast:
                    self.repressible_yeast(bb_res, num)
                elif type == Type.RepressibleMiscEukaryote:
                    self.repressible_misceukaryote(bb_res, num)

                details = get_details(bb_res['name'])
                bb_res['standards'] = details[0]
                yield bb_res
            num = num + 1

    def parse_constitutive(self, response):
        return self.parse_webpage(response,Type.Constitutive)

    def parse_inducible_ecoli(self, response):
        return self.parse_webpage(response,Type.InducibleEColi)

    def parse_inducible_bsubtilis(self, response):
        return self.parse_webpage(response,Type.InducibleBSubtilis)

    def parse_inducible_miscprokaryote(self, response):
        return self.parse_webpage(response,Type.InducibleMiscProkaryote)

    def parse_inducible_yeast(self, response):
        return self.parse_webpage(response,Type.InducibleYeast)

    def parse_inducible_misceukaryote(self, response):
        return self.parse_webpage(response,Type.InducibleMiscEukaryote)

    def parse_repressible_ecoli(self, response):
        return self.parse_webpage(response,Type.RepressibleEColi)

    def parse_repressible_bsubtilis(self, response):
        return self.parse_webpage(response,Type.RepressibleBSubtilis)

    def parse_repressible_phageT7(self, response):
        return self.parse_webpage(response,Type.RepressiblePhageT7)

    def parse_repressible_yeast(self, response):
        return self.parse_webpage(response,Type.RepressibleYeast)

    def parse_repressible_misceukaryote(self, response):
        return self.parse_webpage(response,Type.RepressibleMiscEukaryote)

    def constitutive(self,bb, num):
        if num < 3:
            bb['chasis'] = 'E.coli'
        elif num < 5:
            bb['chasis'] = 'B. subtilis'
        elif num < 6:
            bb['chasis'] = 'Misc. prokaryotes'
        elif num < 7:
            bb['chasis'] = 'Bacteriophage T7'
        elif num < 8:
            bb['chasis'] = 'Bacteriophage SP6'
        elif num < 9:
            bb['chasis'] = 'Yeast'
        elif num < 10:
            bb['chasis'] = 'Misc. Eukaryotes'
        bb['regulation'] = 'Constitutive'
        if num == 0:
            bb['sigma_factor'] = 'Sigma 70'
        elif num == 1:
            bb['sigma_factor'] = 'Sigma S'
        elif num == 2:
            bb['sigma_factor'] = 'Sigma 32'
        elif num == 3:
            bb['sigma_factor'] = 'Sigma A'
        elif num == 4:
            bb['sigma_factor'] = 'Sigma B'

    def inducible_ecoli(self,bb, num):
        bb['chasis'] = 'E.coli'
        bb['regulation'] = 'Inducible'
        if num == 0:
            bb['sigma_factor'] = 'Sigma 70'
        elif num == 1:
            bb['sigma_factor'] = 'Sigma S'
        elif num == 2:
            bb['sigma_factor'] = 'Sigma 32'
        elif num == 3:
            bb['sigma_factor'] = 'Sigma 54'

    def inducible_bsubtilis(self,bb, num):
        bb['chasis'] = 'B. subtilis'
        bb['regulation'] = 'Inducible'
        if num == 0:
            bb['sigma_factor'] = 'Sigma A'
        elif num == 1:
            bb['sigma_factor'] = 'Sigma B'

    def inducible_miscprokaryote(self,bb, num):
        bb['chasis'] = 'Misc. Prokaryote'
        bb['regulation'] = 'Inducible'

    def inducible_yeast(self,bb, num):
        bb['chasis'] = 'Yeast'
        bb['regulation'] = 'Inducible'

    def inducible_misceukaryote(self,bb, num):
        bb['chasis'] = 'Misc. Eukaryote'
        bb['regulation'] = 'Inducible'

    def repressible_ecoli(self, bb, num):
        bb['chasis'] = 'E.coli'
        bb['regulation'] = 'Repressible'

        if num == 0:
            bb['sigma_factor'] = 'Sigma 70'
        elif num == 1:
            bb['sigma_factor'] = 'Sigma S'
        elif num == 2:
            bb['sigma_factor'] = 'Sigma 32'
        elif num == 3:
            bb['sigma_factor'] = 'Sigma 54'

    def repressible_bsubtilis(self,bb, num):
        bb['chasis'] = 'B. subtilis'
        bb['regulation'] = 'Repressible'
        bb['sigma_factor'] = 'Sigma Alpha'

    def repressible_phageT7(self,bb, num):
        bb['chasis'] = 'Bacteriophage T7'
        bb['regulation'] = 'Repressible'

    def repressible_yeast(self,bb, num):
        bb['chasis'] = 'Yeast'
        bb['regulation'] = 'Repressible'

    def repressible_misceukaryote(self,bb, num):
        bb['chasis'] = 'Misc. Eukaryote'
        bb['regulation'] = 'Repressible'
