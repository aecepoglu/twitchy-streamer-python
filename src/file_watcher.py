from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import PatternMatchingEventHandler
import time

events = {}

class MyHandler(PatternMatchingEventHandler):
	def __init__(self, config, uploader):
		super().__init__(
			patterns = config["includes"],
			ignore_patterns = config["excludes"],
			ignore_directories = True
		)
		self.uploader = uploader

	def on_moved(self, ev):
		self.uploader.send(ev.dest_path, "moved", source = ev.src_path)

	def on_any_event(self, ev):
		if ev.event_type == "moved":
			return

		if ev.src_path in events:
			old = events[ev.src_path]
			if old["type"] != ev.event_type:
				old["type"] = "modified"
				old["ticks"] = 0
		else:
			events[ev.src_path] = {
				"type": ev.event_type,
				"ticks": 0
			}
				

def watch(config, Uploader):
	uploader = Uploader(config)

	myHandler = MyHandler(config, uploader)
	observer = Observer()
	observer.schedule(myHandler, config["target"],
		recursive = True
	)

	observer.start()

	try:
		while True:
			for key, value in events.copy().items():
				if value["ticks"] >= 1:
					uploader.send(key, value["type"])
					del events[key]
				else:
					value["ticks"] = value["ticks"] + 1
			time.sleep(5)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()
