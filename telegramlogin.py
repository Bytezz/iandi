#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,json,time
from ctypes.util import find_library
from ctypes import *

global listening;listening=False

# load shared library
tdjson_path = find_library('libtdjson') or 'tdjson.dll'
if tdjson_path is None:
	print("Can't find tdjson library.")
	exit()
try:
	tdjson=CDLL(tdjson_path)
except:
	try:
		tdjson=CDLL("/usr/local/lib/libtdjson.so")
	except:
		print("Can't find tdjson library.")
		exit()

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

# initialize TDLib log with desired parameters
def on_fatal_error_callback(error_message):
	print('TDLib fatal error: ', error_message)

def td_execute(query):
	query = json.dumps(query).encode('utf-8')
	result = td_json_client_execute(None, query)
	if result:
		result = json.loads(result.decode('utf-8'))
	return result

c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
td_set_log_fatal_error_callback(c_on_fatal_error_callback)

# setting TDLib log verbosity level to 1 (errors)
td_execute({'@type': 'setLogVerbosityLevel', 'new_verbosity_level': 1, '@extra': 1.01234})

# create client
global client
client = td_json_client_create()

# simple wrappers for client usage
def td_send(query):
	query = json.dumps(query).encode('utf-8')
	td_json_client_send(client, query)

def td_receive():
	result = td_json_client_receive(client, 1.0)
	if result:
		result = json.loads(result.decode('utf-8'))
	return result

# another test for TDLib execute method
td_execute({'@type': 'getTextEntities', 'text': '@telegram /test_command https://telegram.org telegram.me', '@extra': ['5', 7.0]})

# testing TDLib send method
td_send({'@type': 'getAuthorizationState', '@extra': 1.01234})

def eventsCatcher():
	global listening
	
	# main events cycle
	listening=True
	while listening:
		event = td_receive()
		if event:
			
			# process authorization states
			if event['@type'] == 'updateAuthorizationState':
				auth_state = event['authorization_state']

				# if client is closed, we need to destroy it and create new client
				if auth_state['@type'] == 'authorizationStateClosed':
					break

				# set TDLib parameters
				# you MUST obtain your own api_id and api_hash at https://my.telegram.org
				# and use them in the setTdlibParameters call
				if auth_state['@type'] == 'authorizationStateWaitTdlibParameters':
					td_send({
						"@extra":"internal",
						'@type': 'setTdlibParameters',
						'parameters': {
							'database_directory': os.path.dirname(os.path.abspath(__file__))+'/tdlib/tdlibDB',
							'use_message_database': True,
							'use_secret_chats': False,
							'api_id': 802978,
							'api_hash': '324516b19ffc5ae8e3b9adf3d374ab1a',
							'system_language_code': 'en',
							'device_model': 'Assistant',
							'system_version': 'Linux',
							'application_version': '0.1',
							'enable_storage_optimizer': True
						}
					})

				# set an encryption key for database to let know TDLib how to open the database
				if auth_state['@type'] == 'authorizationStateWaitEncryptionKey':
					td_send({"@extra":"internal",'@type': 'checkDatabaseEncryptionKey', 'key': 'my_key'})

				# enter phone number to log in
				if auth_state['@type'] == 'authorizationStateWaitPhoneNumber':
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
			elif event["@type"]=="chats":
				print("Logged in.")
				exit()

if __name__=="__main__":
	try:
		eventsCatcher()
	except:
		pass
	# destroy client when it is closed and isn't needed anymore
	listening=False
	td_json_client_destroy(client)

	print("\nNow go to \"https://my.telegram.org\".")
	print("Log in and go to \"API development tools\".")
	print("Insert an app title and a short name,")
	print("on \"Platform\" select a platform and then")
	print("click on \"Create application\".")
	api_id=raw_input("api_id> ")
	api_hash=raw_input("api_hash> ")

	with open(os.path.dirname(os.path.abspath(__file__))+"/tdlib/api.conf","w+") as apiConf:
		apiConf.write("{}\n{}".format(api_id,api_hash))
		apiConf.close()

	print("Done.")