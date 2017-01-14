from behave import *
from unittest.mock import patch, mock_open, MagicMock
from src import arg_parser as myArgParser, server_utils as myServerUtils, errors as myErrors
import io
import requests
import requests_mock

def setup_debug_on_error(userdata):
	global BEHAVE_DEBUG_ON_ERROR
	BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")
def before_all(context):
	setup_debug_on_error(context.config.userdata)
def after_step(context, step):
	raise step.exc_traceback
	if step.status == "failed":
		import ipdb
		ipdb.post_mortem(step.exc_traceback)

def before_scenario(context):
	pass

@given('a file at "{filepath}"')
def step_impl(context, filepath):
	previousOpenMock = None
	previousIsfileMock = None
	content = context.text

	if "openMock" in context:
		previousOpenMock = context.openMock
	if "isfileMock" in context:
		previousIsfileMock = context.isfileMock

	def my_open(filename, openOpt="r"):
		assert(openOpt == "r")

		if (filename == filepath):
			return io.StringIO(content)
		elif previousOpenMock:
			return previousOpenMock(filename, openOpt)
		else:
			raise FileNotFoundError(filename)

	def my_isfile(x):
		if (x == filepath):
			return True
		elif previousIsfileMock:
			return previousIsfileMock(x)
		else:
			return False

	context.openMock = my_open
	context.isfileMock = my_isfile

@given('a directory at "{path}" exists')
def step_impl(context, path):
	previousMock = None

	if "isdirMock" in context:
		previousMock = context.isdirMock

	def my_isdir(x):
		if (x == path):
			return True
		elif previousMock:
			return previousMock(x)
		else:
			return False

	context.isdirMock = my_isdir

@given('program arguments are "{args}"')
def step_impl(context, args):
	context.cmdArgs = args.split()

@when('it parses arguments')
def step_impl(context):
	if "openMock" not in context:
		context.openMock = True
	if "isfileMock" not in context:
		context.isfileMock = MagicMock(return_value = False)
	if "isdirMock" not in context:
		context.isdirMock = MagicMock(return_value = False)

	with patch("builtins.open", context.openMock):
		with patch("os.path.isfile", context.isfileMock):
			with patch("os.path.isdir", context.isdirMock):
				try:
					context.parsedArgs = myArgParser.parse(context.cmdArgs)
					context.raisedException = False
				except myErrors.MyError as err:
					context.raisedException = err

@then('config has "{pattern}" in "{targetList}" list')
def step_impl(context, pattern, targetList):
	assert(targetList in context.parsedArgs)
	assert(isinstance(context.parsedArgs[targetList], list))
	assert(pattern in context.parsedArgs[targetList])

@then('config has "{value}" at "{target}"')
def step_impl(context, value, target):
	assert(target in context.parsedArgs)
	assert(context.parsedArgs[target] == value)

@then('config has "{target}"')
def step_impl(context, target):
	assert(target in context.parsedArgs)

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

@given(u'a server at "{host}" responds to "{method}" "{path}" with "{responseText}"')
def step_impl(context, host, method, path, responseText):
	_addr = host + path
	_responseText = responseText
	_method = method
	previousRegistrar = None

	if "registerRequestsMock" in context:
		previousRegistrar = context.registerRequestsMock

	def fun(mocker):
		mocker.register_uri(_method, _addr, text = _responseText)

		if previousRegistrar:
			previousRegistrar()

	context.registerRequestsMock = fun

@given(u'my config has "{value}" as "{key}"')
def step_impl(context, value, key):
	if "myConfig" not in context:
		context.myConfig = {}
	context.myConfig[key] = value

@when(u'it checks for version')
def step_impl(context):
	try:
		with requests_mock.Mocker() as m:
			context.registerRequestsMock(m)
			myServerUtils.check(context.myConfig)

		context.raisedException = False
	except myErrors.MyError as err:
		context.raisedException = err

@then(u'it should succeed')
def step_impl(context):
	assert(not context.raisedException)

@then(u'it should notify me about the newer version')
def step_impl(context):
	#TODO I need to verify this somehow
	pass

@then(u'give me version incompatibility error')
def step_impl(context):
	assert("no longer supported" in str(context.raisedException))
