#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,json,time,random
try:
	import thread
except:
	import _thread
from ctypes.util import find_library
from ctypes import *
from difflib import SequenceMatcher
from playsound import playsound

version="0.1"

global isWorking;isWorking=True

def log(txt):
	txt=json.dumps(txt).encode('utf-8')
	with open("tdlib.log","a+") as l:
		l.write(str(txt)+"\n")
		l.close()

# You MUST obtain your own api_id and api_hash at https://my.telegram.org
# and use them here or in api.conf
api_id=17349
api_hash="344583e45741c457fe1862106095a5eb"

apiConfP="{}/api.conf".format(os.path.dirname(os.path.abspath(__file__)))
if os.path.isfile(apiConfP):
	with open(apiConfP,"r") as apiConfF:
		apiConf=apiConfF.read()
		apiConfF.close()
	apiConf=apiConf.split("\n")
	if len(apiConf)>=2 and apiConf[0]!="" and apiConf[1]!="":
		try:
			apiConf[0]=int(apiConf[0])
			api_id,api_hash=apiConf[:2]
			api_id=api_id.strip()
			api_hash=api_hash.strip()
		except:
			log("Error reading {}".format(apiConfP))

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

def close(errorCode=0,exitStr=""):
	global isWorking;isWorking=False
	if exitStr!="":
		print(exitStr)
	if __name__=="__main__":
		exit(errorCode)

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

def play(fileaudio):
	thread.start_new_thread(playsound,(os.path.dirname(os.path.abspath(__file__))+"/"+fileaudio,))

global eventHistory;eventHistory=[]
global maxEventHistory;maxEventHistory=500
def getEventHistory():
	global eventHistory
	return eventHistory
def getsync(req):
	id=(str(time.time())+str(random.randint(1000,9999))).replace(".","")
	req["@extra"]=id
	oldHistory=getEventHistory()[0:]
	td_send(req)
	found=False
	while not found:
		if getEventHistory()!=oldHistory:
			last=oldHistory[0]
			for i,e in enumerate(getEventHistory()):
				if e==last:
					oldHistory=getEventHistory()[0:]
					break
				else:
					if "@extra" in e:
						if e["@extra"]==id:
							r=e
							found=True
							break
		time.sleep(1)
	return r

global listening;listening=False
global connected;connected=0
global contacts;contacts={}
global chats;chats={}
global unreadMessages;unreadMessages={}

# load shared library
tdjson_path = find_library('libtdjson') or 'tdjson.dll'
if tdjson_path is None:
	close(1,"Can't find tdjson library.")
try:
	tdjson=CDLL(tdjson_path)
except:
	try:
		tdjson=CDLL("/usr/local/lib/libtdjson.so")
	except:
		close(1,"Can't find tdjson library.")

# initialize TDLib log with desired parameters
def on_fatal_error_callback(error_message):
	print('TDLib fatal error: ', error_message)

def td_execute(query):
	query = json.dumps(query).encode('utf-8')
	result = td_json_client_execute(None, query)
	if result:
		result = json.loads(result.decode('utf-8'))
	return result

# simple wrappers for client usage
def td_send(query):
	query = json.dumps(query).encode('utf-8')
	td_json_client_send(client, query)

def td_receive():
	result = td_json_client_receive(client, 1.0)
	if result:
		result = json.loads(result.decode('utf-8'))
	return result

