#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from difflib import SequenceMatcher

version="0.1"

# https://github.com/mledoze/countries
f=open("countries.json","r")
global countries;countries=json.loads(f.read())
f.close()

def getall():
	return countries

def getall_names(codes=False):
	o={}
	for country in countries:
		names=[]
		names.append(country["name"]["common"].lower())
		names.append(country["name"]["official"].lower())
		if codes:
			names.append(country["cca3"].lower())
			names.append(country["cioc"].lower())
		for lang in country["name"]["native"]:
			names.append(country["name"]["native"][lang]["common"].lower())
			names.append(country["name"]["native"][lang]["official"].lower())
		for lang in country["translations"]:
			names.append(country["translations"][lang]["common"].lower())
			names.append(country["translations"][lang]["official"].lower())
		for name in names:
			o[name]=country["ccn3"]
	return o

def search(q,countrieslist="",codes=True):
	if countrieslist=="":
		countrieslist=getall_names(codes)
	atto=0.0
	attn=""
	for country in countrieslist:
		match=SequenceMatcher(None,q,country).ratio()
		if match>atto:
			atto=match
			attn=countrieslist[country]
	return [atto,getby_code(attn)]

def _getby_some(what,value,multiple=False):
	if multiple:
		o=[]
	else:
		o=""
	for code in countries:
		ok=False
		if what=="name":
			if code["name"]["common"].lower()==value.lower():
				ok=True
		elif what=="languages":
			if value.lower() in code[what]:
				ok=True
		elif what=="unilang":
			if value.lower() in code["languages"] and len(code["languages"])==1:
				ok=True
		elif what=="capital":
			if value.capitalize() in code[what]:
				ok=True
		elif code[what].lower()==value.lower():
			ok=True

		if ok:
			if multiple:
				o.append(code)
			else:
				o=code
				break
	correct=False
	if multiple:
		if o!=[]:
			correct=True
	else:
		if o:
			correct=True
	if correct:
		return o
	else:
		return "Error: Not found."

def getby_name(value):
	return _getby_some("name",value)
def getby_alpha2(value):
	return _getby_some("cca2",value)
def getby_alpha3(value):
	return _getby_some("cca3",value)
def getby_code(value):
	return _getby_some("ccn3",value)
def getby_lang(value,multiple=True):
	return _getby_some("languages",value,multiple)
def getby_unilang(value,multiple=False):
	return _getby_some("unilang",value,multiple)
def getby_region(value,multiple=True):
	return _getby_some("region",value,multiple)
def getby_subregion(value,multiple=True):
	return _getby_some("subregion",value,multiple)
def getby_capital(value):
	return _getby_some("capital",value)