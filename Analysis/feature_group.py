import sys
sys.path.append('../')
from Common import *

class FeatureGroup:
	def __init__(self, df, figdir=None, logpath=None):
		self.df = df
		self.corr = df.corr()
		if(figdir):
			self.set_figdir(figdir)
		if(logfile):
			self.set_log(logpath)
			
	def set_figdir(self, figdir):
		assert figdir
		if(not os.path.exists(figdir)):
			os.makedirs(figdir)
		self.figdir = figdir

	def set_log(self, logpath):
		assert logpath
		logdir = os.path.dirname(logpath)
		logname = os.path.basename(logpath)
		if(not os.path.exists(logdir)):
			os.makedirs(logdir)
		self.logdir = logdir
		self.logname = logname

	def set_featname_processor(self, dicts, delimiter, jointer):
		assert type(dicts) == dict
		assert type(delimiter) == str
		assert type(jointer) == str
		def process_featname(self):
			cols = []
			for col in list(self.df.columns):
				for key, value in dicts.items():
					if(key in col):
						col = col.replace(key, value)
				col = jointer.join(col.split(delimiter))
				cols.append(col)
			return cols
		self.process_featname = process_featname
