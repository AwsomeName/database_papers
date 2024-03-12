# coding=utf-8

import json
import os
import logging
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch import helpers


logging.basicConfig(filename="es.log", level=logging.DEBUG)

cafile1 = "/etc/elasticsearch/certs/http_ca.crt"

es = Elasticsearch(hosts=["https://127.0.0.1:9200"], basic_auth=("elastic", "abc12345"), ca_certs=cafile1, verify_certs=True)
print(es.ping())

doc = {
    "mappings": {
        "properties": {
            "id": {
                "type": "text",
            },
            "name": {
                "type": "text",
            },
            "alias_name": {
                "type": "text",
            },
            "full_name": {
                "type": "text",
            },
            "spec": {
                "type": "text",
            },
            "props": {
                "type": "text",
            },
            "prop_str": {
                "type": "text",
            },
        }
    }
}

index_name = "kg_ver_0_1"
# es.indices.delete(index=index_name)
if es.indices.exists(index=index_name):
    try:
        res = es.get(index=index_name, id="54808e2fdac760238002ef26ec3e1090ef5f1b766b6f64fb9b4d30e8e78e0bf8")
        print(res)
    except:
        pass
    es.indices.delete(index=index_name)
else:
    print("索引不存在")

res = es.indices.create(index=index_name, body=doc)
print(res)
# exit()
    

all_data = []
print("loading ...")
with open("/home/lc/data/all_entities.txt", 'r') as fp:
    for line in fp.readlines():
        line = line.strip()
        all_data.append(line)
        # break

print("insert ...")
step = 20
if True:
    len_a = len(all_data)
    for idx in tqdm(range(0, len_a, step)):
        datas = []
        tmp_data = all_data[idx:idx+step]
        # print("tmp_data:", tmp_data)
        for i in range(0, len(tmp_data)):
            data = tmp_data[i]
            ea_info = json.loads(data)
            e_id, e_info = ea_info
            
            td = {}
            td['_index'] = index_name
            td['_id'] = e_id
            src = {}
            src['id'] = e_id
            src['name'] = e_info['name']
            src['full_name'] = e_info['full_name']
            src['alias_name'] = ",".join(e_info['alias_name'])
            src['spec'] = e_info['spec']
            del e_info['name']
            del e_info['full_name']
            del e_info['spec']
            src['props'] = json.dumps(e_info)
            prop_str = ""
            for key in e_info:
                prop_str += key + ":"
                prop_str += ",".join(e_info[key])
                prop_str += "; "
            src['prop_str'] = prop_str
            td["_source"] = src
            # print("-----")
            # print(td)
            datas.append(td)
      
        # break
        helpers.bulk(es, datas)
        # break
    