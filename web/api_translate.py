# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5
import time

# Set your own appid/appkey.
appid = '20230921001824590'
appkey = 'bWyopasL59UjYY0MWBa8'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'en'
to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

salt = random.randint(32768, 65536)
sign = make_md5(appid + query + str(salt) + appkey)

# Build request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

# # Send request
# r = requests.post(url, params=payload, headers=headers)
# result = r.json()

# # Show response
# print(json.dumps(result, indent=4, ensure_ascii=False))


def tran_en(query):
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    payload = {'appid': appid, 'q': query, 'from': "en", 'to': "zh", 'salt': salt, 'sign': sign}
    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    res_list = []
    if "error_code" in result:
        if result['error_code'] == 54003:
            time.sleep(1)
            r = requests.post(url, params=payload, headers=headers)
            
    if "trans_result" not in result:
        return "err:"+ str(result['error_code'])
    for res in result['trans_result']:
        res_list.append(res['dst'])
    # return result
    return ".".join(res_list)

def tran_zh(query):
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    payload = {'appid': appid, 'q': query, 'from': "zh", 'to': "en", 'salt': salt, 'sign': sign}
    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    res_list = []
    if "error_code" in result:
        if result['error_code'] == 54003:
            time.sleep(1)
            r = requests.post(url, params=payload, headers=headers)
            
    if "trans_result" not in result:
        return "err:"+ str(result['error_code'])
    for res in result['trans_result']:
        res_list.append(res['dst'])
    # return result
    return ".".join(res_list)

def tran_auto(query):
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    payload = {'appid': appid, 'q': query, 'from': "auto", 'to': "en", 'salt': salt, 'sign': sign}
    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    res_list = []
    if "error_code" in result:
        if result['error_code'] == 54003:
            time.sleep(1)
            r = requests.post(url, params=payload, headers=headers)
            
    if "trans_result" not in result:
        return ""
    for res in result['trans_result']:
        res_list.append(res['dst'])
    # return result
    return ".".join(res_list)

def tran_auto_2_zh(query):
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    payload = {'appid': appid, 'q': query, 'from': "auto", 'to': "zh", 'salt': salt, 'sign': sign}
    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    res_list = []
    if "error_code" in result:
        if result['error_code'] == 54003:
            time.sleep(1)
            r = requests.post(url, params=payload, headers=headers)
            
    if "trans_result" not in result:
        return ""
    for res in result['trans_result']:
        res_list.append(res['dst'])
    # return result
    return ".".join(res_list)

# import time
# time.sleep(1)
# print(tran_zh("如何使用GPT大模型自动生成prompt"))
# time.sleep(1)
# print(tran_en("how to auto gen prompt by gpt"))
# print(tran_auto("如何使用GPT大模型自动生成prompt"))
# time.sleep(1)