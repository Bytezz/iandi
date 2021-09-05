#!/usr/bin/env python
import globalvars,os

def suspendSys():
	os.system("systemctl suspend")

suspendStrs={
	"eng":"suspend system",
	"ita":"sospendi il sistema",
}

if globalvars.brainlang in suspendStrs:
	suspendStr=suspendStrs[globalvars.brainlang]
else:
	suspendStr=suspendStrs["eng"]

globalvars.brain[suspendStr]="exec%=%suspendSys()%=%exec"