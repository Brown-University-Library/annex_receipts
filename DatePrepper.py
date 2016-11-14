"""
Part of LAS-to-Josiah code.
Obtain date in right format when needed.
"""


class DatePrepper:



	timeToFormat = ""



	def obtainDate(self):
		import time
		if( len(self.timeToFormat) == 0):
			theTime = time.localtime()
		else:
			theTime = self.timeToFormat
		formattedTime = time.strftime("%a %b %d %H:%M:%S %Z %Y", theTime)
		return formattedTime



	def prepareTimeStamp(self):
		import time
		if( len(self.timeToFormat) == 0):
			theTime = time.localtime()
		else:
			theTime = self.timeToFormat
		formattedTime = time.strftime("%Y-%m-%dT%H-%M-%S", theTime)
		return formattedTime




# bottom
