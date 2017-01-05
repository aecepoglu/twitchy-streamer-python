Feature: It takes multiple config files and a target as arguments

Scenario: Multiple config files can be read
Given a file at "config1.yml"
	"""
	includes:
	- "*.js"
	- "*.css"
	publishLink: my-publish-link
	"""
And a file at "config2.yml"
	"""
	includes:
	- "*.py"
	excludes:
	- "secret.py"
	"""
And a directory at "watched-dir" exists
And a file at "watched-dir/twitchy-config.yml"
	"""
	excludes:
	- "twitchy-config.yml"
	"""
And program arguments are "-c config1.yml -c config2.yml watched-dir"
When it parses arguments
Then config has "*.js" in "includes" list
And config has "*.css" in "includes" list
And config has "*.py" in "includes" list
And config has "secret.py" in "excludes" list
And config has "twitchy-config.yml" in "excludes" list
And config has "my-publish-link" at "publishLink"
And config has "watched-dir" at "target"

Scenario: User is prompted to download default config
Given program arguments are "watched-dir"
And a directory at "watched-dir" exists
When it parses arguments
Then it should fail
And it should prompt a link to download one

Scenario: A publishUrl must be read from configs
Given a file at "config1.yml"
	"""
	includes:
	- "*.py"
	"""
And a directory at "watched-dir" exists
And program arguments are "-c config1.yml watched-dir"
When it parses arguments
Then it should fail
And it should say configs must contain publishLink
