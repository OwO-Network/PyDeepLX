"""
Author: Vincent Young
Date: 2023-04-27 00:44:01
LastEditors: Vincent Young
LastEditTime: 2023-05-21 03:58:18
FilePath: /PyDeepLX/PyDeepLX/PyDeepLX.py
Telegram: https://t.me/missuo

Copyright © 2023 by Vincent, All Rights Reserved. 
"""
import random
import time
import json
import httpx


deeplAPI = "https://www2.deepl.com/jsonrpc"
headers = {
	"content-type": "application/json",
	"user-agent": "DeepL/1627620 CFNetwork/3826.500.62.2.1 Darwin/24.4.0",
	"accept": "*/*",
	"x-app-os-name": "iOS",
	"x-app-os-version": "18.4.0",
	"accept-language": "en-US,en;q=0.9",
	"accept-encoding": "gzip, deflate, br",
	"x-app-device": "iPhone16,2",
	"referer": "https://www.deepl.com/",
	"x-product": "translator",
	"x-app-build": "1627620",
	"x-app-version": "25.1",
}


class TooManyRequestsException(Exception):
	"Raised when there is a 429 error"
	
	def __str__(self):
		return "PyDeepLX Error: Too many requests, your IP has been blocked by DeepL temporarily, please don't request it frequently in a short time."
	
	
def getICount(translateText) -> int:
	return translateText.count("i")


def getRandomNumber() -> int:
	random.seed(time.time())
	num = random.randint(8300000, 8399998)
	return num * 1000


def getTimestamp(iCount: int) -> int:
	ts = int(time.time() * 1000)
	
	if iCount == 0:
		return ts
	
	iCount += 1
	return ts - ts % iCount + iCount


def translate(
	text,
	sourceLang="auto",
	targetLang="EN",
	numberAlternative=0,
	printResult=False,
):
	iCount = getICount(text)
	id = getRandomNumber()
	
	numberAlternative = max(min(3, numberAlternative), 0)
	
	# Modified to match the structure in the example
	postData = {
		"jsonrpc": "2.0",
		"method": "LMT_handle_jobs",
		"id": id,
		"params": {
			"commonJobParams": {
				"formality": "undefined",
				"wasSpoken": False,
				"regionalVariant": "en-US",
				"transcribe_as": "romanize",
				"mode": "translate",
				"textType": "plaintext",
				"advancedMode": False
			},
			"lang": {
				"source_lang_user_selected": sourceLang,
				"target_lang": targetLang,
				"source_lang_computed": "ZH" if sourceLang == "auto" else sourceLang
			},
			"jobs": [
				{
					"sentences": [{"prefix": "", "text": text, "id": 0}],
					"kind": "default",
					"raw_en_context_after": [],
					"raw_en_context_before": [],
					"preferred_num_beams": 1
				}
			],
			"timestamp": getTimestamp(iCount),
		},
	}
	postDataStr = json.dumps(postData, ensure_ascii=False)
	
	if (id + 5) % 29 == 0 or (id + 3) % 13 == 0:
		postDataStr = postDataStr.replace('"method":"', '"method" : "', -1)
	else:
		postDataStr = postDataStr.replace('"method":"', '"method": "', -1)
		
	with httpx.Client() as client:
		resp = client.post(url=deeplAPI, data=postDataStr, headers=headers)
		respStatusCode = resp.status_code
		
		if respStatusCode == 429:
			raise TooManyRequestsException
			
		if respStatusCode != 200:
			print("Error", respStatusCode)
			return
		
		respText = resp.text
		respJson = json.loads(respText)
		
		# Adjust response parsing based on the structure expected from LMT_handle_jobs
		try:
			targetText = respJson["result"]["translations"][0]["beams"][0]["sentences"][0]["text"]
			if printResult:
				print(targetText)
			return targetText
		except KeyError:
			# Fallback to original structure in case API response format differs
			if "result" in respJson and "texts" in respJson["result"]:
				if numberAlternative <= 1:
					targetText = respJson["result"]["texts"][0]["text"]
					if printResult:
						print(targetText)
					return targetText
				
				targetTextArray = []
				for item in respJson["result"]["texts"][0]["alternatives"]:
					targetTextArray.append(item["text"])
					if printResult:
						print(item["text"])
						
				return targetTextArray
			else:
				print("Unexpected response format:", respJson)
				return None	

# Example Call
# translate("明天你好", "ZH", "EN", True, True, "socks5://127.0.0.1:7890")
# translate("明天你好", "ZH", "EN", 3, True)
