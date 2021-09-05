#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes
f=open("iso3166.json","r")
global codes;codes=json.loads(f.read())
f.close()

def _getby_some(what,value):
	o=""
	for code in codes:
		if code[what].lower()==value.lower():
			o=code
			break
	if o:
		return o
	else:
		return "Error: Not found."

def getby_name(value):
	_getby_some("name",value)
def getby_alpha2(value):
	_getby_some("alpha-2",value)
def getby_alpha3(value):
	_getby_some("alpha-3",value)
def getby_code(value):
	_getby_some("country-code",value)