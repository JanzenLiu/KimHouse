import sys
sys.path.append('../')
from Common import *

# v16 preprocessor
# 57 features used
# Score of Linear Regression is: 0.468416
# Score of Ridge is 0.468781

env_feats = hr.env_feats

def classify_feats():
	km = []
	part = []
	cat = [] # stands for categorical features
	for feat in env_feats:
		if 'km' in feat:
			km.append(feat)
		elif 'part' in feat:
			part.append(feat)
		else:
			cat.append(feat)
	return km, part, cat

km, part, cat = classify_feats()

def add_feats(df):
	df['new_green_part'] = df['green_part_3000']
	return df

def trim_feats(df):
	return df.drop(env_feats, 1)

def preprocess(df):
	df = add_feats(df)
	df = trim_feats(df)
	return df

def plot_box_cat():
	for feat in cat:
		df['feat'] = train[feat]
		sns.boxplot('feat', 'log_price', data=df)
		plt.title(feat)
		plt.savefig('Figure/Env/Boxplot/%s.png' % feat)
		plt.show()

def plot_scatter_km():
	for feat in km:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Env/Scatter/%s.png' % feat)
		plt.show()

def print_corr_km():
	for feat in km:
		df['feat'] = train[feat]
		corr = df[['feat', 'log_price']].corr()
		print("%s: %f" %(feat, corr['feat']['log_price']))

# green_zone_km: -0.053454
# water_treatment_km: 0.029750
# water_km: -0.024868

def plot_scatter_part():
	for feat in part:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Env/Scatter/%s.png' % feat)
		plt.show()

def print_corr_part():
	for feat in part:
		df['feat'] = train[feat]
		corr = df[['feat', 'log_price']].corr()
		print("%s: %f" %(feat, corr['feat']['log_price']))

# green_zone_part: -0.076166
# green_part_500: -0.043761
# green_part_1000: -0.045874
# green_part_1500: -0.069197
# green_part_2000: -0.096377
# green_part_3000: -0.121648
# green_part_5000: -0.145224
