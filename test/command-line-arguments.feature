Feature: It takes multiple config files as arguments

Scenario: Multiple config files can be read
Given a config file at "config1.yaml"
	"""
	includes:
	- *.js
	- *.css
	publishKey: my-publish-key
	"""
And a config file at "config2.yaml"
	"""
	includes:
	- *.py
	"""
And program arguments have config "config1.yaml"
And program arguments have config "config2.yaml"
When it parses arguments
Then we will find "*.js" in includes
And we will find "*.css" in includes
And we will find "*.py" in includes
And we will find "*.pyc" in excludes

#Scenario: User is prompted to download default config
#Given I entered no config file
#When it parses arguments
#Then it should fail
#And it should prompt a link to download one
#
#Scenario: A publishUrl must be read from configs
#Given a config file at "config1.yaml"
#	"""
#	includes:
#	- *.py
#	"""
#And program arguments have config "config1.yaml"
#When it parses arguments
#Then it should fail
#And it should say configs must contain publishLink
