import pydle

stopped = False

class MyClient(pydle.featurize(
		pydle.features.RFC1459Support,
		pydle.features.IRCv3Support,
		pydle.features.ircv3.CapabilityNegotiationSupport
		)):
	def on_connect(self):
		super().on_connect()
		self.join("#" + self.nickname)

	def on_join(self, channel, user):
		super().on_join(channel, user)
		self.message(channel, "Heya {user}, welcome!".format(user=user))

	def mymessage(self, message):
		super().message("#" + self.nickname, message)

	def on_raw_004(self, message):
		self._registration_completed(message)

	def whois(self, nickname):
		pass

def connect(config):
	conf = config["irc"]
	client = MyClient(conf["nickname"], realname="TwitchyStreamer")
	client.connect("irc.chat.twitch.tv", 6667, password=conf["password"])
	return client

def watch(client):
	client.handle_forever()
	global stopped
	stopped = True

def stop(client):
	if client.connected:
		client._disconnect(expected=True)

def isStopped():
	global stopped
	return stopped
