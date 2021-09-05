#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,iso639,json,os

version="0.1"

def inp(txt):
	try:
		if sys.version_info[0]<3:
			return raw_input(txt)
		else:
			return input(txt)
	except KeyboardInterrupt:
		print("\nInterrupted by user.")
		exit(1)
	except Exception as e:
		print("\n{}".format(e))
		exit(2)

def writeTo(item,frm,addr):
	if len(addr)>0:
		frm[addr[0]]=writeTo(item,frm[addr[0]],addr[1:])
	else:
		frm=item
	return frm

def translateJson(slang,sllang):
	with open("langs/eng.json","r") as f:
		engj=json.loads(f.read())
		f.close()
	newj=engj

	# Getting strings and lists wich have to be translated
	if sys.version_info[0]<3:
		validTypes=[str,unicode,list]
	else:
		validTypes=[str,list]
	addrs=[]
	for x in engj: # this ↓ must be changed with a recursive loop
		if type(engj[x]) in validTypes:
			addrs.append([x])
		else:
			for y in engj[x]:
				if type(engj[x][y]) in validTypes:
					addrs.append([x,y])
				else:
					for z in engj[x][y]:
						if type(engj[x][y][z]) in validTypes:
							addrs.append([x,y,z])
						else:
							for k in engj[x][y][z]:
								if type(engj[x][y][z][k]) in validTypes:
									addrs.append([x,y,z,k])
									print(k)
	
	# Getting translations
	for i,addr in enumerate(addrs):
		engv=engj
		for j in addr:
			engv=engv[j]
		if type(engv)==list:
			engs=engv[0]
		else:
			engs=engv

		print("--------")
		print("{}/{}".format(i+1,len(addrs)))
		print("> "+" > ".join(addr))
		print("English: {}".format(repr(engs)))
		# Todo: add multiple entry feature
		newi=inp("{}: ".format(sllang))

		if type(engv)==list:
			newi=[newi]
		newj=writeTo(newi,newj,addr)
	
	# Save to file
	outname="langs/{}.json".format(slang)
	k=0
	while os.path.isfile(outname):
		outname="langs/{}-{}.json".format(slang,k)
		k+=1
	
	with open(outname,"w+") as out:
		out.write(json.dumps(newj,indent=4))
		out.close()
	print("Writed to {}.".format(repr(outname)))
	return 0

def translateBrain(slang,sllang):
	with open("brains/eng.brain","r") as f:
		engb=f.read().split("\n")
		f.close()
	newb=[]

	for i,line in enumerate(engb):
		if line.startswith("#") or line=="":
			newb.append(line)
		else:
			print("--------")
			print("{}/{}".format(i+1,len(engb)))
			print("English: {}".format(line))
			newb.append(inp("{}: ".format(sllang)))

	# Save to file
	outname="brains/{}.brain".format(slang)
	k=0
	while os.path.isfile(outname):
		outname="brains/{}-{}.brain".format(slang,k)
		k+=1
	
	with open(outname,"w+") as out:
		out.write("\n".join(newb))
		out.close()
	print("Writed to {}.".format(repr(outname)))
	return 0

if __name__=="__main__":
	langs=iso639.all()
	e=False
	while not e:
		slang=inp("Select language (2 or 3 char lang code or name in english): ")
		if not slang in langs:
			print("Language not found. Try again.")
		else:
			if iso639.get_iso2(slang)=="eng":
				print("You can't translate into english, it's already english.")
			else:
				e=True
	slang=iso639.get_iso2(slang)
	sllang=iso639.get_eng(slang)
	
	translateOptions=["brain","json"]
	e=False
	while not e:
		print("What you want to translate?")
		for i,option in enumerate(translateOptions):
			print("{} - {}".format(i,option.capitalize()))

		whatToTranslate=inp("> ")
		if whatToTranslate=="":
			whatToTranslate=-1
		else:
			whatToTranslate=int(whatToTranslate)
		if 0<=whatToTranslate<len(translateOptions):
			e=True
		else:
			print("Option not valid. Try again.")

	if translateOptions[whatToTranslate]=="json":
		exit(translateJson(slang,sllang))
	elif translateOptions[whatToTranslate]=="brain":
		exit(translateBrain(slang,sllang))
	else:
		print("Unexpected error.")
		exit(3)