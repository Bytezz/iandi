#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os,sys,ast,json,datetime,random,time,re,subprocess,locale,iso639,countries,cities,translations,apertium,alsaaudio,vlc,newsapi,tdlib,globalvars,xml.etree.ElementTree as xmletree,traceback
if sys.version_info[0]<3:
	import thread
	import urllib
else:
	import _thread as thread
	import urllib.request as urllib
from playsound import playsound
from difflib import SequenceMatcher

globalvars.rmemversion="0.1.1"

def log(txt):
	txt=str(datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S"))+" - "+str(txt)
	print(txt)
	with open("/tmp/iandi.log","a") as log:
		log.write(txt+"\n")
		log.close()
def encode(o):
	try:
		o=str(o)
	except:
		pass
	try:
		o=unicode(o,"utf-8")
	except:
		pass
	return o
def encode2(o):
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
def encode3(o):
	try:
		o=str(o)
	except:
		pass
	try:
		o=unicode(o,"utf-8")
	except:
		try:
			o=o.encode('utf8')
		except:
			pass
	return o
def gstr(o):
	#o=encode(o).strip().replace("À","à").replace("È","è").replace("É","é").replace("Ì","ì").replace("Ò","ò").replace("Ù","ù").capitalize()
	o=encode(o).strip().capitalize()
	if not o.endswith(".") and not o.endswith("?") and not o.endswith("!"):
		o+="."
	return o
def update_memory(mem):
	with open("mem","w+") as f:
		f.write(str(mem))
		f.close()
try:
	if os.path.exists(os.path.expanduser("~")+"/.iandi/"):
		mempath=os.path.expanduser("~")+"/.iandi/mem"
	else:
		mempath="mem"
	# Create file if it does not exist
	if not os.path.isfile(mempath):
		with open(mempath,"w+") as f:
			f.close()
	# Open mem for reading
	with open(mempath,"r") as f:
		mem=f.read()
		if mem!="":
			mem=ast.literal_eval(mem)
		else:
			mem={}
			update_memory(mem)
		f.close()
except Exception as e:
	log(traceback.format_exc())
	mem={}
	update_memory(mem)
def verify_existence(var,t=None):
	try:
		if type(t)!=type(None):
			if type(mem[var])!=type(t):
				mem[var]=t
	except:
		mem[var]=t
	update_memory(mem)
def make_a_newinput(o,*args):
	args=map(str,args)
	return "<<newinput<"+encode(o)+"<,>"+",".join(args)+">newinput>>"
def call_from_brain(c):
	return "<<callbrain<"+encode(c)+">callbrain>>"
def exec_for_output(c):
	return "<<exec<"+encode(c)+">exec>>"
def similar(a,b):
	try:
		a=encode(a)
	except:
		pass
	try:
		b=encode(b)
	except:
		pass
	return SequenceMatcher(None,a,b).ratio()
def isnumber(txt):
	txt=txt.replace(" ","")
	if txt.isdigit():
		return True
	elif txt.startswith("-") and txt[1:].isdigit():
		return True
	elif "." in txt and txt.split(".")[-1].isdigit():
		if txt.split(".")[0].isdigit() and txt.split(".")[-1].isdigit():
			return True
		elif txt.split(".")[0].startswith("-") and txt.split(".")[0][1:].isdigit() and txt.split(".")[-1].isdigit():
			return True
		else:
			return False
	else:
		return False
def readurl(url):
	page=urllib.urlopen(url)
	content=page.read()
	page.close()
	return content
def _getMasterMixer():
	try:
		mastermixer=alsaaudio.Mixer("Master",0)
	except:
		mastermixer=alsaaudio.Mixer(alsaaudio.mixers()[0],0)
	return mastermixer
def _getSystemVolume():
	mastermixer=_getMasterMixer()
	return mastermixer.getvolume()[0]
def _setSystemVolume(vol):
	mastermixer=_getMasterMixer()
	channel=alsaaudio.MIXER_CHANNEL_ALL
	mastermixer.setvolume(vol,channel)
def _turnMaxSystemVolume():
	mastermixer=_getMasterMixer()
	channel=alsaaudio.MIXER_CHANNEL_ALL
	vol=100
	mastermixer.setvolume(vol,channel)
	return 100
def _removeSystemMute():
	mastermixer=_getMasterMixer()
	channel=alsaaudio.MIXER_CHANNEL_ALL
	mastermixer.setmute(0,channel)
#anstollerance=0
#exitcommand="exit()"
global playing_now;playing_now=False
global mediaVol;mediaVol=_getSystemVolume()
_removeSystemMute()
if mediaVol<=0:
	mediaVol=_turnMaxSystemVolume()

name="Iandi"
birth="14/06/2019"
def list_in_human_format(l,newline=True,conclusion=True):
	output=""
	for n,e in enumerate(l):
		if n>0 and n==len(l)-1:
			if newline:
				output+=" e\n"
			else:
				output+=" e "
		elif n>0:
			if newline:
				output+="\n"
			else:
				output+=" "
		output+=e
		if n==len(l)-1 and conclusion:
			output+="."
		elif n<len(l)-2:
			output+=","
	return output
def format_seconds(s):
	s=s/3600.0
	d=0
	h=int(s)
	if h>24:
		d=int(h/24)
		h-=d*24
		s-=d*24
	m=int((s-h)*60)
	s=int((((s-h)*60)-m)*60)
	output=[]
	if d>0:
		if d==1:
			output.append(str(d)+" "+translations.getstr("day"))
		else:
			output.append(str(d)+" "+translations.getstr("days"))
	if h>0:
		if h==1:
			output.append(str(h)+" "+translations.getstr("hour"))
		else:
			output.append(str(h)+" "+translations.getstr("hours"))
	if m>0:
		if m==1:
			output.append(str(m)+" "+translations.getstr("minute"))
		else:
			output.append(str(m)+" "+translations.getstr("minutes"))
	if s>0:
		if s==1:
			output.append(str(s)+" "+translations.getstr("second"))
		else:
			output.append(str(s)+" "+translations.getstr("seconds"))
	return list_in_human_format(output,newline=False,conclusion=False)
def checkmemo():
	verify_existence("memo",{})
	while True:
		if mem["memo"]!={}:
			t=float("inf")
			try:
				for memo in mem["memo"]:
					if mem["memo"][memo]<time.time():
						del mem["memo"][memo]
						update_memory(mem)
						playsound("resources/sounds/timer.ogg")
					else:
						if mem["memo"][memo]<t:
							t=mem["memo"][memo]
				if t==float("inf"):
					time.sleep(10800)
				else:
					time.sleep(t-time.time())
			except:
				pass
		else:
			time.sleep(10800)
thread.start_new_thread(checkmemo,())

if tdlib.isWorking:
	tdlib.start()

def setlang(ilang="",returning=False,internal=True):
	if ilang:
		syslang=ilang
	else:
		syslang=locale.getdefaultlocale()[0].split("_")[0]
	rsyslang=iso639.get_iso2(syslang)
	if not rsyslang.startswith("Error: "):
		syslang=rsyslang
	o=""
	if not internal:
		syslang=syslang.lower()
		if syslang in iso639.allnames():
			ratio=1.0
			o=syslang
		else:
			try:
				if mem["lang"]!="eng":
					syslang=apertium.translate(syslang,mem["lang"],"eng").lower()
			except:
				pass
			ratio=0
			for code in iso639.allnames():
				match=similar(syslang,code)
				if match>ratio:
					ratio=match
					o=code.lower()
	if o=="":
		o=syslang
	if returning:
		if internal:
			return o
		else:
			return [o,ratio]
	else:
		mem["lang"]=o
		update_memory(mem)
		updateCustCmds()
		if translations.setlang(mem["lang"])=="Error: not found.":
			log("Lang "+iso639.get_eng(mem["lang"])+" not supported in translations. Swithing to english.")
			setlang("eng")
			translations.setlang(mem["lang"])
verify_existence("lang",setlang("",True))

def setcountry(icountry="",returning=False,internal=True):
	if icountry=="":
		if mem["lang"]=="eng":
			icountry="USA"
		else:
			icountry=countries.getby_unilang(mem["lang"])
			if type(icountry)==type("") and icountry.startswith("Error: "):
				icountry=countries.getby_lang(mem["lang"])
				if type(icountry)==type("") and icountry.startswith("Error: "):
					icountry="USA"
				else:
					icountry=icountry["cca3"]
			else:
				icountry=icountry["cca3"]
	if internal:
		countrieslist=countries.getall_names(True)
	else:
		countrieslist=countries.getall_names()
	if icountry.lower() in countrieslist.keys():
		ratio=1.0
		icountry=countries.getby_code(countrieslist[icountry.lower()])
	else:
		rawicountry=icountry
		icountry=countries.search(icountry.lower(),countrieslist)
		ratio=icountry[0]
		if ratio>.2:
			icountry=icountry[1]
		else:
			log("Country '"+rawicountry+"' not in db.")
			if internal:
				icountry=countries.getby_alpha3("USA")
			else:
				return "Error: Lang not in db."
	icountry=icountry["cca3"]
	if returning:
		if internal:
			return icountry
		else:
			return [icountry,ratio]
	else:
		mem["country"]=icountry
		update_memory(mem)
verify_existence("country",setcountry("",True))

def setcity(icity="",returning=False,internal=True,first=True):
	if not icity:
		icity=countries.getby_alpha3(mem["country"])["capital"][0]
	#else:
	#	try:
	#		if mem["lang"]!="eng":
	#			rawicity=apertium.translate(icity,mem["lang"],"eng")
	#			icity=rawicity
	#	except:
	#		pass
	if icity.lower() in cities.getall_names(True):
		ratio=1.0
		icity=icity.capitalize()
	else:
		ratio=0
		attn=""
		for city in cities.getall_names():
			rcity=city.lower()
			match=similar(icity,rcity)
			if match>.3 and match>ratio:
				ratio=match
				attn=city
				if ratio>=1:
					break
		if attn=="":
			log("City '"+icity+"' not in db.")
			if not internal:
				if first and mem["lang"]!="eng":
					try:
						icity=apertium.translate(icity,mem["lang"],"eng")
						r=setcity(icity,returning=True,internal=False,first=False)
						if not(type(r)==type("") and r.startswith("Error: ")):
							icity=r[0]
						else:
							return "Error: not found."
					except:
						return "Error: not found."
				else:
					return "Error: not found."
		else:
			icity=attn
	if returning:
		if internal:
			return icity
		else:
			return [icity,ratio]
	else:
		mem["city"]=icity
		update_memory(mem)
verify_existence("city",setcity("",True))

def updateCustCmds():
	if not "custCmds" in mem:
		mem["custCmds"]={}
		update_memory(mem)
	if mem["custCmds"]!={} and mem["lang"] in mem["custCmds"] and mem["custCmds"][mem["lang"]]!={}:
		for ccmd in mem["custCmds"][mem["lang"]]:
			ext=False
			while ext==False:
				try:
					globalvars.brain[ccmd]=call_from_brain( mem["custCmds"][mem["lang"]][ccmd] )
					ext=True
				except:
					time.sleep(.5)
thread.start_new_thread(updateCustCmds,())

global translations
if translations.setlang(mem["lang"])=="Error: not found.":
	setlang("eng")
	translations.setlang(mem["lang"])

# ↑ internal functions
# ↓ assistant's functions

def oldyear():
	return translations.getstr("oldyear").format(str(int(datetime.date.today().year)-int(birth.split("/")[-1])))
def ctime():
	h=datetime.datetime.now().strftime("%H")
	m=datetime.datetime.now().strftime("%M")
	if h<12:
		s=translations.getstr("ctime","ofmorning")
	else:
		s="."
	return translations.getstr("ctime","its").format(str(h),str(m))
def day():
	d=translations.getraw("weekdays")
	m=translations.getraw("months")
	now=datetime.datetime.now()
	#return 'Oggi è '+str(datetime.date.today().day)+'/'+str(datetime.date.today().month)+'/'+str(datetime.date.today().year)
	return translations.getstr("todayis").format(d[int(now.strftime("%w"))],now.strftime("%d"),m[int(now.strftime("%m"))],now.strftime("%Y"))
def dttm():
	return datetime.datetime.now()

def langsettings(args):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("langsettings","say"),"langsettings")
	else:
		results=[]
		for i,arg in enumerate(args):
			r=[arg,setlang(arg,True,False)]
			if not(type(r)==type("") and r.startswith("Error: ")):
				results.append(r)
		if len(results)==0:
			return translations.getstr("langsettings","notindb")
		else:
			atto=0
			attn={}
			attr=""
			for r in results:
				if r[1][1]>atto:
					atto=r[1][1]
					attn=r[1][0]
					attr=r[0]
			setlang(attn)
			return translations.getstr("langsettings","setted").format(attr)

