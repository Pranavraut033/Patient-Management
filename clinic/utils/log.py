from django.conf import settings

class Logger():
	logging = settings.DEBUG

	def disableLog(self):
		print("--- Log => Status: Disableing Logs")
		self.logging = False

	def enableLog(self):
		print("--- Log => Status: Enabling Logs")
		self.logging = True

	def toggleLogging(self):
		self.logging =  not self.logging
		print("--- Log => logging status " + "Enabled" if logging else "Disaled")

	'''
		Logging Parameters...
	'''
	def web(self, *msg, **kwargs):
		if self.logging: print("--- Log => WEB: ", *msg, **kwargs)

	def i(self, *msg, **kwargs):
		if self.logging: print("--- Log => I: ", *msg, **kwargs)

	def w(self, error=None, *msg, **kwargs):
		if self.logging: print("--- Log => W: ", error, *msg, **kwargs)

	def d(self, *msg, **kwargs):
		if self.logging: print("--- Log => D: ", *msg, **kwargs)

	def e(self, error, *msg, **kwargs):
		if self.logging: print("--- Log => E: ", *msg, error, **kwargs)
