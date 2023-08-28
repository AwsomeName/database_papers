# coding=utf-8

"""arXiv Dataset."""


import json
import os
import logging
from tqdm import tqdm

from datasets import load_dataset
from datasets.utils.info_utils import VerificationMode

# all_data = load_dataset("arxiv_dataset", data_dir="/home/lc/Arxiv/")
# all_data = load_dataset("/home/lc/Arxiv/arxiv_dataset", data_dir="/home/lc/Arxiv/")
# all_data = load_dataset("/home/lc/Arxiv/arxiv_dataset", data_dir="/home/lc/Arxiv/", verification_mode=VerificationMode.NO_CHECKS)
all_data = load_dataset("/home/lc/code/database_papers/arxiv_dataset", data_dir="/home/lc/Arxiv/", verification_mode=VerificationMode.NO_CHECKS)

# print(all_data['train'][0]['id'])
print(all_data['train'][0])
print(len(all_data['train']))

import pymysql
from datetime import datetime

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

step = 100
if True:
    for idx in tqdm(range(0, len(all_data['train']), step)):
        if idx <= 23077:
            continue
        datas = []
        tmp_data = all_data['train'][idx:idx+step]
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
    