def countrysettings(args):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("countrysettings","say"),"countrysettings")
	else:
		r=setcountry(" ".join(args),True,False)
		if not(type(r)=="str" and r.startswith("Error: ")):
			attn=r[0]
			attr=countries.getby_alpha3(attn)
			if mem["lang"] in attr["translations"]:
				attr=attr["translations"][mem["lang"]]["official"]
			else:
				attr=attr["name"]["official"]
			setcountry(attn)
			return translations.getstr("countrysettings","setted").format(attr)
		else:
			results=[]
			for i,arg in enumerate(args):
				r=[arg,setcountry(arg,True,False)]
				if not(type(r)==type("") and r.startswith("Error: ")):
					results.append(r)
			if len(results)==0:
				return translations.getstr("countrysettings","notindb")
			else:
				atto=0
				attn={}
				attr=""
				for r in results:
					if r[1][1]>atto:
						atto=r[1][1]
						attn=r[1][0]
						attr=r[0]
				setcountry(attn)
				return translations.getstr("countrysettings","setted").format(attr)

def citysettings(args):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("citysettings","say"),"citysettings")
	else:
		r=setcity(" ".join(args),True,False)
		if not(type(r)=="str" and r.startswith("Error: ")):
			setcity(r[0])
			return translations.getstr("citysettings","setted").format(r[0].capitalize())
		else:
			results=[]
			for i,arg in args:
				r=setcity(arg,True,False)
				if not(type(r)==type("") and r.startswith("Error: ")):
					results.append(r)
			if len(results)==0:
				return translations.getstr("citysettings","notindb")
			else:
				atto=0
				attn={}
				attr=""
				for r in results:
					if r[1][1]>atto:
						atto=r[1][1]
						attn=r[1][0]
						attr=r[0]
				setcountry(attn)
				return translations.getstr("citysettings","setted").format(attn)
