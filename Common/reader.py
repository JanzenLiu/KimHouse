try:
	from .header import *
except:
	from header import *

# TODO: add exception handler and error log for function of Reader

class Reader:
	def __init__(self, df, logfile):
		self.df = df
		self.logfile = logfile
		self.num_feats = []
		self.cat_feats = []
		for col in df.columns:
			if (df[col].dtype == object):
				self.cat_feats.append(col)
			else:
				self.num_feats.append(col)

	def feats_with_nunique(self, lower, upper=None, feattype=None):
		if(not feattype):
			cols = self.df.columns
		elif(feattype == "num"):
			cols = self.num_feats
		elif(feattype == "cat"):
			cols = self.cat_feats
		else:
			return # invalid parameter
		if(not upper):
			return self.df[cols].loc[:,(self.df[cols].nunique() == lower)].columns
		else:
			return self.df[cols].loc[:,((self.df[cols].nunique() >= lower) * (self.df[cols].nunique() < upper))].columns

	def log(self, msg, title=None):
		if(type(msg) != str):
			msg = format(msg)
		with open(self.logfile, "a") as f:
			if(title):
				f.write("# " + title + "\n")
			f.write(msg + "\n\n")