#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import deepspeech, numpy as np, sys, os, pyaudio, time
from playsound import playsound

pv=sys.version_info[0]

if pv<3:
	raise Exception("Too old python")

def play(filep):
	try:
		playsound(filep)
	except:
		os.system("paplay {}".format(repr(filep)))

def stt(lang,verbose=False):
	
	start=time.time()
	
	model=deepspeech.Model("deepspeechModels/"+lang+"/"+lang+".pbmm")
	model.enableExternalScorer("deepspeechModels/"+lang+"/"+lang+".scorer")

	modelRate = model.sampleRate()

	audio = pyaudio.PyAudio()

	global stream

	global ds_stream
	global text_so_far
	global isSilence
	global silenceStart
	global silenceDtoStop

	ds_stream=model.createStream()
	text_so_far=""
	isSilence=False
	silenceDtoStop=1.5

	def process_audio(in_data, frame_count, time_info, status):
		global text_so_far
		global ds_stream
		global isSilence
		global silenceStart
		global silenceDtoStop
		global stream
	
		data16=np.frombuffer(in_data,dtype=np.int16)
		ds_stream.feedAudioContent(data16)
		text=ds_stream.intermediateDecode()
		if text!=text_so_far:
			isSilence=False
			text_so_far=text
		else:
			if not isSilence:
				isSilence=True
				silenceStart=time.time()
			else:
				silenceD=time.time()-silenceStart
				if silenceD>=silenceDtoStop and text_so_far!="":
					stream.close()
		
		return (in_data, pyaudio.paContinue)

	stream = audio.open(
		format = pyaudio.paInt16,
		channels = 1,
		rate = modelRate,
		input = True,
		frames_per_buffer = 1024,
		stream_callback=process_audio
	)
	
	if verbose:
		print("Ready in {}s".format(time.time()-start))

	play("beep.ogg")
	
	stream.start_stream()

	try:
		while stream.is_active():
			time.sleep(.1)
	except KeyboardInterrupt:
		pass
	except:
		pass
	stream.stop_stream()
	stream.close()
	audio.terminate()
	text=ds_stream.finishStream()
	return(text)

if __name__=="__main__":
	if len(sys.argv)>1:
		lang=sys.argv[1]
	else:
		lang="eng"
	verbose=False
	if len(sys.argv)>2:
		if sys.argv[2]=="verbose":
			verbose=True
	text=stt(lang,verbose)
	print("----\n"+text)