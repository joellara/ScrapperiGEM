import scrapy
import requests
import xml.etree.ElementTree as etree
import json
from enum import Enum
from helper import get_details


class Type(Enum):
    ConstitutiveAnderson = 1
    ConstitutiveCommunity = 2
    RegulatedProkaryotic = 3
    ConstitutiveCustom = 4
    Yeast = 5


class RBSSpider(scrapy.Spider):
    name = "RBS Spider"

    def start_requests(self):
        # Constitutive prokaryotic RBS
        yield scrapy.Request(url='http://parts.igem.org/Ribosome_Binding_Sites/Prokaryotic/Constitutive/Anderson', callback=self.parse_constitutive_anderson)
        yield scrapy.Request(url='http://parts.igem.org/Ribosome_Binding_Sites/Prokaryotic/Constitutive/Community_Collection', callback=self.parse_constitutive_community)
        # Regulated Prokaryotic RBS (Riboregulators)
        yield scrapy.Request(url='http://parts.igem.org/Ribosome_Binding_Sites/Prokaryotic/Regulated/Isaacs', callback=self.parse_regulated_prokaryotic)
        # Constitutive Custom RBS
        yield scrapy.Request(url='http://parts.igem.org/Ribosome_Binding_Sites/Custom/Constitutive/Rackham', callback=self.parse_constitutive_custom)
        # Yeast
        yield scrapy.Request(url='http://parts.igem.org/Ribosome_Binding_Sites/Catalog', callback=self.parse_yeast)

    def parse_webpage(self, response, type):
        if type == Type.Yeast:
            table = response.xpath('//table[@id="assembly_plasmid_table"]')[0]
        else:
            table = response.xpath('//table[@class="wikitable"]')[0]
        num = 0
        biobricks = table.xpath('tr')
        for bb in biobricks[1:]:
            bb_res = dict()
            bb_res['name'] = bb.xpath('td').xpath('a/text()').extract_first()
            # Specific webpage
            if type == Type.ConstitutiveAnderson:
                if num == 0 or num == 1:
                    num = num + 1
                    continue
                bb_res['type'] = "Constitutive Anderson Library"
                bb_res['chassis'] = "Prokaryotic"
            elif type == Type.ConstitutiveCommunity:
                if num == 0:
                    num = num + 1
                    continue
                bb_res['type'] = "Constitutive Community Collection"
                bb_res['chassis'] = "Prokaryotic"
            elif type == Type.RegulatedProkaryotic:
                bb_res['type'] = "Regulated Prokaryotic"
                bb_res['chassis'] = "Prokaryotic"
            elif type == Type.ConstitutiveCustom:
                bb_res['type'] = "Constitutive Custom"
                bb_res['chassis'] = "Prokaryotic"
            elif type == Type.Yeast:
                bb_res['type'] = "Yeast"
                bb_res['chassis'] = "Eukaryote"

            details = get_details(bb_res['name'])
            bb_res['experience'] = details.rating
            bb_res['standards'] = details.standards
            bb_res['status'] = details.samplestatus
            bb_res['description'] = details.shortdesc
            yield bb_res
        num = num + 1

    def parse_constitutive_anderson(self, response):
        return self.parse_webpage(response, Type.ConstitutiveAnderson)

    def parse_constitutive_community(self, response):
        return self.parse_webpage(response, Type.ConstitutiveCommunity)

    def parse_regulated_prokaryotic(self, response):
        return self.parse_webpage(response, Type.RegulatedProkaryotic)

    def parse_constitutive_custom(self, response):
        return self.parse_webpage(response, Type.ConstitutiveCustom)

    def parse_yeast(self, response):
        return self.parse_webpage(response, Type.Yeast)
