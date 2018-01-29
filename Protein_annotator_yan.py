
import urllib.request
import requests
import json
from nltk.tokenize import sent_tokenize, word_tokenize
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def convone(ori, root, orianno, relations):
    # print(sent_tokenize(ss))
    global offset
    offset += 1
    # pos = orianno
    pos = []
    articalId = 0
    text = ''

    text = ori['text']
    articalId = ori['sourceid']
    for x in ori['denotations']:
        if x['span']['begin'] not in [i[0] for i in pos]:
            pos.append([x['span']['begin'], x['span']['end'], x['obj'][5:]])
    # print(x)
    # print(articalId)
    # print(pos)
    # print(text)
    pos.sort()
    # for x in pos:
    #     print(x[0], end='\t')
    # print()
    sentences = sent_tokenize(text)
    for x in range(len(sentences)):
        if x != 0:
            sentences[x] = ' ' + sentences[x]
        # print(len(sentences[x]), end='\t')
    # print()
    # a = ET.Element('sentence')
    # id = 'd' + articalId + ',s' +
    # c = ET.SubElement(a, 'child')
    # c.text = 'some text'
    # d = ET.SubElement(a, 'child2')
    # b = ET.Element('elem_b')
    # root = ET.Element('root')
    # root.extend((a, b))
    # tree = ET.ElementTree(root)
    # tree.write('ss/output.xml')

    senid = -1
    senlen = 0
    entid = 0
    id = ""
    isempty = True
    isfirst = 0
    geneset = {}
    # print(len(sentences))
    for x in pos:
        # print('x[0] and senlen: ', x[0], senlen)
        if x[0] >= senlen:
            # for i in geneset:
            #     if i in relations:
            #         for j in relations[i]:
            #             if j in geneset.keys():
            #                 for m in geneset[i]:
            #                     for n in geneset[j]:
            #                         if m != n:
            #                             rel = ET.SubElement(
            #                                 root[-1], 'interaction')
            #                             rel.set('e1', m)
            #                             rel.set('e2', n)
            geneset = {}
            while x[0] >= senlen:
                if senid < 0:
                    senid += 1
                    senlen += len(sentences[senid])
                    continue

                if isempty is True:
                    root.append(ET.Element('sentence'))
                    a = root[-1]
                    id = 'Gene.d' + str(articalId) + '.s' + str(senid + offset)
                    a.set('id', id)
                    a.set('text', sentences[senid])
                isempty = True

                senid += 1
                senlen += len(sentences[senid])
                # print('curlen and senlen: ', len(
                #     sentences[senid]) if senid >= 0 else 0, senlen)
            # if senid >= len(sentences):
            #     continue;
            isempty = False
            entid = 0
            root.append(ET.Element('sentence'))
            a = root[-1]
            id = "Gene.d" + str(articalId) + '.s' + str(senid + offset)
            # id = str(x[2]) + '.d' + str(articalId) + '.s' + str(senid +
            # offset)
            a.set('id', id)
            if sentences[senid][0] != ' ':
                isfirst = 0
                a.set('text', sentences[senid])
            else:
                isfirst = 1
                a.set('text', sentences[senid][1:])

            entity = ET.SubElement(a, 'entity')
            entity_id = str(x[2]).split(';')[0] + '.d' + str(articalId) + \
                '.s' + str(senid + offset) + '.e' + str(entid)
            entity.set('id', entity_id)
            # print('charOffset: ', str(x[0]) + '-' + str(x[1]))
            entity.set('charOffset', str(
                x[0] - (senlen - len(sentences[senid])) - isfirst) + '-' + str(x[1] - (senlen - len(sentences[senid])) - isfirst))
            entity.set('Gene', str(x[2]).split(';')[0])
            if str(x[2]).split(';')[0] not in geneset:
                geneset[str(x[2]).split(';')[0]] = [entity_id]
            else:
                geneset[str(x[2]).split(';')[0]].append(entity_id)
        else:
            a = root[-1]
            entid += 1

            entity = ET.SubElement(a, 'entity')
            entity_id = str(x[2]).split(';')[0] + '.d' + str(articalId) + \
                '.s' + str(senid + offset) + '.e' + str(entid)
            entity.set('id', entity_id)
            # print('charOffset: ', str(x[0]) + '-' + str(x[1]))
            entity.set('charOffset', str(
                x[0] - (senlen - len(sentences[senid])) - isfirst) + '-' + str(x[1] - (senlen - len(sentences[senid])) - isfirst))
            entity.set('Gene', str(x[2]).split(';')[0])
            if str(x[2]).split(';')[0] not in geneset:
                geneset[str(x[2]).split(';')[0]] = [entity_id]
            else:
                geneset[str(x[2]).split(';')[0]].append(entity_id)
    # for i in geneset:
    #     if i in relations:
    #         for j in relations[i]:
    #             if j in geneset.keys():
    #                 for m in geneset[i]:
    #                     for n in geneset[j]:
    #                         if m != n:
    #                             rel = ET.SubElement(
    #                                 root[-1], 'interaction')
    #                             rel.set('e1', m)
    #                             rel.set('e2', n)
    offset += senid


offset = 0
root = ET.Element('root')
with open('PMtask_Relations_TestSet.json', 'r') as orifile:
    ori = json.load(orifile)
    cnt = 0
    aa = 0
    for compo in ori['documents']:
        if aa == 2:
            break
        #aa += 1
        result = []
        orianno = []
        relations = {}
        # for x in compo['passages']:
        #     for i in x['annotations']:
        #         orianno.append([i['locations'][0]['offset'], i['locations'][0][
        #                        'offset'] + i['locations'][0]['length'], i['infons']['NCBI GENE']])
        # for i in compo['relations']:
        #     if i['infons']['Gene1'] in relations:
        #         relations[i['infons']['Gene1']].append(i['infons']['Gene2'])
        #     else:
        #         relations[i['infons']['Gene1']] = [i['infons']['Gene2']]

        # try:
        url = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Gene/" + \
            compo['id'] + "/json/"
        # url = 'https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Gene/17012600/json/'
        print(compo['id'])
        sock = urllib.request.urlopen(url)
        htmlSource = sock.read()
        sock.close()
        # print(htmlSource)
        toolfile = json.loads(htmlSource.decode('utf-8'))
        convone(toolfile, root, orianno, relations)
        # except Exception as e:
        #     cnt += 1
        #     print(str(e))

tree = ET.ElementTree(root)
tree.write('outputxxxxxx.xml')
print(cnt)