def eventsCatcher():
	global listening
	global connected
	global eventHistory
	global maxEventHistory
	global contacts
	global chats
	global unreadMessages
	
	# main events cycle
	listening=True
	while listening:
		event = td_receive()
		if event:
			eventHistory.insert(0,event)
			if len(eventHistory)>maxEventHistory:
				eventHistory.pop(-1)
			
			# process authorization states
			if event['@type'] == 'updateAuthorizationState':
				auth_state = event['authorization_state']

				# if client is closed, we need to destroy it and create new client
				if auth_state['@type'] == 'authorizationStateClosed':
					break

				# set TDLib parameters
				if auth_state['@type'] == 'authorizationStateWaitTdlibParameters':
					td_send({
						"@extra":"internal",
						'@type': 'setTdlibParameters',
						'parameters': {
							'database_directory': os.path.dirname(os.path.abspath(__file__))+'/tdlibDB',
							'use_message_database': True,
							'use_secret_chats': False,
							'api_id': 802978,
							'api_hash': '324516b19ffc5ae8e3b9adf3d374ab1a',
							'system_language_code': 'en',
							'device_model': 'Assistant',
							'system_version': 'Linux',
							'application_version': version,
							'enable_storage_optimizer': True
						}
					})

				# set an encryption key for database to let know TDLib how to open the database
				if auth_state['@type'] == 'authorizationStateWaitEncryptionKey':
					td_send({"@extra":"internal",'@type': 'checkDatabaseEncryptionKey', 'key': 'my_key'})

				# enter phone number to log in
				if auth_state['@type'] == 'authorizationStateWaitPhoneNumber':
					close(2,"Login required. Use telegramlogin.py")
					return None
					phone_number = raw_input('Please enter your phone number: ')
					td_send({"@extra":"internal",'@type': 'setAuthenticationPhoneNumber', 'phone_number': phone_number})

				# wait for authorization code
				if auth_state['@type'] == 'authorizationStateWaitCode':
					code = raw_input('Please enter the authentication code you received: ')
					td_send({"@extra":"internal",'@type': 'checkAuthenticationCode', 'code': code})

				# wait for first and last name for new users
				if auth_state['@type'] == 'authorizationStateWaitRegistration':
					first_name = raw_input('Please enter your first name: ')
					last_name = raw_input('Please enter your last name: ')
					td_send({"@extra":"internal",'@type': 'registerUser', 'first_name': first_name, 'last_name': last_name})

				# wait for password if present
				if auth_state['@type'] == 'authorizationStateWaitPassword':
					password = raw_input('Please enter your password: ')
					td_send({"@extra":"internal",'@type': 'checkAuthenticationPassword', 'password': password})
			
			elif event["@type"]=="ok":
				if connected<=4:
					connected+=1
					td_send({
						"@extra":"internal",
						"@type":"getContacts"
					})
					td_send({
						"@extra":"internal",
						"@type":"getChats",
						"offset_order":2**63-1,
						"offset_chat_id":0,
						"limit":100
					})
			
			elif event["@type"]=="error":
				print("Error: "+event["message"]+"\nCode: "+str(event["code"]))
			
			elif event["@type"]=="users":
				for id in event["user_ids"]:
					if not id in contacts:
						contacts[id]={
							"id":id,
							"name":"",
							"lastname":""
						}
						td_send({
							"@extra":"internal",
							"@type":"getUser",
							"user_id":id
						})
			elif event["@type"]=="user":
				infos={
					"id":event["id"],
					"username":event["username"],
					"name":event["first_name"],
					"last_name":event["last_name"],
					"phone":event["phone_number"]
				}
				contacts[event["id"]].update(infos)
			
			elif event["@type"]=="chats":
				for id in event["chat_ids"]:
					if not id in chats:
						chats[id]={}
					td_send({
						"@extra":"internal",
						"@type":"getChat",
						"chat_id":id
					})
			elif event["@type"]=="chat":
				chats[event["id"]]=event
				if event["unread_count"]>0:
					# using more request to get all unreaded messages cause a bug wich return only one message at request
					td_send({
						"@extra":"internal",
						"@type":"getChatHistory",
						"chat_id":event["id"],
						"from_message_id":0,
						"offset":0,
						"limit":1,
						"only_local":False
					})
					if event["unread_count"]>1:
						td_send({
							"@extra":"internal",
							"@type":"getChatHistory",
							"chat_id":event["id"],
							"from_message_id":event["last_message"]["id"], # using id of last_message instead of 0 to use offset to get older messages
							"offset":0,
							"limit":event["unread_count"]-1,
							"only_local":False
						})
			elif event["@type"]=="messages":
				for mess in event["messages"]:
					if "content" in mess and ("text" in mess["content"] or mess["content"]["@type"]=="messageVoiceNote"):
						if mess["content"]["@type"]=="messageVoiceNote":
							if not mess["content"]["voice_note"]["voice"]["local"]["is_downloading_completed"]:
								td_send({
									"@type":"downloadFile",
									"file_id":mess["content"]["voice_note"]["voice"]["id"],
									"priority":32,
									"offset":0,
									"limit":0,
									"synchronous":True
								})
						fromChatId=mess["chat_id"]
						messId=mess["id"]
						if not fromChatId in unreadMessages:
							unreadMessages[fromChatId]={}
						if not mess["id"] in unreadMessages[fromChatId]:
							if mess["content"]["@type"]=="messageVoiceNote" and mess["content"]["voice_note"]["voice"]["local"]["is_downloading_completed"]:
								mess=mess["content"]["voice_note"]["voice"]
								mess["@type"]="messageVoiceNote"
							unreadMessages[fromChatId][messId]=mess
							#log(unreadMessages)
			elif event["@type"]=="file":
				if event["local"]["is_downloading_completed"]:
					for chat_id in unreadMessages:
						for mess in unreadMessages[chat_id]:
							if "@type" in unreadMessages[chat_id][mess] and unreadMessages[chat_id][mess]["@type"]=="messageVoiceNote":
								if unreadMessages[chat_id][mess]["content"]["voice_note"]["voice"]["remote"]["id"]==event["remote"]["id"]:
									fileVoiceNote=event
									fileVoiceNote["@type"]="messageVoiceNote"
									unreadMessages[chat_id][mess]=fileVoiceNote
									break
									break
			
			elif event["@type"]=="updateUnreadMessageCount":
				if event["unread_count"]>0:
					play("msg_incoming.mp3")
				unreadMessages={}
				td_send({
					"@extra":"internal",
					"@type":"getChats",
					"offset_order":2**63-1,
					"offset_chat_id":0,
					"limit":100
				})
			
			#elif event["@type"]=="updateUnreadChatCount":
			#	print(event)
			
			else:
				#if "message_id" in str(event) and not "last_message" in str(event):
				#	log(event)
				# handle an incoming update or an answer to a previously sent request
				if event["@type"].startswith("update"):
					#print(event["@type"])
					pass
				else:
					#print(event)
					#sys.stdout.flush()
					pass

