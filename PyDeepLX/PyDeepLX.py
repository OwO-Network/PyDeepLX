'''
Author: Vincent Young
Date: 2023-04-27 00:44:01
LastEditors: Vincent Young
LastEditTime: 2023-05-21 03:45:32
FilePath: /PyDeepLX/PyDeepLX/PyDeepLX.py
Telegram: https://t.me/missuo

Copyright © 2023 by Vincent, All Rights Reserved. 
'''
import random
import time
import json
import httpx
from langdetect import detect


deeplAPI = "https://www2.deepl.com/jsonrpc"
headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "x-app-os-name": "iOS",
    "x-app-os-version": "16.3.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "x-app-device": "iPhone13,2",
    "User-Agent": "DeepL-iOS/2.6.0 iOS 16.3.0 (iPhone13,2)",
    "x-app-build": "353933",
    "x-app-version": "2.6",
    "Connection": "keep-alive"
}


class TooManyRequestsException(Exception):
    "Raised when there is a 429 error"
    def __str__(self):
        return "PyDeepLX Error: Too many requests, your IP has been blocked by DeepL temporarily, please don't request it frequently in a short time."


def detectLang(translateText) -> str:
    language = detect(translateText)
    return language.upper()

def getICount(translateText) -> int:
    return translateText.count('i')


def getRandomNumber() -> int:
    random.seed(time.time())
    num = random.randint(8300000, 8399998)
    return num * 1000


def getTimestamp(iCount: int) -> int:
    ts = int(time.time() * 1000)
    if iCount != 0:
        iCount += 1
        return ts - ts % iCount + iCount
    else:
        return ts


def translate(text, sourceLang=None, targetLang=None, needAlternative=False, printResult=False, proxies=None):
    iCount = getICount(text)
    id = getRandomNumber()
    if sourceLang == None:
        sourceLang = detectLang(text)
    if targetLang == None:
        targetLang = "EN"

    postData = {
        "jsonrpc": "2.0",
        "method": "LMT_handle_texts",
        "id": id,
        "params": {
            "texts": [{
                "text": text,
                "requestAlternatives": 3
            }],
            "splitting": "newlines",
            "lang": {
                "source_lang_user_selected": sourceLang,
                "target_lang": targetLang,
            },
            "timestamp": getTimestamp(iCount),
            "commonJobParams": {
                "wasSpoken": False,
                "transcribe_as": "",
            }}
    }
    postDataStr = json.dumps(postData, ensure_ascii=False)

    if (id+5) % 29 == 0 or (id+3) % 13 == 0:
        postDataStr = postDataStr.replace(
            "\"method\":\"", "\"method\" : \"", -1)
    else:
        postDataStr = postDataStr.replace(
            "\"method\":\"", "\"method\": \"", -1)
        
    # Add proxy (e.g. proxies='socks5://127.0.0.1:9150')
    with httpx.Client(proxies=proxies) as client:
        resp = client.post(url=deeplAPI, data=postDataStr, headers=headers)
        respStatusCode = resp.status_code
        respText = resp.text
        respJson = json.loads(respText)
        targetTextArray = []
        if respStatusCode == 200:
            if needAlternative == True:
                targetText = respJson["result"]["texts"][0]["text"]
                if printResult == True:
                    print(targetText)
                for item in respJson["result"]["texts"][0]["alternatives"]:
                    targetTextArray.append(item["text"])
                    if printResult == True:
                        print(item["text"])
                return targetTextArray
            else:
                targetText = respJson["result"]["texts"][0]["text"]
                if printResult == True:
                    print(targetText)
                return targetText
        elif respStatusCode == 429:
            raise TooManyRequestsException
        else:
            print("Error", respStatusCode)
            return None

# Example Call
translate("明天你好", "ZH", "EN", True, True, "socks5://127.0.0.1:7890")