def umbrella():
	if globalvars.onlineconnection:
		output=""
		r=json.loads(readurl("http://api.weatherstack.com/current?access_key=4259baf5cdc16ffb529bc3c6384d349c&query="+mem["city"]))
		if "success" in r and r["success"]==False:
			if "error" in r:
				raise Exception("Error in request to weatherstack: "+str(r["error"]["type"])+".")
			else:
				raise Exception("Error in request to weatherstack.")
		if 1<=r["current"]["precip"]<10:
			output="Sta piovigginando, conviene portarlo."
		elif r["current"]["precip"]>=10:
			output="Sì, sta piovendo."
		elif r["current"]["cloudcover"]>=40:
			output="È nuvoloso, potrebbe iniziare a piovere. Pòrtalo"
		else:
			output="Non serve l'ombrello."
		return output
	else:
		return translations.getstr("internetneeded")
def weather():
	if globalvars.onlineconnection:
		r=json.loads(readurl("http://api.weatherstack.com/current?access_key=4259baf5cdc16ffb529bc3c6384d349c&query="+mem["city"]))
		if "success" in r and r["success"]==False:
			if "error" in r:
				raise Exception("Error in request to weatherstack: "+str(r["error"]["type"])+".")
			else:
				raise Exception("Error in request to weatherstack.")
		output=translations.getstr("weather","at").format(mem["city"])+\
		translations.getstr("weather","degrees").format(str(r["current"]["temperature"]))
		if 1<=r["current"]["precip"]<10:
			output+=translations.getstr("weather","drizzle")
		elif r["current"]["precip"]>=10:
			output+=translations.getstr("weather","rain")
		if r["current"]["cloudcover"]>=40:
			output+=translations.getstr("weather","cloudy")
		elif r["current"]["cloudcover"]>=20:
			output+=translations.getstr("weather","bitcloudy")
		else:
			output+=translations.getstr("weather","clear")
		return output
	else:
		return translations.getstr("internetneeded")
