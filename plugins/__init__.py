#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
path=os.path.dirname(os.path.abspath(__file__))
#plugins=[i for i in os.listdir(path) if not i.startswith("__init__.py")]      # files and dirs
plugins=[i for i in os.listdir(path) if os.path.isdir(os.path.join(path,i))]   # only dirs
#plugins=[i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i))] # only files
for plugin in plugins:
	if plugin.endswith(".py"):
		plugin=plugin[:-3]
	if plugin.endswith(".pyc"):
		plugin=plugin[:-4]
	if not plugin.startswith(".") and not plugin.startswith("-"):
		exec("from plugins.{} import *".format(plugin))