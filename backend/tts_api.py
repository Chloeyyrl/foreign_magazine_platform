
# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
import importlib

importlib.reload(sys)


YOUDAO_URL = 'https://openapi.youdao.com/ttsapi'
APP_KEY = '6dd2e289581eec52'
APP_SECRET = '1UsMhnrNgOnrNb7kXZrRNK5mdATSbftv'


def encrypt(signStr):
    hash_algorithm = hashlib.md5()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect():
    q = '''"Healthplex Expo 2024, Natural & Nutraceutical Products China 2024" (HNC), co-organized by CCCMHPIE and Sinoexpo Informa Markets, will be held during 19-21 June 2024 at the National Exhibition and Convention Center (NECC) in Shanghai. HNC expo will be co-located with Hi & Fi Asia-China, ProPak China & FoodPack China 2024, etc., forming a 200,000 sqm food industry chain event, and committed to providing a one-stop supplying and purchasing service platform of food industry from nutraceuticals, healthy natural ingredients, food ingredients, natural and plant-based products to food processing and packaging machinery. 

In 2023, with a total exhibition area of 150,000 square meters, the series shows took up 6 exhibition halls at NECC, brought together more than 2,000 well-known domestic and international exhibitors, presenting a comprehensive picture of the booming upgrading in the health industry.'''

    data = {}
    data['langType'] = 'en'
    salt = str(uuid.uuid1())
    signStr = APP_KEY + q + salt + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "testing_0508" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        print(response.content)


if __name__ == '__main__':
    connect()