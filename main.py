#!/usr/bin/python3
from src import arg_parser, errors, server_utils, file_watcher
import sys

try:
	config = arg_parser.parse(sys.argv[1:])
	config = server_utils.mergeIgnores(config)
	server_utils.check(config)
	file_watcher.watch(config, server_utils.Uploader)

except errors.MyError as err:
	print(err, file = sys.stderr)
	sys.exit(1)
