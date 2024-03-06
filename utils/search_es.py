# coding=utf-8

import logging
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer, util


logging.basicConfig(filename="es.log", level=logging.DEBUG)
acc_token = "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"
# sentences = ["This is an example sentence", "Each sentence is converted"]
# sentences = ["如何增加大模型的处理窗口长度"]
# sentences = ["CODET: CODE GENERATION WITH GENERATED TESTS"]
sentences = ["auto generate prompt using gpt for special task"]
# sentences = ["Using the GPT large model to handle more complex tasks"]
# sentences = ["How to Use Large Models to Process Longer Text"]
# sentences = ["how to use the big gpt model to process diffcult problom"]
# model = SentenceTransformer('sentence-transformes/all-MiniLm-L6-v2')
model = SentenceTransformer('all-MiniLM-L6-v2', use_auth_token=acc_token)
embeddings = model.encode(sentences)[0]
# print("length of embeddings: {}, dims: {}".format(len(embeddings), len(embeddings[0])))
# print("emb:", embeddings)


cafile1 = "/etc/elasticsearch/certs/http_ca.crt"

es = Elasticsearch(hosts=["https://127.0.0.1:9200"], basic_auth=("elastic", "abc12345"), ca_certs=cafile1, verify_certs=True)
print(es.ping())


res = es.knn_search(
    index = "paper_title_emb",
    source = ["title", "abstract"],
    knn = {
        "field": "ab_emb",
        "k": 5,
        "num_candidates": 10,
        "query_vector": embeddings
    }
)

# print(res)

title = [[x['_source'], x["_score"]]  for x in res['hits']['hits']] 
 
for item in title:
    print(item)

print("--------")

res = es.knn_search(
    index = "paper_title_emb",
    source = ["title", "abstract"],
    knn = {
        "field": "title_emb",
        "k": 5,
        "num_candidates": 10,
        "query_vector": embeddings
    }
)

title = [[x['_source'], x["_score"]]  for x in res['hits']['hits']] 
 
for item in title:
    print(item)