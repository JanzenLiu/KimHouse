from header import *

# TODO(JanzenLiu): add function of selecting columns with certain nunique() number
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

	def feats_with_nunique(self, lower, upper=None, numfeats=True):
		if(numfeats):
			cols = self.num_feats
		else:
			cols = self.df.columns
		if(not upper):
			return self.df[cols].loc[:,(self.df[cols].nunique() == lower)].columns
		else:
			return self.df[cols].loc[:,((self.df[cols].nunique() >= lower) * (self.df[cols].nunique() < upper))].columns