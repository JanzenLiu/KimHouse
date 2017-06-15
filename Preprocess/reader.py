from header import *

class Reader:
	def __init__(self, df):
		self.df = df
		self.shape = df.shape
		self.num_feats = []
		self.cat_feats = []
		for col in df.columns:
			if (df[col].dtype == object):
				self.cat_feats.append(col)
			else:
				self.num_feats.append(col)

cr = Reader(combine)