class Logger():
	logging = True

	def disableLog(self):
		print("Disableing Logs")
		self.logging = False

	def enableLog(self, ):
		print("Enabling Logs")
		self.logging = True

	def toggleLogging(self):
		self.logging =  not self.logging
		print("log: " + str(logging))

	'''
		Logging Parameters...
	'''
	def web(self, *msg):
		if self.logging: print("---\nWEB: ", *msg)

	def i(self, *msg):
		if self.logging: print("---\nI: ", *msg)

	def w(self, error=None, *msg):
		if self.logging: print("---\nW: ", error, *msg)

	def d(self, *msg):
		if self.logging: print("---\nD: ", *msg)

	def e(self, error, *msg, ):
		if self.logging: print("---\nE: ", *msg, error)
