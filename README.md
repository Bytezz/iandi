# Iandi assistant

Iandi it's a simple, open source, privacy oriented
assistant based on [sobot](https://github.com/bytezz/sobot).

This isn't an official Telegram client.

## Table of contents

- [Features](#features)
- [Todo](#todo)
- [Install/Uninstall](#installuninstall)
- [Execution types](#exectypes)
- [Translations](#translations)
- [Plugins](#plugins)
- [External sources](#externalsrc)
- [License](#license)

<a name="features"></a>
## Features

- What time is it?
- What day is it?
- Repeat
- Calculate
- Set language
- Set country
- Set city
- Set custom/shortcut commands
- Phone
- - Read messages
- - Send message
- Get near places (work in progess...)
- - Restaurants
- - Cafes
- - Markets
- - Banks
- Do i need umbrella today?
- How is the weather?
- Notes manager
- - Add a note
- - Delete a note
- - Read notes
- Reminder manager
- - Add a reminder
- - Delete a reminder
- - Read reminders
- System utility
- - Run program
- - Set system volume
- - Turn up the system volume
- - Turn down the system volume
- Dice
- - Random number
- - Flip a coin
- - Roll a die
- Timer
- - Set a timer
- - Verify timer
- Answer (ask a question to search on web)
- Music player
- - Play (search on YouTube)
- - Stop
- - Pause
- - Resume
- - Set volume
- - Turn up the volume
- - Turn down the volume
- - Mute
- - Unmute
- Read the news

<a name="todo"></a>
## Todo

- GUI
- Tray icon
- Phone
- - Improve contact search
- - Call
- Dictate
- Lists
- Alarms clock
- Translate command
- Search on web command
- RSS reader
- Road directions
- Play music even offline
- Change stt (maybe deepspeech)
- Change tts
- Configuration page in ad-hoc wifi
- Fix plugins problems when Iandi's main use internals.py
- Make the code python3 compatible
- Finish near places
- Stock market

<a name="installuninstall"></a>
## Install/Uninstall

### Dependencies

#### System

- portaudio (portaudio19-dev)
- libespeak-dev
- youtube-dl ([installation instruction](https://github.com/ytdl-org/youtube-dl/#installation))
- TDLib ([build instruction](https://github.com/tdlib/td#building))
- Snowboy ([Kitt-AI](https://github.com/kitt-ai/snowboy), [Seasalt-ai](https://github.com/seasalt-ai/snowboy))

#### Python

- pyaudio
- playsound
- pyttsx3
- speechrecognition
- pocketsphinx
- pyalsaaudio
- python-vlc

### Install

`sudo ./install`

To log into Telegram:  
`python telegramlogin.py`

#### Step by step installation

- "Install dependencies?" will ask you to insert a package manager (apt, dnf, etc.) and it will install all dependecies automatically (along with pip).
- "Install snowboy?" will install the wake word detector. If you want use vocal command, then type Y then choose a precompiled snowboy. If in the list there isn't your system, then you have to compile it by yourself.
- "Compile procname?" will enable Iandi to manifest it self as "Iandi" in task managers and system monitors.
- "Get Terminal Virtual Face?" will get the python code to generate a talking face in the terminal. Type Y if you are unsure.
- "Install tdlib?" will enable Iandi to use telegram to get and send messages across it.
- "Install brain MIME type?" will enable the system to see the *.brain files as a brain for sobot like bots.
- "Install Iandi on system?" will enable the user to execute Iandi by typing "iandi" into the terminal or by executing the launcher (.desktop)
- "Autostart Iandi on login?" (only if installed on system) will autostart Iandi on user login.

### Uninstall

Uninstall instructions.

<a name="exectypes"></a>
## Execution types

At the moment there are only 3 execution types:

- Lite
- NoUi
- Normal

To select execution type, pass it as argument:  
`./iandi lite`
`./iandi noui`

Passing no argument means normal execution type will be set.

<a name="translations"></a>
## Translations

### How it works

There are 2 files which have to be translated:

- brain (in brains/)
- json (in langs/)

To better understand brain syntax,
read [sobot](https://github.com/bytezz/sobot)'s readme.  
To better understand json in langs/ just use eng.json as example.

For lang code use the 3 digits version. A list of all
codes are available in `ISO-639-2_utf-8.txt`.

### Available translations

#### Brain

- English
- Italian

#### Json

- English
- Italian

<a name="plugins"></a>
## Plugins

### Add a plugin

To add a plugin, just add a folder in "plugins/" and
in it put "\__init__.py" with functions you want add
or replace.

### How plugins works

To access global vars (like brain), `import globalvars` and then call `globalvars.varName`.  
Example: `globalvars.brain`

When creating internal plugin's functiones and vars, choose names not used by internal Iandi's functiones/vars or by other plugins, to avoid problems.

To disable a plugin, just put a "-" in front of folder name.

### Plugin example

- gtts: use Google tts for output.
- lol: add command "lol" to brain.

<a name="externalsrc"></a>
## External sources

- Acoustic Models for offline use by [CMU Sphinx](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/)
- Countries list by [mledoze/countries](https://github.com/mledoze/countries)
- Cities list by [lutangar/cities.json](https://github.com/lutangar/cities.json)
- Terminal UI Face by [Bytezz/VirtualFace](https://github.com/Bytezz/VirtualFace)
- Weather by [weatherstack](https://weatherstack.com)
- Translations by [Apertium](https://apertium.org)
- Online answers by [Answers](https://www.answers.com)
- Music by [YouTube](https://youtube.com) using [youtube-dl](https://youtube-dl.org/)
- News by [NewsAPI](https://newsapi.org)
- Places by [Overpass API](http://overpass-api.de)
- Brain icon in MIME type icon by [Arjun Adamson](https://thenounproject.com/arjunadamson/)

<a name="license"></a>
## License

[GPLv3](LICENSE)

---

Iandi 0.1
Readme update of 2021/09/05