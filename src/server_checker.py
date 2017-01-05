import requests
import semver
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
				return
		raise MyError("Your version {} is no longer supported. Download a newer version at http://link".format(config["version"]))


	else:
		raise Exception("Server is not responding")
