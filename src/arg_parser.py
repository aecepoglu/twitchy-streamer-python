import argparse
import yaml
import collections
import sys

class MyError(Exception):
	pass

def _update(d, u):
	for k, v in u.items():
		if isinstance(v, list) and k in d:
			d[k] = d[k] + v
		else:
			d[k] = u[k]
	return d

def parse(args):
	parser = argparse.ArgumentParser(description="TwitchyStreamer python client")

	parser.add_argument("--config", "-c", action="append", help="/path/to/config.yaml (this argument can be supplied multiple times)", dest="configs")

	parsed = parser.parse_args(args)
	result = {
		#default values here
	}

	if not parsed.configs or len(parsed.configs) < 1:
		raise MyError("You haven't entered any config files.\nYou can find a sample config file at http://something-something.yaml")

	for path in parsed.configs:
		with open(path) as fp:
			try:
				_update(result, yaml.load(fp))
			except yaml.scanner.ScannerError as err:
				raise MyError("Yaml format error: {}".format(err))

	if "publishLink" not in result:
		raise MyError("publishLink couldn't be read")

	return result
