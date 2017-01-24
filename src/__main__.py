#!/usr/bin/env python3
from . import arg_parser, errors, server_utils, file_watcher, irc
import sys
import time
import threading

def main():
	try:
		config = arg_parser.parse(sys.argv[1:])
		config = server_utils.mergeIgnores(config)
		server_utils.check(config)
		ircClient = irc.connect(config)
		uploader = server_utils.Uploader(config, irc=ircClient)

		t1 = threading.Thread(target=irc.watch, args=[ircClient])
		t2 = threading.Thread(target=file_watcher.watch, args=[config, uploader])

		t1.start()
		t2.start()

		t1.join()
		t2.join()
	
	except errors.MyError as err:
		print(err, file = sys.stderr)
		sys.exit(1)
	except KeyboardInterrupt:
		print("terminating...")
		file_watcher.stop()
		irc.stop(ircClient)

		while not(irc.isStopped() and file_watcher.isStopped()):
			time.sleep(1)
	finally:
		print("bye...")
