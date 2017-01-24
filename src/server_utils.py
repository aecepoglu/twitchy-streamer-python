import requests
import semver
import os
from urllib.parse import urlsplit
from .errors import MyError

def check(config):
	checkUrl = urlsplit(config["publishLink"])._replace(
		path = "/api/version",
		query = None
	).geturl()

	resp = requests.get(checkUrl)

	myVersionInfo = semver.parse_version_info(config["version"])

	if resp.status_code == requests.codes.ok:
		supportedVersions = resp.text.split(" ")

		for it in supportedVersions:
			versionInfo = semver.parse_version_info(it)
			if myVersionInfo.major == versionInfo.major:
				if semver.compare(config["version"], it) < 0:
					print("A newer version of the software ({}) is available. Download it at http://link".format(it)) #TODO link
				print("version OK")
				return
		raise MyError("Your version {} is no longer supported. Download a newer version at http://link".format(config["version"]))
	else:
		raise Exception("Server is not responding")


def mergeIgnores(config):
	#TODO
	return config

class Uploader:
	def __init__(self, config, irc=None):
		self.publishLink = config["publishLink"]
		self.rootPath = config["target"]
		self.irc = irc
		pass

	def send(self, filepath, eventType, source=None):
		print(eventType, filepath)
		r = None
		params = {
			"method": eventType,
			"destination": os.path.relpath(filepath, self.rootPath)
		}

		if eventType == "deleted":
			r = requests.post(self.publishLink, params = params)
		elif eventType == "moved":
			params.update({
				"source": os.path.relpath(source, self.rootPath)
			})

			r = requests.post(self.publishLink, params = params)
		else:
			with open(filepath, "rb") as fp:
				r = requests.post(self.publishLink, files = {
					"file": fp
				}, params = params)

			if r.status_code >= 400:
				print(r.text)
			elif self.irc is not None:
				print(r.text)
				self.irc.mymessage("updated " + r.text)