def rand(args):
	if args==[]:
		args=[0,10]
	else:
		digs=[]
		for e in args:
			if e.isdigit():
				digs.append(int(e))
		if len(digs)==0:
			args=[0,10]
		elif len(digs)==1:
			args=[0,digs[0]]
		else:
			digs.sort()
			args=[digs[0],digs[-1]]
	return str(random.randint(args[0],args[1]))
def choiserand(l):
	return random.choice(l)
def addnote(args):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("addnote","saynote"),"addnote")
	else:
		verify_existence("notes",[])
		mem["notes"].append(" ".join(args))
		update_memory(mem)
		return translations.getstr("addnote","noteadded").format(" ".join(args))
def rmnote(args):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("removenote","saynote"),"rmnote")
	else:
		verify_existence("notes",[])
		ntd=" ".join(args)
		s=[0,0]
		for i,note in enumerate(mem["notes"]):
			ts=similar(ntd,note)
			if ts>=.65 and ts>s[0]:
				s=[ts,i]
		if s[0]>0:
			ntd=mem["notes"][s[1]]
			mem["notes"].pop(s[1])
			update_memory(mem)
			return translations.getstr("removenote","noteremoved").format(ntd)
		else:
			return translations.getstr("removenote","notenotfound")
def readnote():
	verify_existence("notes",[])
	if len(mem["notes"])==1:
		prestr=translations.getstr("readnote","one","prestr")
		aftstr=translations.getstr("readnote","one","aftstr")
	else:
		prestr=translations.getstr("readnote","multiple","prestr")
		aftstr=translations.getstr("readnote","multiple","aftstr")
	output=translations.getstr("readnote","print").format(encode(prestr),str(len(mem["notes"])),encode(aftstr),list_in_human_format(mem["notes"]))
	return output
def waitmemo(t):
	if t-time.time()<10800:
		if t>time.time():
			time.sleep(t-time.time())
		playsound("resources/sounds/timer.ogg")
		for i in mem["memo"]:
			if mem["memo"][i]==t:
				del mem["memo"][i]
				update_memory(mem)
	else:
		pass
def addmemo(args,t=0):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("addmemo","saymemo"),"addmemo")
	else:
		verify_existence("memo",{})
		if t==0:
			return make_a_newinput(translations.getstr("addmemo","when"),"addmemo",str(args))
		d=translations.getraw("weekdays")
		m=translations.getraw("months")
		now=datetime.datetime.now()
		day=int(now.strftime("%d"))
		month=int(now.strftime("%m"))
		year=int(now.strftime("%Y"))
		hour=0
		minute=0
		second=0
		securehourminute=False
		for i,word in enumerate(t):
			if ":" in word:
				if len(word.split(":"))==2:
					if word.split(":")[0].isdigit() and word.split(":")[1].isdigit():
						if int(word.split(":")[0])<24 and int(word.split(":")[1])<60:
							hour=int(word.split(":")[0])
							minute=int(word.split(":")[1])
							securehourminute=True
			if word.isdigit() or word in translations.getraw("one") or word in translations.getraw("two"):
				if word in translations.getraw("one"):
					tmpnum=1
				elif word in translations.getraw("two"):
					tmpnum=2
				else:
					tmpnum=int(word)
				if len(t)-1>i:
					for j,k in enumerate(m):
						if t[i+1].lower()==k.lower():
							if (j+1==month and tmpnum<day) or (j+1<month):
								year+=1
							day=tmpnum
							month=j+1
				elif tmpnum<24 or tmpnum<60 and not securehourminute:
					if tmpnum>=24:
						minute=tmpnum
					else:
						if hour==0:
							hour=tmpnum
						elif minute==0:
							minute=tmpnum
						else:
							hour=minute
							minute=tmpnum
		t=float(datetime.datetime(year,month,day,hour,minute,second).strftime('%s'))
		thread.start_new_thread(waitmemo,(t,))
		mem["memo"][" ".join(args)]=t
		update_memory(mem)
		return translations.getstr("addmemo","memoadded").format(" ".join(args))
def rmmemo(args):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("removememo","saymemo"),"rmmemo")
	else:
		verify_existence("memo",{})
		mtd=" ".join(args)
		s=[0,0]
		for i,memo in enumerate(mem["memo"]):
			ts=similar(mtd,memo)
			if ts>=.65 and ts>s[0]:
				s=[ts,memo]
		if s[0]>0:
			ntd=mem["memo"][s[1]]
			del mem["memo"][s[1]]
			update_memory(mem)
			return translations.getstr("removememo","memoremoved").format(s[1])
		else:
			return translations.getstr("removememo","memonotfound")
def readmemo():
	verify_existence("memo",{})
	if len(mem["memo"])==1:
		prestr=translations.getstr("readmemo","one","prestr")
		aftstr=translations.getstr("readmemo","one","aftstr")
	else:
		prestr=translations.getstr("readmemo","multiple","prestr")
		aftstr=translations.getstr("readmemo","multiple","aftstr")
	lm=[]
	for m in mem["memo"]:
		lm.append(time.strftime(translations.getstr("readmemo","oneprint"),time.localtime(mem["memo"][m]))+" "+m)
	prestr=encode(prestr)
	output=translations.getstr("readmemo","print").format(prestr,str(len(mem["memo"])),aftstr,list_in_human_format(lm))
	return output

def timer(s):
	global timerenabled;timerenabled=[True,time.time()+s]
	time.sleep(s)
	timerenabled=[False,0]
	playsound("resources/sounds/timer.ogg")
