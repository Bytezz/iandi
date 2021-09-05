#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

iandiV=""        # Iandi main file and internals.py version
rmemV=""         # RMem version
iso639V=""       # Iso639 lib and json version
countriesV=""    # Countries lib and json version
citiesV=""       # Cities lib and json version
translationsV="" # Translations lib and json version
apertiumV=""     # Apertium lib version
newsapiV=""      # NewsAPI lib version
tdlibwV=""       # Tlib wrapper version
installerV=""    # Iandi installer version
readmeD=""       # Readme update date
getverV="0.1"    # getversions.py version

# Getting Iandi version
with open("iandi","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("globalvars.version="):
			iandiV=line.split('"')[1]
			break
	f.close()

# Getting RMem version
with open("rmem.py","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("globalvars.rmemversion="):
			rmemV=line.split('"')[1]
			break
	f.close()

# Getting iso639 version
with open("iso639.py","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("version="):
			iso639V=line.split('"')[1]
			break
	f.close()

# Getting countries version
with open("countries.py","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("version="):
			countriesV=line.split('"')[1]
			break
	f.close()

# Getting cities version
with open("cities.py","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("version="):
			citiesV=line.split('"')[1]
			break
	f.close()

# Getting translations version
with open("translations.py","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("version="):
			translationsV=line.split('"')[1]
			break
	f.close()

# Getting apertium version
with open("apertium.py","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("version="):
			apertiumV=line.split('"')[1]
			break
	f.close()

# Getting NewsAPI version
with open("newsapi.py","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("version="):
			newsapiV=line.split('"')[1]
			break
	f.close()

# Getting tdlib wrapper version
with open("tdlib/__init__.py","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("version="):
			tdlibwV=line.split('"')[1]
			break
	f.close()

# Getting iandi installer version
with open("install","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("installerVersion="):
			installerV=line.split('"')[1]
			break
	f.close()

# Getting readme update date
with open("README.md","r") as f:
	c=f.read()
	for line in c.split("\n"):
		if line.startswith("Readme update of"):
			readmeD=line.split('of ')[1]
			break
	f.close()

# Showing versions
print(
"Iandi \t\t"+iandiV+"\n"+
" (Iandi main file and internals.py)\n"+
"RMem \t\t"+rmemV+"\n"+
" (rmem.py)\n"+
"Iso639 \t\t"+iso639V+"\n"+
" (iso639.py and ISO-639-2_utf-8.txt)\n"+
"Countries \t"+countriesV+"\n"+
" (countries.py and countries.json)\n"+
"Cities \t\t"+citiesV+"\n"+
" (cities.py and cities.json)\n"+
"Translations \t"+translationsV+"\n"+
" (translations.py and langs/eng.json)\n"+
"Apertium \t"+apertiumV+"\n"+
" (apertium.py)\n"+
"NewsAPI \t"+newsapiV+"\n"+
" (newsapi.py)\n"+
"TDLib wrapper \t"+tdlibwV+"\n"+
" (tdlib/__init__.py)\n"+
"Installer \t"+installerV+"\n"+
" (./install)\n"+
"Readme update of "+readmeD+"\n"+
" (README.md, YYYY/MM/DD)\n"+

"GetVersions \t"+getverV+"\n"+
" (getversions.py)"
)
print("\nTotal version: {};{};{};{};{};{};{};{};{};{};{}\n".format(
	iandiV,
	rmemV,
	iso639V,
	countriesV,
	citiesV,
	translationsV,
	apertiumV,
	newsapiV,
	tdlibwV,
	installerV,
	getverV
))