def start():
	thread.start_new_thread(eventsCatcher,())

def _stop():
	global listening
	global client
	listening=False
	time.sleep(1.5)
	td_json_client_destroy(client)
def stop():
	thread.start_new_thread(_stop,())

def searchContact(to):
	global contacts
	global chats
	touser=[.5,""]
	for contact in contacts.keys()+chats.keys():
		if contact in contacts:
			infos=contacts[contact]
			name=infos["name"]+" "+infos["lastname"]
		else:
			infos=chats[contact]
			if infos!={}:
				name=infos["title"]
			else:
				name=""
		simil=similar(name,to)
		if simil>=touser[0]:
			touser=[simil,infos["id"],name]
	return touser

def getUnreadMessages():
	global chats
	global unreadMessages
	if len(unreadMessages)>0:
		o={}
		for chat_id in unreadMessages:
			if not chats[chat_id]["title"] in o:
				o[chats[chat_id]["title"]]=[]
			for msg in unreadMessages[chat_id]:
				
				if unreadMessages[chat_id][msg]["@type"]=="messageVoiceNote":
					msgType="messageVoiceNote"
					content=unreadMessages[chat_id][msg]["local"]["path"]
				else:
					msgType="text"
					content=unreadMessages[chat_id][msg]["content"]["text"]["text"]
				
				o[chats[chat_id]["title"]].append([msgType,content])
			# Reverse array of messages
			o[chats[chat_id]["title"]]=o[chats[chat_id]["title"]][::-1]
		return o
	else:
		return 1

def sendMessage(msg,to):
	td_send({
		"@type":"sendMessage",
		"chat_id":to,
		"input_message_content":{
			"@type":"inputMessageText",
			"text":{
				"@type":"formattedText",
				"text":msg
			}
		}
	})

def readMessages(msgs):
	if type(msgs)==list:
		tmpmsgs={}
		for msg in msgs:
			if not msg["chat_id"] in tmpmsgs:
				tmpmsgs[msg["chat_id"]]=[]
			tmpmsgs[msg["chat_id"]].append(msg["id"])
		msgs=tmpmsgs
	if type(msgs)==dict:
		for chat_id in msgs:
			tmpmsgs=[]
			for msg in msgs[chat_id]:
				tmpmsgs.append(msgs[chat_id][msg]["id"])
			td_send({
				"@type":"viewMessages",
				"chat_id":chat_id,
				"message_thread_id":0,
				"message_ids":tmpmsgs,
				"force_read":True
			})
	else:
		return 0

def call(to,is_video=False):
	protocol={
		"udp_p2p":True,
		"udp_reflector":False,
		"min_layer":65,
		"max_layer":65
	}
	td_send({
		"@type":"createCall",
		"user_id":to,
		"protocol":protocol,
		"is_video":is_video
	})

if isWorking:
	# load TDLib functions from shared library
	td_json_client_create = tdjson.td_json_client_create
	td_json_client_create.restype = c_void_p
	td_json_client_create.argtypes = []

	td_json_client_receive = tdjson.td_json_client_receive
	td_json_client_receive.restype = c_char_p
	td_json_client_receive.argtypes = [c_void_p, c_double]

	td_json_client_send = tdjson.td_json_client_send
	td_json_client_send.restype = None
	td_json_client_send.argtypes = [c_void_p, c_char_p]

	td_json_client_execute = tdjson.td_json_client_execute
	td_json_client_execute.restype = c_char_p
	td_json_client_execute.argtypes = [c_void_p, c_char_p]

	td_json_client_destroy = tdjson.td_json_client_destroy
	td_json_client_destroy.restype = None
	td_json_client_destroy.argtypes = [c_void_p]

	fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

	td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
	td_set_log_fatal_error_callback.restype = None
	td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]

	c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
	td_set_log_fatal_error_callback(c_on_fatal_error_callback)

	# setting TDLib log verbosity level to 1 (errors)
	td_execute({'@type': 'setLogVerbosityLevel', 'new_verbosity_level': 1, '@extra': 1.01234})

	# create client
	global client
	client = td_json_client_create()

	# another test for TDLib execute method
	td_execute({'@type': 'getTextEntities', 'text': '@telegram /test_command https://telegram.org telegram.me', '@extra': ['5', 7.0]})

	# testing TDLib send method
	td_send({'@type': 'getAuthorizationState', '@extra': 1.01234})

	if __name__=="__main__":
		start()
		while True:
			msg=raw_input("msg> ")
			if msg=="!!!!":
				break
			if msg!="":
				to=raw_input("to> ")
				if to!="":
					touser=searchContact(to)
					if touser[1]!="":
						print(touser[2])
						if msg=="call":
							call(touser[1])
						elif msg=="read":
							readMessages(unreadMessages)
						elif msg=="getm":
							print(getUnreadMessages())
						else:
							sendMessage(msg,touser[1])
					else:
						print("No user found.")
		# destroy client when it is closed and isn't needed anymore
		_stop()
