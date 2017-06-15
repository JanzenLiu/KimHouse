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

print(format("%d Categorical Features:\n" % len(cr.cat_feats)), cr.cat_feats, "\n") # 16
print(format("%d Numerical Features:\n" % len(cr.num_feats)), cr.num_feats, "\n") # 275

for col in cr.cat_feats:
	print(cr.df[col].nunique())
