#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,iso639,json,os,time,pyautogui,pyperclip

version="0.1"

deepl_langs=[
	"bg",
	"zh",
	"cs",
	"da",
	"nl",
	"et",
	"fi",
	"fr",
	"de",
	"el",
	"hu",
	"ja",
	"lv",
	"lt",
	"pl",
	"pt",
	"ro",
	"ru",
	"sk",
	"sl",
	"sv",
]

guiwebbar=(233,107)
guiintxt=(55,268)
guiouttxt=(352,270)
guiterm=(85,756)

def encode(o):
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

def putInAndGetOut(textin):
	pyautogui.click(guiintxt)
	pyautogui.hotkey('ctrl','a')
	
	pyperclip.copy(textin.replace("\n","\"\\n\""))
	pyautogui.hotkey('ctrl','v')
	
	time.sleep(1.3)
	pyautogui.click(guiouttxt)
	pyautogui.hotkey('ctrl','a')
	pyautogui.hotkey('ctrl','c')
	
	pyautogui.click(guiterm)
	
	return encode(pyperclip.paste().replace("\"\\n\"","\\n"))

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
	
	pyautogui.click(guiwebbar)
	pyautogui.hotkey('ctrl','a')
	
	"""pyautogui.write("https:")
	pyautogui.press("divide")
	pyautogui.press("divide")
	pyautogui.write("www.deepl.com")
	pyautogui.press("divide")
	pyautogui.write("translator")
	pyautogui.press("#")
	pyautogui.write("en")
	pyautogui.press("divide")
	pyautogui.write("{}".format(iso639.get_iso1(slang)))
	pyautogui.press("divide")"""
	
	pyperclip.copy("https://www.deepl.com/translator#en/{}/".format(iso639.get_iso1(slang)))
	pyautogui.hotkey("ctrl","v")
	
	pyautogui.press('enter')
	time.sleep(.5)
	
	# Getting translations
	for i,addr in enumerate(addrs):
		engv=engj
		for j in addr:
			engv=engv[j]
		if type(engv)!=list:
			engstrings=[engv]
		else:
			engstrings=engv
		
		for engs in engstrings:
			print("--------")
			print("{}/{}".format(i+1,len(addrs)))
			print("> "+" > ".join(addr))
			print("English: {}".format(repr(engs)))
			
			#pyperclip.copy(engs)
			
			pyautogui.click(guiintxt)
			pyautogui.hotkey('ctrl','a')
			
			#pyautogui.typewrite(engs.replace("\n","\\n"))
			pyperclip.copy(engs.replace("\n","\"\\n\""))
			pyautogui.hotkey('ctrl','v')
			
			time.sleep(1.3)
			pyautogui.click(guiouttxt)
			pyautogui.hotkey('ctrl','a')
			pyautogui.hotkey('ctrl','c')
			
			pyautogui.click(guiterm)
			#pyautogui.hotkey('ctrl',"shift",'v')
			#pyautogui.press('enter')
			
			# Todo: add multiple entry feature
			#newi=inp("{}: ".format(sllang))
			newi=encode(pyperclip.paste().replace("\"\\n\"","\\n"))
			print("{}: {}".format(sllang,newi))
			
			if type(engv)==list:
				newii=[]
				newii.append(newi)
			else:
				newii=newi
		newj=writeTo(newii,newj,addr)
	
	# Save to file
	outname="langs/{}.json".format(slang)
	k=0
	while os.path.isfile(outname):
		outname="langs/{}-{}.json".format(slang,k)
		k+=1
	
	with open(outname,"w+") as out:
		out.write(json.dumps(newj,indent=16).replace(" "*16,"\t"))
		out.close()
	print("Writed to {}.".format(repr(outname)))
	return 0

