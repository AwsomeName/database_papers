# coding=utf-8

import json
import os
import logging
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from datasets import load_dataset
from datasets.utils.info_utils import VerificationMode

from sentence_transformers import SentenceTransformer, util


logging.basicConfig(filename="es.log", level=logging.DEBUG)
acc_token = "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"
sentences = ["This is an example sentence", "Each sentence is converted"]
# model = SentenceTransformer('sentence-transformes/all-MiniLm-L6-v2')
model = SentenceTransformer('all-MiniLM-L6-v2', use_auth_token=acc_token)
embeddings = model.encode(sentences)
print("length of embeddings: {}, dims: {}".format(len(embeddings), len(embeddings[0])))
# print("emb:", embeddings)

def gen_emb():
    return 

cafile1 = "/etc/elasticsearch/certs/http_ca.crt"

es = Elasticsearch(hosts=["https://127.0.0.1:9200"], basic_auth=("elastic", "abc12345"), ca_certs=cafile1, verify_certs=True)
print(es.ping())

doc = {
    "mappings": {
        "properties": {
            "id": {
                "type": "text",
                # "index": True,
            },
            "submitter": {
                "type": "text",
                # "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
            "authors": {
                "type": "text",
                # "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
            "title": {
                "type": "text",
                # "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
            "comments": {
                "type": "text",
                # "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
            "journal-ref": {
                "type": "text",
                # "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
            "doi": {
                "type": "text",
                # "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
            "report-no": {
                "type": "text",
                # "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
            "categories": {
                "type": "text",
                # "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
            "license": {
                "type": "text",
                # "index": True,
            },
            "abstract": {
                "type": "text",
                # "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
            "ab_emb": {
                "type": "dense_vector",
                "index": True,
                "dims": 384,
                # "index": True,
                "similarity": "l2_norm"
            },
            "title_emb": {
                "type": "dense_vector",
                "index": True,
                "dims": 384,
                # "index": True,
                "similarity": "l2_norm"
            },
            "version": {
                "type": "text",
                # "index": True,
            },
            "update_date": {
                "type": "text",
                # "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
        }
    }
}

# es.indices.delete(index="paper_title_emb")
# if es.indices.exists(index="paper_emb"):
#     res = es.get(index="paper_emb", id="0704.0001")
#     print(res)
#     es.indices.delete(index="paper_emb")
# else:
#     print("索引不存在")

res = es.indices.create(index="paper_title_emb", body=doc)
print(res)
# exit()
    

all_data = load_dataset("/home/lc/code/database_papers/arxiv_dataset", data_dir="/home/lc/Arxiv/141", verification_mode=VerificationMode.NO_CHECKS)
print(all_data['train'][0])
print(len(all_data['train']))

# exit()
step = 10
if True:
    len_a = len(all_data['train'])
    # for idx in tqdm(range(0, len(all_data['train']), step)):
    for idx in tqdm(range(0, len_a, step)):
        print("-----------", idx, len_a, idx / len_a)
        datas = []
        tmp_data = all_data['train'][idx:idx+step]
        # print("tmp_data:", tmp_data)
        for i in range(0, len(tmp_data['id'])):
            td = {}
            td['_index'] = "paper_title_emb"
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
            # src['abstract'] = str(tmp_data['abstract'][i])
            abstract = str(tmp_data['abstract'][i])
            src['abstract'] = abstract
            # print("abstract:", abstract)
            ab_emb = model.encode([abstract])
            # print("ab_emb:", ab_emb)
            src['ab_emb'] = ab_emb[0]
            title = str(tmp_data['title'][i])
            title_emb = model.encode([title])
            src['title_emb'] = title_emb[0]
            src['versions'] = str(tmp_data['versions'][i])
            src['update_date'] = str(tmp_data['update_date'][i])
            td["_source"] = src
            datas.append(td)
      
        # break
        helpers.bulk(es, datas)
        # break
    