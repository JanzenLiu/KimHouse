import sys
sys.path.append('../')
from Common import *

def preprocess(df):
	# v1 preprocessor
	# 10 features used
	# Score of Linear Regression is: 0.521055
	# Score of Ridge is 0.521040
	# Score (Kaggle): 0.41746
	# map categorical building feature to numeric, and transform square meter features to their log1p
	hr = HouseReader()
	df['product_type'] = df['product_type'].map({'OwnerOccupier':0, 'Investment':1})
	df['full_sq'] = np.log1p(df['full_sq'])
	df['life_sq'] = np.log1p(df['life_sq'])
	df['kitch_sq'] = np.log1p(df['kitch_sq'])
	df['build_year'] = df['build_year'].map(lambda x: 2018 - x if x < 1000 else x if x < 3000 else 2005)
	df[hr.bld_feats] = df[hr.bld_feats].fillna(df[hr.bld_feats].median())
	return df