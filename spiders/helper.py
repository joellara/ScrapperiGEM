import requests
import xml.etree.ElementTree as etree
from standards import check_standards
from collections import namedtuple
PartDetails = namedtuple(
    'PartDetails', 'standards, rating, regulation, samplestatus, shortdesc')


def get_details(bbName):
    response = requests.get(
        'http://parts.igem.org/cgi/xml/part.cgi?part='+bbName)
    root = etree.fromstring(response.content)
    part = root[0][0]
    seq = part.find('sequences').find('seq_data').text
    sample_status = part.find('sample_status').text
    #status = part.find('release_status').text
    part_short_desc = part.find('part_short_desc').text
    rating = part.find('part_rating').text or part.find(
        'part_results').text or "No results"
    multiple = part.find('categories').findall("category")
    regulation = None
    for mul in multiple:
        if mul.text == "//regulation/multiple":
            regulation = "Multiple"
    seq = "".join(seq.split())
    seq.replace('\n', '')
    seq = seq.upper()
    details = PartDetails(standards=check_standards(seq), rating=rating,
                          regulation=regulation, samplestatus=sample_status, shortdesc=part_short_desc)
    return details
