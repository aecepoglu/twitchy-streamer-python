import argparse
import yaml
import collections
import sys
import os
from urllib.parse import urlsplit
from .errors import MyError
from .version import VERSION

def _update(d, u):
	if type(u) is not dict:
		return d

	for k, v in u.items():
		if isinstance(v, list) and k in d:
			d[k] = d[k] + v
		else:
			d[k] = u[k]
	return d

def parse(args):
	parser = argparse.ArgumentParser(description="TwitchyStreamer python client")

	parser.add_argument("path",
		nargs = 1,
		help = "File or folder to watch for changes"
	)

	parser.add_argument("-c",
		action="append",
		help="/path/to/config.yaml (this argument can be supplied multiple times)",
		dest="configs",
		metavar="FILE"
	)

	parsed = parser.parse_args(args)
	result = {
		#default values here
		"target": parsed.path[0],
		"includes": [],
		"excludes": []
	}

	if not parsed.configs:
		if not isinstance(parsed.configs, list):
			parsed.configs = []

	configInTarget = os.path.join(parsed.path[0], "twitchy-config.yml")
	if os.path.isdir(parsed.path[0]) and os.path.isfile(configInTarget):
		parsed.configs.append(configInTarget)

	if len(parsed.configs) == 0:
		parser.print_help()
		print("------")
		raise MyError("You haven't entered any config files.\nYou can find a sample config file at http://something-something.yaml")

	for path in parsed.configs:
		with open(path) as fp:
			try:
				_update(result, yaml.load(fp))
			except yaml.scanner.ScannerError as err:
				raise MyError("Yaml format error: {}".format(err))

	if "publishLink" not in result:
		raise MyError("publishLink couldn't be read")
	#else:
	#	for pair in urlsplit(result["publishLink"]).query.split("&"):
	#		l = pair.split("=")
	#		print(l)
	#		if l[0] == "key":
	#			result["publishKey"] = l[1];
	#			break

	result["version"] = VERSION

	return result
