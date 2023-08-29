# 查询版本号
# 自动下载

# https://www.kaggle.com/datasets/Cornell-University/arxiv/download?datasetVersionNumber=141
# https://storage.googleapis.com/kaggle-data-sets/612177/6331255/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20230827%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230827T040224Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=ab19dcb63ebd57e03912b740a0c62d3364f384a354bf9adafd6ed96e8dc108b4511bdefb7fbdc9e5f9fff82fda90b34edbbe3a99b48c1f222a1d991d9ed22b03291acb7d433f4bdcde56c9fbc0779f74053bfd50d18577311fb348737c3916bcf040c4194cf75bad6a0e4d7706675b24ed7bcbfacfd7e21adf6f79628e172d2e5f553fe8997cf98c221a203044ddf741ab1cea1054095ee6d01be7674002b6a28e0fe62d767fe92e8c737cd532f8c764680215948577c3c08e3f5dcb5d595ab042d7c49f925f903a757f35ebac9cb3b3ef64f4723da9035e989f57230eb6fcf3d0d18a96399bc80b6158e9fceedace7c1907a48d6b0e76aab677a777d45dce36

# 更新版本号
# ToDo

# ---------------------------
# 根据id，查找差量
# /home/lc/Arxiv/141/arxiv-metadata-oai-snapshot.json
# /home/lc/Arxiv/arxiv-metadata-oai-snapshot.json
import logging
from tqdm import tqdm
import pymysql
from datetime import datetime

from datasets import load_dataset
from datasets.utils.info_utils import VerificationMode

old_data = load_dataset("/home/lc/code/database_papers/arxiv_dataset", data_dir="/home/lc/Arxiv/", verification_mode=VerificationMode.NO_CHECKS)
new_data = load_dataset("/home/lc/code/database_papers/arxiv_dataset", data_dir="/home/lc/Arxiv/141/", verification_mode=VerificationMode.NO_CHECKS)
print(old_data['train'][0]['id'])
# print(all_data['train'][0])
# print(len(all_data['train']))
all_old_id = {}
for data_id in tqdm(old_data['train']):
    did = data_id['id']
    # print(did)
    # break
    all_old_id[did] = True

print("len:", len(all_old_id))

print("len old_data:", len(old_data['train']))
diff_data = new_data.filter(lambda x: x["id"] not in all_old_id)
print("len diff_data:", len(diff_data['train']))

# exit()
# 更新MySQL

format = "%Y-%m-%d"
conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="lc",
    password="abc12345",
    database="paper_default",
    charset="utf8"
)

sql = "insert into paper_base \
    (is_del, p_id_uni, p_submitter, p_authors, p_title, p_comments, p_journal_ref, p_doi, p_report_no, p_categories, p_license, p_abstract, p_update_date, p_versions) \
    values(%r, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
logging.basicConfig(filename="sql.log", level=logging.DEBUG)

step = 10
if True:
    for idx in tqdm(range(0, len(diff_data['train']), step)):
        if idx <= 23077:
            continue
        datas = []
        tmp_data = diff_data['train'][idx:idx+step]
        # print("tmp_data:", tmp_data)
        for i in range(0, len(tmp_data['id'])):
            td = []
            td.append(0)
            td.append(str(tmp_data['id'][i]))
            td.append(str(tmp_data['submitter'][i]))
            td.append(str(tmp_data['authors'][i]))
            td.append(str(tmp_data['title'][i]))
            td.append(str(tmp_data['comments'][i]))
            td.append(str(tmp_data['journal-ref'][i]))
            td.append(str(tmp_data['doi'][i]))
            td.append(str(tmp_data['report-no'][i]))
            td.append(str(tmp_data['categories'][i]))
            td.append(str(tmp_data['license'][i]))
            td.append(str(tmp_data['abstract'][i]))
            td.append(str(tmp_data['versions'][i]))
            td.append(str(tmp_data['update_date'][i]))
            datas.append(td)
        try:
            with conn.cursor() as cursor:
                rows = cursor.executemany(sql, datas)
            conn.commit()

        except pymysql.MySQLError as err:
            conn.rollback()
            # print(type(err), err)
            log_str = "insert failed " + ",".join([d[1] for d in datas])
            logging.info(log_str)
            logging.debug(log_str)

        # break
    


# 更新ES

from elasticsearch import Elasticsearch
from elasticsearch import helpers

from datasets.utils.info_utils import VerificationMode

from sentence_transformers import SentenceTransformer, util


acc_token = "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"
sentences = ["This is an example sentence", "Each sentence is converted"]
model = SentenceTransformer('all-MiniLM-L6-v2', use_auth_token=acc_token)
# embeddings = model.encode(sentences)
# print("length of embeddings: {}, dims: {}".format(len(embeddings), len(embeddings[0])))
# print("emb:", embeddings)

cafile1 = "/etc/elasticsearch/certs/http_ca.crt"

es = Elasticsearch(hosts=["https://127.0.0.1:9200"], basic_auth=("elastic", "abc12345"), ca_certs=cafile1, verify_certs=True)
print("es test", es.ping())

step = 10
if True:
    len_a = len(diff_data['train'])
    # for idx in tqdm(range(0, len(all_data['train']), step)):
    for idx in tqdm(range(0, len_a, step)):
        print("-----------", idx, len_a, idx / len_a)
        datas = []
        tmp_data = diff_data['train'][idx:idx+step]
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
    