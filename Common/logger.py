try:
	from .header import *
except:
	from header import *

class Logger:
	def __init__(self, filename):
		self.filename = filename

	def log(self, msg, title=None):
		if(type(msg) != str):
			msg = format(msg)
		with open(self.filename, "a") as f:
			if(title):
				f.write("# " + title + "\n")
			f.write(msg + "\n\n")