#!/usr/bin/env python
# -*- coding: utf-8 -*-

version="0.1"

f=open("ISO-639-2_utf-8.txt","r")
rawlangs=f.read()
f.close()
global langs;langs={}
global names;names={}

for line in rawlangs.split("\n"):
	inf={}
	inf["bibliographic"],inf["terminologic"],inf["alpha2"],inf["english"],inf["french"]=line.strip().split("|")
	langs[inf["bibliographic"]]=inf
	if inf["terminologic"]:
		langs[inf["terminologic"]]=inf
	if inf["alpha2"]:
		langs[inf["alpha2"]]=inf
	if inf["english"]:
		langs[inf["english"].lower()]=inf
		langs[inf["french"].lower()]=inf
		names[inf["english"].lower()]=inf
		names[inf["french"].lower()]=inf

def all():
	return langs

def allnames():
	return names

def get_iso2(langcode):
	if langcode in langs:
		return langs[langcode]["bibliographic"]
	else:
		return "Error: lang not found."

def get_iso1(langcode):
	if langcode in langs:
		return langs[langcode]["alpha2"]
	else:
		return "Error: lang not found."

def get_eng(langcode):
	if langcode in langs:
		return langs[langcode]["english"]
	else:
		return "Error: lang not found."

def get_info(lang):
	if lang in langs:
		return langs[lang]
	else:
		return "Error: lang not found."