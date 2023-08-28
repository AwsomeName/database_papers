# coding=utf-8

import json
from tqdm import tqdm

from datasets import load_dataset
from datasets.utils.info_utils import VerificationMode


all_data = load_dataset("/home/lc/code/database_papers/arxiv_dataset", data_dir="/home/lc/Arxiv/", verification_mode=VerificationMode.NO_CHECKS)
# print(all_data['train'][0])
# print(len(all_data['train']))

train_data = all_data['train']
# for idx in range(len(all_data['train'])):
len_cnt = {}
for idx in range(0, len(train_data)):
    # print(train_data[idx]['abstract'])
    ab_len = len(train_data[idx]['abstract'].split(" "))
    if ab_len in len_cnt:
        len_cnt[ab_len] += 1
    else:
        len_cnt[ab_len] = 1


with open("cnt.txt", 'w') as wp:
    json.dump(len_cnt, wp)

print(len_cnt)
