from distutils.core import setup

setup(
	name="twitchy_streamer",
	version="0.1.0",
	description="TwitchyStreamer Client",
	author="aecepoglu",
	author_email="aecepoglu@fastmail.fm",
	url="http://github.com/aecepoglu/twitchy-streamer-python",
	packages=["twitchy_streamer"],
	package_dir={
		"twitchy_streamer": "src"
	},
	entry_points = {
		"console_scripts": ["twitchy-streamer=twitchy_streamer.__main__:main"]
	},
	install_requires = [
		"pyyaml",
		"argparse",
		"semver",
		"requests",
		"watchdog"
	]
)
