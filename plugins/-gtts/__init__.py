#!/usr/bin/env python
# -*- coding: utf-8 -*-
import globalvars,internals,iso639
from gtts import gTTS as gtts
from playsound import playsound
def voice(txt):
	maxwordsforonline=60
	onlinetts=True
	if globalvars.onlineconnection and len(txt.split(" "))<=maxwordsforonline and onlinetts:
		o=gtts(text=txt,lang=globalvars.voicelang)
		o.save("/tmp/voice.mp3")
		globalvars.voicebusy=True
		playsound("/tmp/voice.mp3")
		globalvars.voicebusy=False
	else:
		internals.voice(txt)