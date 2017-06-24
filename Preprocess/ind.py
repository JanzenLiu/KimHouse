import sys
sys.path.append('../')
from Common import *

# TODO(Janzen): to add two misclassified features back to cul.py

ind_feats = hr.ind_feats.copy()
# ind_feats.remove('culture_objects_top_25_raion')
# ind_feats.remove('culture_objects_top_25')

def trim_feats(df):
	# print(ind_feats)
	df['new_culture_top_25'] = df['culture_objects_top_25'].map(lambda x: 1 if 'yes' else 0)
	df['new_culture_top_25_raion'] = df['culture_objects_top_25_raion'].map(lambda x: x if x < 3 else 0)
	df = df.drop(ind_feats, 1)
	return df

def preprocess(df):
	df = trim_feats(df)
	return df
