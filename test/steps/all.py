from behave import *
from unittest.mock import patch, mock_open, MagicMock
from src import arg_parser as myArgParser
import io

def setup_debug_on_error(userdata):
	global BEHAVE_DEBUG_ON_ERROR
	BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")
def before_all(context):
	setup_debug_on_error(context.config.userdata)
def after_step(context, step):
	if step.status == "failed":
		import ipdb
		ipdb.post_mortem(step.exc_traceback)

@given('a config file at "{filepath}"')
def step_impl(context, filepath):
	previousOpenMock = None
	content = context.text

	if "openMock" in context:
		previousOpenMock = context.openMock

	def myOpen(filename, openOpt="r"):
		assert(openOpt == "r")

		if (filename == filepath):
			return io.StringIO(content)
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
	#with patch("builtins.open", mock_open(read_data="publishLink: ahmet")):
	if "openMock" not in context:
		context.openMock = None

	with patch("builtins.open", context.openMock):
		try:
			context.parsedArgs = myArgParser.parse(context.cmdArgs)
			context.raisedException = False
		except myArgParser.MyError as err:
			context.raisedException = err

@then('config should have "{pattern}" in "{targetList}" list')
def step_impl(context, pattern, targetList):
	assert(targetList in context.parsedArgs)
	assert(isinstance(context.parsedArgs[targetList], list))
	assert(pattern in context.parsedArgs[targetList])

@then('config should have "{value}" at "{target}"')
def step_impl(context, value, target):
	assert(target in context.parsedArgs)
	assert(context.parsedArgs[target] == value)

@when('I start the program')
def step_impl(context):
	raise NotImplementedError('STEP: When I start the program')

@given('I entered no arguments')
def step_impl(context):
	context.cmdArgs = []
	pass

@then('it should fail')
def step_impl(context):
	assert(context.raisedException)

@then('it should prompt a link to download one')
def step_impl(context):
	assert("can find a sample config file at" in str(context.raisedException))

@then('it should say configs must contain publishLink')
def step_impl(context):
	assert("publishLink" in str(context.raisedException))
	#TODO may be improve this a bit

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
