#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,re,ast,random,time,datetime,pyttsx3,iso639
try:
	import thread
except:
	import _thread as thread
import globalvars
try:
	import terminal_virtualface as virtualface
	globalvars.virtualface_enabled=True
except:
	globalvars.virtualface_enabled=False
from pocketsphinx import LiveSpeech
import speech_recognition as sr
from playsound import playsound
from rmem import *
from difflib import SequenceMatcher

def log(txt):
	# Append a line to log with timestamp
	txt=str(datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S"))+" - "+str(txt)
	print(txt)
	with open("iandi.log","a") as log:
		log.write(txt+"\n")
		log.close()

def quit(exitCode,speak=True):
	try:
		if speak:
			if globalvars.brain.has_key("CBM"):
				globalvars.cm=resultcode(globalvars.brain["CBM"])
				output(globalvars.cm)
			else:
				output("Exit...")
		
		if globalvars.executiontype!="lite":
			globalvars.detector.terminate()

		globalvars.faceExecuting=False
		os.system("tput cnorm")
	except Exception as e:
		log(e)
	
	exit(exitCode)

def addhistory(txt):
	# Add last used command to history, with a max of 10 commands
	globalvars.history.append(txt)
	if len(globalvars.history)>10:
		globalvars.history.pop(0)
def readurl(url):
	# Retrun page content of url
	page=urllib.urlopen(url)
	content=page.read()
	page.close()
	return content
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
def similar(a,b):
	# Return percentage of similarity between A and B
	try:
		a=encode(a)
	except:
		pass
	try:
		b=encode(b)
	except:
		pass
	return SequenceMatcher(None,a,b).ratio()
def getlang():
	# Return current language setted
	return mem["lang"]
def setbrain():
	try:
		brainfile="brains/brain-"+getlang()
		if not os.path.isfile(brainfile):
			log("Lang "+iso639.get_eng(getlang())+" not supported in brains. Swithing to english.")
			updlang("eng")
			brainfile="brains/brain-eng"
		tbrain=open(brainfile,"r")
		globalvars.brain=ast.literal_eval(tbrain.read())
		tbrain.close()
	except Exception as e:
		log(brainfile+" error: "+str(e))
		globalvars.brain={}
	globalvars.brainlang=mem["lang"]
def checklang():
	if globalvars.brainlang!=mem["lang"]:
		setbrain()
def updlang(newlang,returnString=False):
	setlang(newlang)
	setbrain()
	if returnString:
		return "English setted as language."
def sttmodel(lang=""):
	# Return speech to text model's files
	availablelangs=list(os.walk("sttlangs/"))[0][1]
	if not lang in availablelangs:
		for al in availablelangs:
			if lang.lower()==al.lower().split("-")[0]:
				lang=al
			if not lang in availablelangs:
				lang="eng"
	modelpath="sttlangs/"+lang+"/"
	modelfiles=list(os.walk(modelpath))[0]
	hmm=modelpath+modelfiles[1][0]+"/"
	for f in modelfiles[2]:
		if f.endswith(".lm.bin"):
			lm=modelpath+f
		if f.endswith(".dict"):
			dic=modelpath+f
	return [hmm,lm,dic]
def voice(txt):
	if txt!=None and txt!="":
		maxwordsforonline=60
		onlinetts=False
		if globalvars.onlineconnection and len(txt.split(" "))<=maxwordsforonline and onlinetts:
			# Demo version of IBM tts with italian voice. Test purpose only, so keep "onlinetts" var to false.
			urllib.urlretrieve('https://text-to-speech-demo.ng.bluemix.net/api/v3/synthesize?text='+urllib.quote_plus(encode2(txt))+'&voice=it-IT_FrancescaVoice&download=true&accept=audio%2Fmp3',"/tmp/voice.mp3")
		else:
			if globalvars.rvoicelang!=getlang():
				globalvars.rvoicelang=getlang()
				globalvars.voicelang=iso639.get_iso1(globalvars.rvoicelang)
				if not globalvars.voicelang:
					globalvars.voicelang=globalvars.rvoicelang
				globalvars.voicelang=globalvars.voicelang.lower()
				globalvars.voicetts.setProperty("voice",globalvars.voicelang+"+f1")
			globalvars.voicetts.say(txt)
		globalvars.voicebusy=True
		if globalvars.onlineconnection and len(txt.split(" "))<=maxwordsforonline and onlinetts:
			playsound("/tmp/voice.mp3")
		else:
			globalvars.voicetts.runAndWait()
		#
		globalvars.voicetts.stop()
		globalvars.voicebusy=False
def face():
	globalvars.faceExecuting=True

	oldc=globalvars.c
	if globalvars.virtualface_enabled:
		os.system("tput civis")
	while globalvars.faceExecuting:
		if globalvars.c!="":
			oldc=globalvars.c
		if globalvars.virtualface_enabled:
			if globalvars.voicebusy:
				virtualface.face(speak=True,expr=globalvars.expr)
			else:
				virtualface.face()
		else:
			os.system('cls' if os.name=='nt' else 'clear')
		print(oldc)
		if globalvars.virtualface_enabled:
			time.sleep(.1)
		else:
			time.sleep(1)
	os.system("tput cnorm")
def resultcode(cm,args=[]):
	if cm!=None:
		if "|&|" in cm:
			cm=cm.split("|&|")[(random.randrange(0,len(cm.split("|&|"))))]
	if cm!=None:
		if cm.startswith(":goto:") and cm.endswith(":goto:"):
			if globalvars.brain.has_key(cm[6:-6]):
				cm=resultcode(globalvars.brain[cm[6:-6]],args)
	if cm!=None:
		if cm.startswith("exec%=%") and cm.endswith("%=%exec"):
			try:
				exec("cm="+"".join(re.findall('exec%=%(.*?)%=%exec',cm)))
			except KeyboardInterrupt:
				quit(0)
			except Exception as e:
				log(getattr(e,"message",e))

				if globalvars.brain.has_key("ERR"):
					cm=globalvars.brain["ERR"] # ERR must be only string to avoid problems and recursion over them
				else:
					cm="Error, check the log."
	if cm==None:
		cm=""
	return cm
def elabout(s,outfn):
	f=[] # [type,in]
	outhist=[]

	def printInLine(txt):
		sys.stdout.write(encode2(txt))
		sys.stdout.flush()

	if outfn=="print":
		outfn=printInLine

	search=re.findall(r'<<exec<(.*?)>exec>>',s)
	if len(search)>0:
		for i,r in enumerate(search):
			estr="<<exec<{}>exec>>".format(r)
			pre=s.split(estr)[0]
			if pre!="":
				f.append(["str",pre])
			f.append(["exe",r])
			s=estr.join(s.split(estr)[1:])
			if i==len(search)-1 and len(s)>0:
				f.append(["str",s])
	else:
		f.append(["str",s])

	for i,e in enumerate(f):
		if e[0]=="str":
			outhist.append(e[1])
			if outfn==printInLine:
				outfn("".join(outhist)+"\r")
			else:
				outfn(e[1])
		elif e[0]=="exe":
			exec("exertn="+e[1],globals())
			if exertn!=None:
				outhist.append(str(exertn))
				if outfn==printInLine:
					outfn("".join(outhist)+"\r")
				else:
					outfn(str(exertn))
		if i==len(f)-1 and outfn==printInLine:
			printInLine("\n")
def output(o,close=True,setexpr=[]):
	newinput=False
	o=encode(o)
	if o.startswith("<<callbrain<") and o.endswith(">callbrain>>"):
		callBrain(o[12:-12])
	else:
		if o.startswith("<<newinput<") and o.endswith(">newinput>>"):
			newinput=True
			o,f=o[11:-11].split("<,>")
			farg=""
			if "," in f:
				farg=",".join(f.split(",")[1:])+","
				#farg=f.split(",")[1:]
				#for i,arg in enumerate(farg):
				#	if not "(" in arg and not "[" in arg and not "{" in arg:
				#		farg[i]=repr(arg)
				#farg=",".join(farg)+","
				f=f.split(",")[0]
		if globalvars.executiontype=="lite":
			#print(o)
			elabout(o,"print")
		else:
			exprl=[]
			for e in setexpr:
				globalvars.expr.append(e)
				exprl.append(len(globalvars.expr)-1)
			if o!="":
				try:
					#voice(o) #thread.start_new_thread(voice,(o,))
					elabout(o,voice)
				except KeyboardInterrupt:
					quit(0,False)
				except Exception as err:
					log(err)
					quit(1)
			for e in exprl:
				globalvars.expr.pop(e)
		if newinput:
			exec("output("+f+"("+farg+str(sinput().split(" "))+"))")
		else:
			if close:
				globalvars.notcheckword=False
				if globalvars.executiontype!="lite":
					playsound("peeb.ogg")

def callBrain(c):
	globalvars.c=c
	if globalvars.c!=globalvars.exitcommand:
		rawc=globalvars.c
		globalvars.c=globalvars.c.lower()
		if globalvars.brain.has_key(globalvars.c):
			addhistory(globalvars.c)
			globalvars.cm=resultcode(globalvars.brain[globalvars.c])
			output(globalvars.cm)
		else:
			atto=0
			attn=""
			num=0
			cwords=globalvars.c.split(" ")
			rawcwords=rawc.split(" ")
			for a in globalvars.brain:
				for n,word in enumerate(cwords):
					ccutted=" ".join(cwords[:len(cwords)-n])
					if similar(ccutted,a)>=globalvars.anstollerance:
						if similar(ccutted,a)>atto:
							atto=float(similar(ccutted,a))
							attn=a
							args=rawcwords[len(rawcwords)-n:]
			if atto!=0:
				globalvars.c=attn
				#print("> {}".format(globalvars.c))
				#print("< Args: {}".format(args))
				addhistory(globalvars.c)
				globalvars.cm=resultcode(globalvars.brain[globalvars.c],args)
				output(globalvars.cm)
			elif globalvars.brain.has_key("CNFE"):
				addhistory("CNFE")
				globalvars.cm=resultcode(globalvars.brain["CNFE"])
				if globalvars.history[-3:]!=["CNFE","CNFE","CNFE"]:
					closeAft=False
				else:
					closeAft=True
				output(globalvars.cm,close=closeAft,setexpr=["eyes-semi-closed"])
			else:
				addhistory("CNFE")
				if globalvars.history[-3:]!=["CNFE","CNFE","CNFE"]:
					closeAft=False
				else:
					closeAft=True
				output("Command not found.",close=closeAft)
	else:
		quit(0)

def sr_adjust():
	while True:
		if globalvars.onlineconnection:
			with sr.Microphone() as source:
				globalvars.r.adjust_for_ambient_noise(source)
		time.sleep(10800)
def googleSTT(first=True,lang=""):
	with sr.Microphone() as source:
		if first:
			rlang=getlang()
			lang=iso639.get_iso1(rlang)
			if not lang:
				lang=rlang
			playsound("beep.ogg")
			first=False
		audio=globalvars.r.listen(source)
		try:
			o=globalvars.r.recognize_google(audio,language=lang)
		except Exception as e:
			log("googleSTT error: {}".format(e))
			o=""
		if o=="":
			o=googleSTT(first,lang)
	return o
def deepspeech():
	lang=getlang()
	if not lang:
		lang=rlang
	if globalvars.executiontype=="noui":
		verbose="verbose"
	else:
		verbose=""
	#playsound("beep.ogg") moved directly in deepspeechSTT.py
	out=os.popen("python3 deepspeechSTT.py {} {}".format(repr(lang),repr(verbose))).read()
	rout=out
	if verbose=="verbose":
		print(out)
	for i,line in enumerate(out.split("\n")):
		if line=="----":
			break
	out=" ".join(out.split("\n")[i+1:])
	out=out.replace("\n"," ").strip()
	if out=="":
		log("deepspeechSTT.py error: Segmentation fault")
		#out=deepspeech(lang)
	else:
		out=out[0].capitalize()+out[1:]
	return out
def sinput():
	if globalvars.executiontype=="lite":
		try:
			o=raw_input("> ")
		except KeyboardInterrupt:
			quit(0)
		except Exception as e:
			log(e)
			quit(1)
	else:
		#playsound("beep.ogg")
		pausemusic(False)
		if not globalvars.onlineconnection:
			# Pocketsphinx speech to text (offline)
			hmm,lm,dic=sttmodel(getlang())
			playsound("beep.ogg")
			try:
				for o in LiveSpeech(hmm=hmm,lm=lm,dic=dic):
					if o!="":
						break
			except KeyboardInterrupt:
				quit(0)
			except Exception as e:
				log(e)
				quit(1)
			
			# Mozilla speech to text (offline)
			#o=deepspeech()
		else:
			try:
				# Google speech to text (online)
				o=googleSTT()
			except KeyboardInterrupt:
				quit(0)
			except Exception as e:
				log(e)
				quit(1)
	return encode(o)
def hotword():
	globalvars.notcheckword=True
def checkhotword():
	return globalvars.notcheckword
def checkOnlineConnection(onceCheck=False):
	host="https://lite.duckduckgo.com/lite/"#"1.1.1.1"
	checksleep=5.0
	neverConnected=True

	while True:
		try:
			readurl(host)
			globalvars.onlineconnection=True
			if neverConnected:
				globalvars.r=sr.Recognizer()
				thread.start_new_thread(sr_adjust,())
				neverConnected=False
		except Exception as e:
			globalvars.onlineconnection=False

		if onceCheck:
			break
		else:
			time.sleep(checksleep)

# Importing plugins
#from plugins import *