def settimer(args):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("settimer","howmany"),"settimer")
	ts=0
	s=0
	for i,arg in enumerate(args):
		if arg.isdigit() or arg in translations.getraw("one") or arg in translations.getraw("two"):
			if arg in translations.getraw("one"):
				arg=1
			elif arg in translations.getraw("two"):
				arg=2
			s=int(arg)
			if len(args)>i+1:
				if args[i+1]==translations.getstr("minute") or args[i+1]==translations.getstr("minutes"):
					s*=60
					ts+=s
				elif args[i+1]==translations.getstr("hour") or args[i+1]==translations.getstr("hours"):
					s*=3600
					ts+=s
				else:
					ts+=s
			else:
				ts+=s
	if ts==0:
		return make_a_newinput(translations.getstr("settimer","howmany"),"settimer")
	else:
		thread.start_new_thread(timer,(ts,))
		return translations.getstr("settimer","setted").format(format_seconds(ts))
def checktimer():
	global timerenabled
	try:
		if timerenabled[0]:
			return translations.getstr("checktimer","eta").format(format_seconds(int(timerenabled[1]-time.time())))
		else:
			return encode(translations.getstr("checktimer","notimer"))
	except:
		return encode(translations.getstr("checktimer","notimer"))

def repeat(args):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("repeat","what"),"repeat")
	return " ".join(args)
def execute(args):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("execute","what"),"execute")
	elif args[0].lower() in translations.getraw("cancel"):
		return call_from_brain(translations.getstr("cancel"))
	else:
		args=[arg.lower() for arg in args]
		try:
			thread.start_new_thread(subprocess.call,(args,))
			return translations.getstr("execute","executing").format(" ".join(args))
		except Exception as e:
			log(traceback.format_exc())
			return translations.getstr("execute","error")
def calculate(args):
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("calculate","what"),"calculate")
	elif args[0].lower() in translations.getraw("cancel"):
		return call_from_brain(translations.getstr("cancel"))
	else:
		args=encode((" ".join(args)).lower())
		args=args.replace(encode(translations.getstr("plus")),"+").replace(encode(translations.getstr("minus")),"-").replace(encode(translations.getstr("for")),"*").replace("x","*").replace(encode(translations.getstr("divided")),"/")
		args=args.replace("+"," + ").replace("-"," - ").replace("*"," * ").replace("/"," / ").replace("  "," ").replace("  "," ")
		e=[]
		for word in args.split(" "):
			if word!="":
				if word=="+":
					e.append("+")
				elif word=="-":
					e.append("-")
				elif word=="*":
					e.append("*")
				elif word=="/":
					e.append("/")
				elif isnumber(word):
					e.append(str(float(word)))
		try:
			e=str(eval("".join(e)))
			if "." in e:
				if e.split(".")[1]=="0":
					e=e.split(".")[0]
			return e
		except:
			return make_a_newinput(translations.getstr("calculate","notvalid"),"calculate")

# Custom commands
def pairCustCmd(newcc, ctc=[]):
	if ctc==[] or ctc==[""]:
		return make_a_newinput(translations.getstr("custCmds","tellcmdpair"),"pairCustCmd",newcc)
	elif " ".join(ctc).lower().strip() in translations.getraw("cancel"):
		return call_from_brain(translations.getstr("cancel"))
	else:
		mem["custCmds"][mem["lang"]][" ".join(newcc).lower()]=" ".join(ctc).lower()
		update_memory(mem)
		updateCustCmds()
		return translations.getstr("custCmds","paired").format(" ".join(newcc).lower(), " ".join(ctc).lower())

def addCustCmd(args):
	verify_existence("custCmds",{})

	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("custCmds","tellcmdadd"),"addCustCmd")
	else:
		if not mem["lang"] in mem["custCmds"]:
			mem["custCmds"][mem["lang"]]={}
		return pairCustCmd(args)

def removeCustCmd(args):
	verify_existence("custCmds",{})

	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("custCmds","tellcmdrm"),"removeCustCmd")
	else:
		ctd=" ".join(args)
		if mem["lang"] in mem["custCmds"]:
			s=[0,""]
			for ccmd in mem["custCmds"][mem["lang"]]:
				ts=similar(ctd,ccmd)
				if ts>=.65 and ts>s[0]:
					s=[ts,ccmd]
			if s[0]>0:
				del mem["custCmds"][mem["lang"]][s[1]]
				if globalvars.brain.has_key(s[1]):
					del globalvars.brain[s[1]]
				update_memory(mem)
				return translations.getstr("custCmds","removed").format(s[1])
			else:
				return translations.getstr("custCmds","rmnotfound")
		else:
			return translations.getstr("custCmds","rmnotfound")

def listCustCmds():
	verify_existence("custCmds",{})

	if mem["lang"] in mem["custCmds"] and mem["custCmds"][mem["lang"]]!=[]:
		ccmds=[]
		for ccmd in mem["custCmds"][mem["lang"]]:
			ccmds.append(ccmd)
		if len(ccmds)==1:
			outtxt=translations.getstr("custCmds","listone")
		else:
			outtxt=translations.getstr("custCmds","listmore")

		return outtxt.format(len(ccmds), list_in_human_format(ccmds))

	else:
		return translations.getstr("custCmds","listno")

