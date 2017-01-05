Feature: It takes multiple config files as arguments

Scenario: Multiple config files can be read
Given a config file at "config1.yaml"
	"""
	includes:
	- "*.js"
	- "*.css"
	publishLink: my-publish-link
	"""
And a config file at "config2.yaml"
	"""
	includes:
	- "*.py"
	excludes:
	- "secret.py"
	"""
And program arguments have config "config1.yaml"
And program arguments have config "config2.yaml"
When it parses arguments
Then config should have "*.js" in "includes" list
And config should have "*.css" in "includes" list
And config should have "*.py" in "includes" list
And config should have "secret.py" in "excludes" list
And config should have "my-publish-link" at "publishLink"

Scenario: User is prompted to download default config
Given I entered no arguments
When it parses arguments
Then it should fail
And it should prompt a link to download one

Scenario: A publishUrl must be read from configs
Given a config file at "config1.yaml"
	"""
	includes:
	- "*.py"
	"""
And program arguments have config "config1.yaml"
When it parses arguments
Then it should fail
And it should say configs must contain publishLink