def translateBrain(slang,sllang):
	with open("brains/brain-eng","r") as f:
		engb=f.read().split("\n")
		f.close()
	newb=[]
	
	pyautogui.click(guiwebbar)
	pyautogui.hotkey('ctrl','a')
	pyperclip.copy("https://www.deepl.com/translator#en/{}/".format(iso639.get_iso1(slang)))
	pyautogui.hotkey("ctrl","v")
	pyautogui.press('enter')
	time.sleep(.5)
	
	for i,line in enumerate(engb):
		if line.startswith("# ") or line=="" or line=="{" or line=="}":
			newb.append(line)
		elif line.startswith("#"):
			newb.append("")
		else:
			print("--------")
			print("{}/{}".format(i+1,len(engb)))
			print("English: {}".format(line))
			
			if '":"' in line:
				line=line.split('":"')
				line[0]+='"'
				line[1]='"'+line[1]
			elif "':'" in line:
				line=line.split("':'")
				line[0]+="'"
				line[1]="'"+line[1]
			elif '": "' in line:
				line=line.split('": "')
				line[0]+='"'
				line[1]='"'+line[1]
			elif "': '" in line:
				line=line.split("': '")
				line[0]+="'"
				line[1]="'"+line[1]
			elif '" :"' in line:
				line=line.split('" :"')
				line[0]+='"'
				line[1]='"'+line[1]
			elif "' :'" in line:
				line=line.split("' :'")
				line[0]+="'"
				line[1]="'"+line[1]
			elif '" : "' in line:
				line=line.split('" : "')
				line[0]+='"'
				line[1]='"'+line[1]
			elif "' : '" in line:
				line=line.split("' : '")
				line[0]+="'"
				line[1]="'"+line[1]
			
			if line[0].startswith("{"):
				query=line[0][2:-1]
				pre=line[0][:1]
			else:
				query=line[0][1:-1]
				pre=""
			
			if line[1].endswith(","):
				answer=line[1][1:-2]
				aft=line[1][-1]
			else:
				answer=line[1][1:-1]
				aft=""
			
			if query!=query.upper():
				query=putInAndGetOut(query)
			
			if answer.startswith(":goto:") and answer.endswith(":goto:"):
				answer=":goto:"+putInAndGetOut(answer[6:-6])+":goto:"
			elif "|&|" in answer:
				answers=[]
				for ans in answer.split("|&|"):
					if not(answer.startswith("exec%=%") and answer.endswith("%=%exec")):
						if answer.startswith(":goto:") and answer.endswith(":goto:"):
							answers.append(":goto:"+putInAndGetOut(ans[6:-6])+":goto:")
						else:
							answers.append(putInAndGetOut(ans))
				answer="|&|".join(answers)
			else:
				if not (answer.startswith("exec%=%") and answer.endswith("%=%exec")):
					answer=putInAndGetOut(answer)
			
			newline="{}{}:{}{}".format(pre,repr(query),repr(answer),aft)
			print(("{}: {}".format(sllang,newline)))
			newb.append(newline)
	
	# Save to file
	outname="brains/brain-{}".format(slang)
	k=0
	while os.path.isfile(outname):
		outname="brains/brain-{}-{}".format(slang,k)
		k+=1
	
	with open(outname,"w+") as out:
		out.write("\n".join(newb))
		out.close()
	print("Writed to {}.".format(repr(outname)))
	return 0

if __name__=="__main__":
	"""langs=iso639.all()
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
	sllang=iso639.get_eng(slang)"""
	
	"""translateOptions=["brain","json"]
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
			print("Option not valid. Try again.")"""
	
	wantStart=inp("Do you want to start? [y/N] ")
	if not (wantStart.lower()=="y" or wantStart.lower()=="yes"):
		print("Quitting.")
		exit(0)
	
	for lang in deepl_langs:
		slang=iso639.get_iso2(lang)
		sllang=iso639.get_eng(lang)
		#if translateOptions[whatToTranslate]=="json":
		translateJson(slang,sllang)
		#elif translateOptions[whatToTranslate]=="brain":
		translateBrain(slang,sllang)
		#else:
		#	print("Unexpected error.")
		#	break

	print("Done.")
	os.system("systemctl suspend")
