#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,json

if sys.version_info[0]<3:
	import urllib
else:
	import urllib.request
	import urllib.parse

version="0.1.1"

def _readurl(url):
	if sys.version_info[0]<3:
		page=urllib.urlopen(url)
	else:
		page=urllib.request.urlopen(url)
	content=page.read()
	page.close()
	return content
def _urlencode(toParse):
	if sys.version_info[0]<3:
		return(urllib.urlencode(toParse))
	else:
		return(urllib.parse.urlencode(toParse))
####
token="ef1f15ea31cf4c0dbd49deaa880d5d56"
server="https://newsapi.org/v2/"
def topheads(country="us",category="general",q="",pageSize=20,page=1,source=True):
	p=_urlencode({"apiKey":token,"country":country,"category":category,"pageSize":pageSize,"page":page})
	r=json.loads(_readurl(server+"top-headlines?"+p))
	if r["status"]=="ok":
		heads=[]
		for art in r["articles"]:
			if source:
				heads.append(art["title"])
			else:
				heads.append(" - ".join(art["title"].split(" - ")[:-1]))
		if heads!=[]:
			return heads
		else:
			return "!Error: No results."
	else:
		return "!Error: "+r["code"]
def everything(q="",qInTitle="",domains="",excludeDomains="",since="",to="",language="en",sortBy="",pageSize=20,page=1,source=True):
	p=_urlencode({"apiKey":token,
		"q":q,
		"qInTitle":qInTitle,
		"domains":domains,
		"excludeDomains":excludeDomains,
		"from":since,
		"to":to,
		"language":language,
		"sortBy":sortBy,
		"pageSize":pageSize,
		"page":page
	})
	r=json.loads(_readurl(_readurl(server+"everything?"+p)))
	if r["status"]=="ok":
		heads=[]
		for art in r["articles"]:
			if source:
				heads.append(art["title"])
			else:
				heads.append(" - ".join(art["title"].split(" - ")[:-1]))
		if heads!=[]:
			return heads
		else:
			return "!Error: No results."
	else:
		return "!Error: "+r["code"]
####
if __name__=="__main__":
	c=raw_input("Country> ")
	print("\n".join(topheads(country=c,pageSize=3,source=False)))