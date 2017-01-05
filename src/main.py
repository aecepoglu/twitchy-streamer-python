#!/usr/bin/python3
import arg_parser, errors
import sys

try:
	config = arg_parser.parse(sys.argv[1:])
	# 2 - retrieve a list of unwanted files from the server
	# 3 - check the server for version compatibility
	# 4 - start watching for files
	# 4.1 - when a file changes send sync requests
	print(config)
except errors.MyError as err:
	print(err, file = sys.stderr)
	sys.exit(1)
