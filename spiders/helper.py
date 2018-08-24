import requests
import xml.etree.ElementTree as etree
from standards import check_standards

def get_details( bbName):
    response = requests.get('http://parts.igem.org/cgi/xml/part.cgi?part='+bbName)
    root = etree.fromstring(response.content)
    part = root[0][0]
    seq = part.find('sequences').find('seq_data').text
    status = part.find('release_status').text
    seq = "".join(seq.split())
    seq.replace('\n','')
    seq = seq.upper()
    return (check_standards(seq),status)