# Phone
def readMessages(args):
	if globalvars.onlineconnection:
		if not tdlib.isWorking:
			return translations.getstr("phone","notLogged")
		msgs=tdlib.getUnreadMessages()
		if msgs!=1:
			o=""
			for chat_name in msgs:
				tmpmsgs=[]
				for msg in msgs[chat_name]:
					if msg[0]=="text":
						tmpmsgs.append(msg[1])
					elif msg[0]=="messageVoiceNote":
						#playsound(msg[1])
						tmpmsgs.append(exec_for_output("playsound('"+msg[1]+"')"))
				o+=translations.getstr("phone","readMsgList").format(chat_name,"\n".join(tmpmsgs))
			return o
		else:
			return translations.getstr("phone","noUnreadMessages")
	else:
		return translations.getstr("internetneeded")
def markMessagesAsRead():
	if globalvars.onlineconnection:
		if not tdlib.isWorking:
			return translations.getstr("phone","notLogged")
		tdlib.readMessages(tdlib.unreadMessages)
		return translations.getstr("phone","markedAsRead")
	else:
		return translations.getstr("internetneeded")
def sendMessageText(to,args=[]):
	if globalvars.onlineconnection:
		if not tdlib.isWorking:
			return translations.getstr("phone","notLogged")
		if args==[] or args==[""]:
			return make_a_newinput(translations.getstr("phone","textOfMessage").format(to[2]),"sendMessageText",to)
		elif " ".join(args).lower().strip() in translations.getraw("cancel"):
			return call_from_brain(translations.getstr("cancel"))
		else:
			msg=" ".join(args)
			msg=msg.strip()
			tdlib.sendMessage(msg,to[1])
			to[2]=to[2].strip()
			if len(msg.split(" "))<=5:
				return translations.getstr("phone","messageSentShort").format(msg,to[2])
			else:
				return translations.getstr("phone","messageSent").format(to[2])
	else:
		return translations.getstr("internetneeded")
def sendMessage(args):
	if globalvars.onlineconnection:
		if not tdlib.isWorking:
			return translations.getstr("phone","notLogged")
		if args==[] or args==[""]:
			return make_a_newinput(translations.getstr("phone","toWhoMessage"),"sendMessage")
		elif args[0].lower() in translations.getraw("cancel"):
			return call_from_brain(translations.getstr("cancel"))
		else:
			to=" ".join(args)
			to=tdlib.searchContact(to)
			if to[1]!="":
				return sendMessageText(to)
			else:
				return make_a_newinput(translations.getstr("phone","contactNotFound"),"sendMessage")
	else:
		return translations.getstr("internetneeded")
def callTG(args):
	if globalvars.onlineconnection:
		if not tdlib.isWorking:
			return translations.getstr("phone","notLogged")
		return translations.getstr("notWorkingYet")
	else:
		return translations.getstr("internetneeded")

# System audio
def setSystemVolume(args):
	vol=None
	if args==[] or args==[""]:
		return make_a_newinput(translations.getstr("systemaudio","setvolumeask"),"setSystemVolume")
	elif args[0].lower() in translations.getraw("cancel"):
		return call_from_brain(translations.getstr("cancel"))
	else:
		for word in args:
			word=word.replace(".","").replace(",","").replace("!","").replace("%","")
			if isnumber(word):
				vol=int(word)
		if vol==None:
			return make_a_newinput(translations.getstr("systemaudio","setvolumepercentage"),"setSystemVolume")
		else:
			if vol>100:
				vol=100
			elif vol<10:
				vol=10
			_setSystemVolume(vol)
def turnUpSystemSound():
	vol=_getSystemVolume()+10
	if vol>100:
		vol=100
	_setSystemVolume(vol)
def turnDownSystemSound():
	vol=_getSystemVolume()-10
	if vol<10:
		vol=10
	_setSystemVolume(vol)

def reboot_iandi():
	playsound("resources/sounds/rebootiandi.ogg")
	os.execv(sys.executable,[sys.executable]+sys.argv)

# Search online answers
def searchanswer(args):
	if globalvars.onlineconnection:
		if args==[] or args==[""]:
			return make_a_newinput(translations.getstr("searchanswer","what"),"searchanswer",onlineconnection)
		else:
			pairs=apertium.listPairs()["responseData"]
			q=apertium.translate(encode2(" ".join(args)),mem["lang"],"eng",pairs)
			o=readurl("https://www.answers.com/search?q="+urllib.quote(q)).replace("\n","")
			if re.findall("<link rel='canonical' href='(.*?)'>",o)[0]=="https://www.answers.com/search":
				r=re.findall('"slug":"(.*?)"',o)
				a=re.findall('"num_answers":(.*?),',o)
				o=""
				for i,n in enumerate(a):
					if n!="0" and r[i]!="Uncategorized" and o=="":
						o=r[i]
						break
				if o!="":
					o=readurl("https://www.answers.com/Q/"+o).replace("\n","")
					if not re.findall("<title>(.*?)</title>",o)[0]=="404 Not Found | Answers.com":
						o=re.findall('name="description" content="(.*?)">',o)[0]
						if not o=="Answers is the place to go to get the answers you need and to ask the questions you want":
							o=apertium.translate(o.upper(),"eng",mem["lang"],pairs)
						else:
							o=translations.getstr("searchanswer","notfound")
					else:
						o=translations.getstr("searchanswer","notfound")
				else:
					o=translations.getstr("searchanswer","notfound")
			else:
				o=re.findall('name="description" content="(.*?)">',o)[0]
				o=apertium.translate(o.upper(),"eng",mem["lang"],pairs)
			return gstr(o)
	else:
		return translations.getstr("searchanswer","internetneeded")

# Translate
def translate(args):
	if globalvars.onlineconnection:
		return translations.getstr("notWorkingYet")
	else:
		return translations.getstr("internetneeded")

