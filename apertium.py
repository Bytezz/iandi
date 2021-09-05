#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,json

version="0.1"

if sys.version_info[0]<3:
	from urllib import urlopen,quote_plus
else:
	from urllib.request import urlopen
	from urllib.parse import quote_plus
def _readurl(url):
	page=urlopen(url)
	content=page.read()
	page.close()
	return content
def _encode(o):
	try:
		o=str(o)
	except:
		pass
	try:
		o=unicode(o,"utf-8")
	except:
		pass
	try:
		o=o.encode('utf8')
	except:
		pass
	return o
def listPairs():
	r=json.loads(_readurl("https://apertium.org/apy/listPairs"))
	return r
def listLanguageNames():
	return json.loads(_readurl("https://apertium.org/apy/listLanguageNames"))
def availableLangs():
	r=listPairs()
	langs=[]
	for pair in r["responseData"]:
		if not pair["sourceLanguage"] in langs:
			langs.append(pair["sourceLanguage"])
		if not pair["targetLanguage"] in langs:
			langs.append(pair["targetLanguage"])
	return langs
def identifyLang(txt,onlyBest=True):
	r=json.loads(_readurl("https://beta.apertium.org/apy/identifyLang?q="+_encode(txt)))
	if onlyBest:
		o=[None,None]
		for v in r:
			if o[0]<r[v]:
				o=[r[v],v]
		if o[0]>=0:
			return o[1]
		else:
			return None
	else:
		return r
def translate(txt,src,trg,pairs=None):
	if pairs==None:
		pairs=listPairs()["responseData"]
	def _occur(l,w):
		o=0
		p=None
		i=0
		for e in l:
			if e==w:
				o+=1
				if o<=2:
					p=i
			i+=1
		return o,p
	def _spath(src,trg,path=[],i=0):
		path.append(src)
		pl=[]
		for pair in pairs:
			if pair["sourceLanguage"]==src:
				if pair["targetLanguage"]==trg:
					path.append(pair["targetLanguage"])
					return path
				else:
					pl.append(pair["targetLanguage"])
		if len(path)>=3:
			if _occur(path,path[-1])[0]>0:
				for i in range(len(path)-(_occur(path,path[-1])[1]-1)):
					path.pop(-1)
				return None
		for l in pl:
			o=_spath(l,trg,path,i+1)
			if o!=None:
				return o
		return None
	langs=availableLangs()
	if src in langs:
		if trg in langs:
			try:
				path=_spath(src,trg)
			except:
				return "!Error: Source and target are not compatible."
			if path!=None:
				o=txt
				i=0
				while i<len(path)-1:
					o=json.loads(_readurl("https://apertium.org/apy/translate?markUnknown=no&langpair="+path[i]+"|"+path[i+1]+"&q="+quote_plus(_encode(o))))["responseData"]["translatedText"]
					i+=1
				return o
			else:
				return "!Error: Source and target are not compatible."
		else:
			return "!Error: Target lang not available."
	else:
		return "!Error: Source lang not available."

if __name__=="__main__":
	txt=raw_input("> ")
	#src=identifyLang(txt)
	src=raw_input("in> ")
	trg=raw_input("out> ")
	print("> "+translate(txt,src,trg))