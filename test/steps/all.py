from behave import *
from unittest.mock import mock_open, patch

@given('a config file at "{filepath}"')
def step_impl(context, filepath):
	previousOpenMock = None
	
	if "openMock" in context:
		previousOpenMock = context.openMock

	def myOpen(filename, openOpt):
		assert(openOpt == "r")

		if (filename == filepath):
			fp = mock_open(read_data = context.text)
			fp.__iter__.return_value = content.splitlines(True) #TODO why do I need this?
			return fp
		elif previousOpenMock:
			return previousOpenMock(filename, openOpt)
		else:
			raise FileNotFoundError(filename)

	context.openMock = myOpen

@given('program arguments have config "{filepath}"')
def step_impl(context, filepath):
	if "cmdArgs" not in context:
		context.cmdArgs = []
	context.cmdArgs.append("-c")
	context.cmdArgs.append(filepath)

@when('it parses arguments')
def step_impl(context):
	with patch("__main__.open", context.openMock):
		context.parsedArgs = call_my_argument_parser()

@then('we will find "{pattern}" in includes')
def step_impl(context, pattern):
	assert(pattern in context.parsedArgs.includes)

@then('we will find "{pattern}" in excludes')
def step_impl(context, pattern):
	assert(pattern in context.parsedArgs.excludes)

@when('I start the program')
def step_impl(context):
	raise NotImplementedError('STEP: When I start the program')

@given('I entered no config file')
def step_impl(context):
	pass

@then('it should fail')
def step_impl(context):
	raise NotImplementedError('STEP: Then it should fail')

@then('it should prompt a link to download one')
def step_impl(context):
	raise NotImplementedError('STEP: Then it should prompt a link to download one')

@then('it should say configs must contain publishLink')
def step_impl(context):
	raise NotImplementedError('STEP: Then it should say configs must contain publishLink')

@given('a server exists')
def step_impl(context):
	raise NotImplementedError('STEP: Given a server exists')

@given('it will verify my version-check')
def step_impl(context):
	raise NotImplementedError('STEP: Given it will verify my version-check')

@when('it checks for version')
def step_impl(context):
	raise NotImplementedError('STEP: When it checks for version')

@then('it should successfully proceed')
def step_impl(context):
	raise NotImplementedError('STEP: Then it should successfully proceed')

@given('it verifies my version-check but a newer version exists')
def step_impl(context):
	raise NotImplementedError('STEP: Given it verifies my version-check but a newer version exists')

@then('it should notify me about the newer version')
def step_impl(context):
	raise NotImplementedError('STEP: Then it should notify me about the newer version')

@given('it doesn\'t support my version')
def step_impl(context):
	raise NotImplementedError('STEP: Given it doesn\'t support my version')

@then('it should fail and show a warning')
def step_impl(context):
	raise NotImplementedError('STEP: Then it should fail and show a warning')
