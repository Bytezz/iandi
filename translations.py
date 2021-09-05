#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json,os,random

version="0.1"

global langstrings
langstrings=None

def checklang(lang):
	if lang=="eng":
		return "Already english."
	elif os.path.isfile("langs/"+lang+".json"):
		f=open("langs/"+lang+".json","r")
		checking=json.loads(f.read())
		f.close()
		f=open("langs/eng.json","r")
		default=json.loads(f.read())
		f.close()
		changedsome=False
		for e in default:
			if not e in checking:
				checking[e]=default[e]
				changedsome=True
			else:
				if type(default[e])==type({}):
					if type(checking[e])!=type({}):
						checking[e]=default[e]
						changedsome=True
					else:
						for sube in default[e]:
							if not sube in checking[e]:
								checking[e][sube]=default[e][sube]
								changedsome=True
		#if changedsome:
		#	f=open("langs/"+lang+".json","w")
		#	f.write(json.dumps(checking,indent=4))
		#	f.close()
		#return "Ok."
		return checking
	else:
		return "Error: not found."

def setlang(lang):
	global langstrings
	if os.path.isfile("langs/"+lang+".json"):
		chkl=checklang(lang)
		if type(chkl)==str:
			f=open("langs/"+lang+".json","r")
			langstrings=json.loads(f.read())
			f.close()
		else:
			langstrings=chkl
		return "Ok."
	else:
		return "Error: not found."

def getstr(*path):
	o=langstrings
	for e in path:
		o=o[e]
	if type(o)==type([]):
		o=random.choice(o)
	return o

def getraw(*path):
	o=langstrings
	for e in path:
		o=o[e]
	return o