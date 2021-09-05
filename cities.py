#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

version="0.1"

# https://github.com/lutangar/cities.json
f=open("cities.json","r")
global cities;cities=json.loads(f.read())
f.close()

def getall():
	return cities

def getall_names(lower=False):
	o=[]
	for city in cities:
		if lower:
			o.append(city["name"].lower())
		else:
			o.append(city["name"].lower())
	return o

def _getby_some(what,value,multiple=False):
	if multiple:
		o=[]
	else:
		o=""
	for code in cities:
		ok=False
		if code[what].lower()==value.lower():
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

def getby_name(value,multiple=False):
	return _getby_some("name",value,multiple)
def getby_country(value,multiple=False):
	return _getby_some("country",value,multiple)