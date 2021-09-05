#!/usr/bin/env python
# -*- coding: utf-8 -*-
import globalvars,random

def lolr():
	if random.randint(0,1)==0:
		return "lol."
	else:
		return "lel."

globalvars.brain["lol"]="exec%=%lolr()%=%exec"