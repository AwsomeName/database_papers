# coding=utf-8

import json
import os
import logging
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from datasets import load_dataset
from datasets.utils.info_utils import VerificationMode


cafile1 = "/etc/elasticsearch/certs/http_ca.crt"

es = Elasticsearch(hosts=["https://127.0.0.1:9200"], basic_auth=("elastic", "abc12345"), ca_certs=cafile1, verify_certs=True)
print(es.ping())

# doc = {
#     "mappings": {
#         "properties": {
#             "name": {
#                 "type": "text"
#             },
#             "id": {
#                 "type": "text"
#             }
#         }
#     }
# }

if es.indices.exists(index="paper_base"):
    res = es.get(index="paper_base", id="0704.0001")
    print(res)
    es.indices.delete(index="paper_base")
else:
    print("索引不存在")

# res = es.indices.create(index="paper_base", body=doc)
# print(res)
# exit()
    
logging.basicConfig(filename="es.log", level=logging.DEBUG)

all_data = load_dataset("/home/lc/code/database_papers/arxiv_dataset", data_dir="/home/lc/Arxiv/", verification_mode=VerificationMode.NO_CHECKS)
print(all_data['train'][0])
print(len(all_data['train']))
step = 100
if True:
    for idx in tqdm(range(0, len(all_data['train']), step)):
        datas = []
        tmp_data = all_data['train'][idx:idx+step]
        # print("tmp_data:", tmp_data)
        for i in range(0, len(tmp_data['id'])):
            td = {}
            td['_index'] = "paper_base"
            # td['_type'] = "doc"
            # td.append(0)
            td['_id'] = str(tmp_data['id'][i])
            src = {}
            src['id'] = str(tmp_data['id'][i])
            src['submitter'] = str(tmp_data['submitter'][i])
            src['authors'] = str(tmp_data['authors'][i])
            src['title'] = str(tmp_data['title'][i])
            src['comments'] = str(tmp_data['comments'][i])
            src['journal-ref'] = str(tmp_data['journal-ref'][i])
            src['doi'] = str(tmp_data['doi'][i])
            src['report-no'] = str(tmp_data['report-no'][i])
            src['categories'] = str(tmp_data['categories'][i])
            src['license'] = str(tmp_data['license'][i])
            src['abstract'] = str(tmp_data['abstract'][i])
            src['versions'] = str(tmp_data['versions'][i])
            src['update_date'] = str(tmp_data['update_date'][i])
            td["_source"] = src
            datas.append(td)
      
        # break
        helpers.bulk(es, datas)
        # break
    