# Music
def playmusic(path):
	global playing_now
	global music_player
	try:
		music_player.stop()
	except:
		pass
	playing_now=True
	music_player=vlc.MediaPlayer("file://"+path)
	music_player.audio_set_volume(mediaVol)
	music_player.play()
	time.sleep(1.5)
	music_player.audio_set_mute(0)
	time.sleep(music_player.get_length()/1000)
	playing_now=False
def stopmusic(out=True):
	global playing_now
	global music_player
	if playing_now:
		music_player.stop()
		playing_now=False
	else:
		if out:
			return translations.getstr("music","nothingplay")
def musicgetifpaused():
	global music_pause
	try:
		return music_pause
	except:
		return False
def pausemusic(out=True):
	global playing_now
	global music_player
	global music_pause
	global music_internal_pause
	try:
		isplaying=playing_now or music_player.is_playing()
	except:
		isplaying=playing_now
	if isplaying:
		if not out:
			try:
				music_internal_pause
			except:
				music_internal_pause=False
			if not music_internal_pause:
				music_player.pause()
				music_internal_pause=True
		else:
			try:
				music_pause
			except:
				music_pause=False
			if not music_pause:
				music_player.set_pause(1)
				#playing_now=False
				music_pause=True
				#print(music_player.is_playing())
	else:
		if out:
			return translations.getstr("music","nothingplay")
def resumemusic(out=True):
	global playing_now
	global music_player
	global music_pause
	global music_internal_pause
	if playing_now:
		music_player.play()
		playing_now=True
		music_pause=False
		if not out:
			music_internal_pause=False
	else:
		if out:
			return translations.getstr("music","wasnothingplay")
def setvolume(args):
	global music_player
	global mediaVol
	vol=None
	try:
		if args==[] or args==[""]:
			return make_a_newinput(translations.getstr("music","setvolumeask"),"setvolume")
		elif args[0].lower() in translations.getraw("cancel"):
			return call_from_brain(translations.getstr("cancel"))
		else:
			for word in args:
				word=word.replace(".","").replace(",","").replace("!","").replace("%","")
				if isnumber(word):
					vol=int(word)
			if vol==None:
				return make_a_newinput(translations.getstr("music","setvolumepercentage"),"setvolume")
			else:
				if vol>100:
					vol=100
				elif vol<0:
					vol=0
				mediaVol=vol
				music_player.audio_set_volume(vol)
	except:
		return translations.getstr("music","nothingplay")
def turnupsound():
	global music_player
	global mediaVol
	try:
		try:
			vol=music_player.audio_get_volume()+10
		except:
			vol=mediaVol+10
		if vol>100:
			vol=100
		mediaVol=vol
		if mediaVol>_getSystemVolume():
			_setSystemVolume(vol)
		music_player.audio_set_volume(vol)
	except:
		return translations.getstr("music","nothingplay")
def turndownsound():
	global music_player
	global mediaVol
	try:
		try:
			vol=music_player.audio_get_volume()-10
		except:
			vol=mediaVol-10
		if vol<0:
			vol=0
		mediaVol=vol
		music_player.audio_set_volume(vol)
	except:
		return translations.getstr("music","nothingplay")
def togglemutesound():
	global music_player
	try:
		music_player.audio_set_mute(not music_player.audio_get_mute())
	except:
		return translations.getstr("music","nothingplay")
def oldDownloadmusic(url):
	r=1
	i=0
	while r!=0 and i<4:
		r=os.system("youtube-dl -o '/tmp/iandi-music.%(ext)s' --extract-audio --audio-format mp3 "+url)
		i+=1
	if r==0:
		playmusic("/tmp/iandi-music.mp3")
def downloadmusicforstream(url,o="/tmp/iandi-music.%(ext)s"):
	r=1
	i=0
	while r!=0 and i<4:
		r=os.system("youtube-dl -o "+repr(o)+" --extract-audio --audio-format mp3 "+repr(url)+" > /dev/null")
		i+=1
def downloadmusic(url):
	def getsize(filepath):
		return os.path.getsize(filepath)

	try:
		os.system("rm /tmp/iandi-music.mp3 2> /dev/null")
	except:
		pass

	#minsize=2097152 # 2MB
	#minsize=1048576 # 1MB
	#minsize=524288 # 0.5MB
	#minsize=262144 # 256KB
	#minsize=51200 # 50KB
	minsize=1024 # 1KB

	checksleep=.1

	thread.start_new_thread(downloadmusicforstream,(url,))

	startedDownload=True
	timeElapsed=0.0
	exitCheckFileExist=False
	while not os.path.isfile("/tmp/iandi-music.mp3.part") and not os.path.isfile("/tmp/iandi-music.mp3") and not exitCheckFileExist:
		time.sleep(checksleep)
		timeElapsed+=checksleep
		if timeElapsed>=10.0:
			startedDownload=False
	if startedDownload:
		try:
			while getsize("/tmp/iandi-music.mp3.part")<=minsize:
				time.sleep(checksleep)
			filepath="/tmp/iandi-music.mp3.part"
		except:
			while getsize("/tmp/iandi-music.mp3")<=minsize:
				time.sleep(checksleep)
			filepath="/tmp/iandi-music.mp3"

		playmusic(filepath)
	else:
		playsound("resources/sounds/error.ogg")
