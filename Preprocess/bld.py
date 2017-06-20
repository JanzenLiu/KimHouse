import sys
sys.path.append('../')
from Common import *

def preprocess(df):
	# v1 preprocessor
	# Score of Linear Regression is: 0.521055
	# Score of Ridge is 0.521040
	hr = HouseReader()
	df['product_type'] = df['product_type'].map({'OwnerOccupier':0, 'Investment':1})
	df['full_sq'] = np.log1p(df['full_sq'])
	df['life_sq'] = np.log1p(df['life_sq'])
	df['kitch_sq'] = np.log1p(df['kitch_sq'])
	df[hr.bld_feats] = df[hr.bld_feats].fillna(df[hr.bld_feats].median())
	return df