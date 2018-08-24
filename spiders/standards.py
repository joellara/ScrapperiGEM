import ahocorasick
import collections
#Restriction sites
EcoRI = ('EcoRI','GAATTC',len('GAATTC'))
XbaI = ('XbaI','TCTAGA',len('TCTAGA'))
SpeI = ('SpeI','ACTAGT',len('ACTAGT'))
PstI = ('PstI','CTGCAG',len('CTGCAG'))
NotI = ('NotI','GCGGCCGC',len('GCGGCCGC'))
NheI = ('NheI','GCTAGC',len('GCTAGC'))
PvuII = ('PvuII','CAGCTG',len('CAGCTG'))
XhoI = ('XhoI','CTCGAG',len('CTCGAG'))
AvrII = ('AvrII','CCTAGG',len('CCTAGG'))
SapI = ('SapI','GCTCTTC',len('GCTCTTC'))
SapI_2 = ('SapI_2','GAAGAGC',len('GAAGAGC'))
BglII = ('BglII','AGATCT',len('AGATCT'))
BamHI = ('BamHI','GGATCC',len('GGATCC'))
NgoMIV = ('NgoMIV','GCCGGC',len('GCCGGC'))
AgeI = ('AgeI','ACCGGT',len('ACCGGT'))

RestrictionEnzimes = set([EcoRI,XbaI,SpeI,PstI,NotI,NheI,PvuII,XhoI,AvrII,SapI,SapI_2,BglII,BamHI,NgoMIV,AgeI])

#declare Standards
RFC10 = dict()
RFC10['name'] = 'RFC10'
RFC10['illegal'] = [EcoRI,XbaI,SpeI,PstI]
RFC10['avoid'] = [NotI]
RFC10['prefix'] = EcoRI[1] + NotI[1] + 'T' + XbaI[1] + 'G'
RFC10['prefix2'] = EcoRI[1] + NotI[1] + 'T' + 'TCTAG'
RFC10['suffix'] = 'T' + SpeI[1] + 'A' + NotI[1] + PstI[1]
RFC10['scar'] = 'TACTAGAG'
RFC10['scar2'] = 'TACTAG'

RFC12 = dict()
RFC12['name'] = 'RFC12'
RFC12['illegal'] = [EcoRI,SpeI,NheI,PstI,NotI]
RFC12['avoid'] = [PvuII,XhoI,AvrII,XbaI,SapI,SapI_2]
RFC12['prefix'] = 'GTTTCTTCGAATTCGCGGCCGCACTAGA'
RFC12['suffix'] = 'GTTTCTTCCTGCAGCGGCCGCGCTAGC'

RFC21 = dict()
RFC21['name'] = 'RFC21'
RFC21['illegal'] = [EcoRI,BglII,BamHI,XhoI]
RFC21['prefix'] = EcoRI[1] + 'ATG' + BglII[1]
RFC21['suffix'] = BamHI[1] + 'TAA' + XhoI[1]
RFC12['scar'] = 'GGATCT'

RFC23 = dict()
RFC23['name'] = 'RFC23'
RFC23['illegal'] = [EcoRI,XbaI,SpeI,PstI,NotI]
RFC23['prefix'] = EcoRI[1] + NotI[1] + 'T' + XbaI[1]
RFC23['suffix'] = SpeI[1] + 'A' + NotI[1] + PstI[1]
RFC23['scar'] = 'ACTAGA'

RFC25 = dict()
RFC25['name'] = 'RFC25'
RFC25['illegal'] = [EcoRI,XbaI,NgoMIV,AgeI,SpeI,PstI,NotI]
RFC25['prefix'] = EcoRI[1] + NotI[1] + 'T' + XbaI[1] + 'TG' + NgoMIV[1]
RFC25['suffix'] = AgeI[1] + 'TAAT' + SpeI[1] + 'A' + NotI[1] + PstI[1]
RFC25['N-Parts-prefix'] = EcoRI[1] + NotI[1] + 'T' + XbaI[1]
RFC25['N-Parts-suffix'] = AgeI[1] + 'TAAT' + SpeI[1] + 'A' + NotI[1] + PstI[1]

Standards = [RFC10,RFC12,RFC21,RFC23,RFC25]
StandardsNames = set(['RFC10','RFC12','RFC21','RFC23','RFC25'])

def check_standards(seq):
    """ """
    seq.replace(" ",'')
    seq = seq.upper()
    keyword_processor = ahocorasick.Automaton()
    for restriction in RestrictionEnzimes:
        keyword_processor.add_word(restriction[1],restriction)
    keyword_processor.make_automaton()

    noncompatible_stds = set()
    for item in keyword_processor.iter(seq):
        for std  in Standards:
            if item[1] in std['illegal']:
                noncompatible_stds.add(std['name'])
                break
    return StandardsNames.difference(noncompatible_stds)
