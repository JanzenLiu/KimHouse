import sys
sys.path.append('../')
from Common import *

# v18 preprocessor
# 66 features used
# Score of Linear Regression is: 0.467625
# Score of Ridge is 0.467963
# Score of XGBoost (Linear Regression) is: 0.428583

nbr_feats = hr.nbr_feats

def classify_feats():
	by_m = ['raion_build_count_with_material_info', 'build_count_block', 'build_count_wood', 
	 'build_count_frame', 'build_count_brick', 'build_count_monolith', 'build_count_panel',
	 'build_count_foam', 'build_count_slag', 'build_count_mix'] # stands for by material

	by_t = ['raion_build_count_with_builddate_info', 'build_count_before_1920', 'build_count_1921-1945',
	 'build_count_1946-1970', 'build_count_1971-1995', 'build_count_after_1995'] # stands for by time

	return by_m, by_t

def add_feats(df):
	df[nbr_feats] = df[nbr_feats].fillna(df[nbr_feats].median())
	df['log_build_with_material'] = np.log1p(df['raion_build_count_with_material_info'])
	df['log_build_brick'] = np.log1p(df['build_count_brick'])
	# df['log_build_monolith'] = np.log1p(df['build_count_monolith'])
	# df['log_build_with_builddate'] = np.log1p(df['raion_build_count_with_builddate_info'])
	df['new_build_brick'] = df['build_count_brick']
	df['new_build_monolith'] = df['build_count_monolith']
	df['log_old_build'] = np.log1p(df['build_count_before_1920'])
	df['log_new_build'] = np.log1p(df['build_count_after_1995'])
	return df

def trim_feats(df):
	return df.drop(nbr_feats, 1)

def preprocess(df):
	df = add_feats(df)
	df = trim_feats(df)
	return df

def plot_scatter_all():
	df = pd.DataFrame({'log_price': np.log(train['price_doc'])})
	for feat in nbr_feats:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Nbr/Scatter/%s.png' % feat)
		plt.show()

def plot_scatter_all_log():
	for feat in nbr_feats:
		df['log_feat'] = np.log1p(train[feat])
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Nbr/Scatter/log_%s.png' % feat)
		plt.show()

def print_corr_all():
	for feat in nbr_feats:
		df['feat'] = train[feat]
		corr = df[['feat', 'log_price']].corr()
		print("%s: %f" %(feat, corr['feat']['log_price']))

# raion_build_count_with_material_info: 0.041510
# build_count_block: 0.010761
# build_count_wood: -0.036811
# build_count_frame: -0.028549
# build_count_brick: 0.108256
# build_count_monolith: 0.100927
# build_count_panel: 0.005750
# build_count_foam: 0.000565
# build_count_slag: -0.020154
# build_count_mix: -0.028256
# raion_build_count_with_builddate_info: 0.041525
# build_count_before_1920: 0.055700
# build_count_1921-1945: 0.002348
# build_count_1946-1970: 0.029529
# build_count_1971-1995: 0.013574
# build_count_after_1995: 0.030708

def print_corr_all_log():
	for feat in nbr_feats:
		df['log_feat'] = np.log1p(train[feat])
		corr = df[['log_feat', 'log_price']].corr()
		print("log_%s: %f" %(feat, corr['log_feat']['log_price']))

# log_raion_build_count_with_material_info: 0.124472
# log_build_count_block: 0.074824
# log_build_count_wood: -0.004313
# log_build_count_frame: 0.007430
# log_build_count_brick: 0.111603
# log_build_count_monolith: 0.146496
# log_build_count_panel: 0.057707
# log_build_count_foam: -0.006890
# log_build_count_slag: 0.012801
# log_build_count_mix: -0.008158
# log_raion_build_count_with_builddate_info: 0.124713
# log_build_count_before_1920: 0.086425
# log_build_count_1921-1945: 0.052477
# log_build_count_1946-1970: 0.078467
# log_build_count_1971-1995: 0.087610
# log_build_count_after_1995: 0.110595