def music(args,sayDownloading=True):
	if globalvars.onlineconnection:
		if args==[] or args==[""]:
			return make_a_newinput(translations.getstr("music","what"),"music")
		elif args[0].lower() in translations.getraw("cancel"):
			return call_from_brain(translations.getstr("cancel"))
		else:
			q=" ".join(args)
			url="https://www.youtube.com/watch?v="+re.findall(r'{"webCommandMetadata":{"url":"/watch\?v=(.*?)"',readurl("https://www.youtube.com/results?q="+urllib.quote(encode2(q))))[0]
			title=re.findall(r'<meta name="title" content="(.*?)">',readurl(url))[0]
			thread.start_new_thread(downloadmusic,(url,))
			if sayDownloading:
				try:
					return translations.getstr("music","downloading").format(encode3(title))
				except:
					return translations.getstr("music","downloading").format("")
	else:
		return translations.getstr("internetneeded")

# News
def news():
	if globalvars.onlineconnection:
		r=newsapi.topheads(country=countries.getby_alpha3(mem["country"])["cca2"],pageSize=4,source=False)
		if type(r)==type("") and r.startswith("!Error: "):
			log(r)
			return translations.getstr("news","error")
		else:
			return list_in_human_format(r)
	else:
		return translations.getstr("internetneeded")

# Places - work in progress
def restaurant():
	if globalvars.onlineconnection:
		output=""
		rawxml=readurl('http://overpass-api.de/api/interpreter?data=[bbox:40.8512,14.2208,40.8600,14.2303];(node["amenity"="restaurant"];way["amenity"="restaurant"];relation["amenity"="restaurant"];);out center;')
		xml=xmletree.fromstring(rawxml)
		rawallp=xml.iter("node")
		allp={}
		i=0
		for node in rawallp:
			allp[i]={}
			for tag in node:
				allp[i][tag.attrib["k"]]=tag.attrib["v"]
			i+=1
		if i>0:
			output=translations.getstr("restaurant","near").format(str(i))
			n=0
			for p in allp:
				if n>0 and n==i-1:
					output+="\n"+"e "
				else:
					output+="\n"
				output+=translations.getstr("restaurant","print").format(allp[p]["name"],allp[p]["addr:street"],allp[p]["addr:housenumber"])
				if n==i-1:
					output+="."
				elif n<i-2:
					output+=","
				n+=1
		else:
			output=translations.getstr("restaurant","no")
		return output
	else:
		return translations.getstr("internetneeded")
def coffee():
	if globalvars.onlineconnection:
		output=""
		rawxml=readurl('http://overpass-api.de/api/interpreter?data=[bbox:40.8512,14.2208,40.8600,14.2303];(node["amenity"="cafe"];way["amenity"="cafe"];relation["amenity"="cafe"];);out center;')
		xml=xmletree.fromstring(rawxml)
		rawallp=xml.iter("node")
		allp={}
		i=0
		for node in rawallp:
			allp[i]={}
			for tag in node:
				allp[i][tag.attrib["k"]]=tag.attrib["v"]
			i+=1
		if i>0:
			output=translations.getstr("coffee","near").format(str(i))
			n=0
			for p in allp:
				if n>0 and n==i-1:
					output+="\n"+"e "
				else:
					output+="\n"
				output+=translations.getstr("coffee","print").format(allp[p]["name"],allp[p]["addr:street"],allp[p]["addr:housenumber"])
				if n==i-1:
					output+="."
				elif n<i-2:
					output+=","
				n+=1
		else:
			output=translations.getstr("coffee","no")
		return output
	else:
		return translations.getstr("internetneeded")
def market():
	if globalvars.onlineconnection:
		output=""
		rawxml=readurl('http://overpass-api.de/api/interpreter?data=[bbox:40.8512,14.2208,40.8600,14.2303];(node["shop"="supermarket"];way["shop"="supermarket"];relation["shop"="supermarket"];);out center;')
		xml=xmletree.fromstring(rawxml)
		rawallp=xml.iter("node")
		allp={}
		i=0
		for node in rawallp:
			allp[i]={}
			for tag in node:
				allp[i][tag.attrib["k"]]=tag.attrib["v"]
			i+=1
		if i>0:
			output=translations.getstr("market","near").format(str(i))
			n=0
			for p in allp:
				if n>0 and n==i-1:
					output+="\n"+"e "
				else:
					output+="\n"
				output+=translations.getstr("market","print").format(allp[p]["name"],allp[p]["addr:street"],allp[p]["addr:housenumber"])
				if n==i-1:
					output+="."
				elif n<i-2:
					output+=","
				n+=1
		else:
			output=translations.getstr("market","no")
		return output
	else:
		return translations.getstr("internetneeded")
def bank():
	if globalvars.onlineconnection:
		output=""
		rawxml=readurl('http://overpass-api.de/api/interpreter?data=[bbox:40.8512,14.2208,40.8600,14.2303];(node["amenity"="bank"];way["amenity"="bank"];relation["amenity"="bank"];);out center;')
		xml=xmletree.fromstring(rawxml)
		rawallp=xml.iter("node")
		allp={}
		i=0
		for node in rawallp:
			allp[i]={}
			for tag in node:
				allp[i][tag.attrib["k"]]=tag.attrib["v"]
			i+=1
		if i>0:
			output=translations.getstr("bank","near").format(str(i))
			n=0
			for p in allp:
				if n>0 and n==i-1:
					output+="\n"+"e "
				else:
					output+="\n"
				output+=translations.getstr("bank","print").format(allp[p]["name"],allp[p]["addr:street"],allp[p]["addr:housenumber"])
				if n==i-1:
					output+="."
				elif n<i-2:
					output+=","
				n+=1
		else:
			output=translations.getstr("bank","no")
		return output
	else:
		return translations.getstr("internetneeded")
"""def hotel():
	"""
