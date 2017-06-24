import sys
sys.path.append('../')
from Common import *

spt_feats = hr.spt_feats

def classify_feats():
	km = []
	count = []
	for feat in spt_feats:
		if 'km' in feat:
			km.append(feat)
		else:
			count.append(feat)
	return km, count

km, count = classify_feats()

def add_feats(df):
	df['sport_raion'] = df['sport_objects_raion']
	df['sport_count'] = df['sport_count_5000']
	# df['log_swim_pool_km'] = np.log1p(df['swim_pool_km'])
	df['log_fitness_km'] = np.log1p(df['fitness_km'])
	# df['new_stadium_km'] = df['stadium_km']
	# df['new_basketball_km'] = df['basketball_km']
	return df

def trim_feats(df):
	df = df.drop(spt_feats, 1)
	return df

def preprocess(df):
	df = add_feats(df)
	df = trim_feats(df)
	return df

def plot_scatter_km():
	df = pd.DataFrame({'log_price': np.log(train['price_doc'])})
	for feat in km:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Spt/Scatter/%s.png' % feat)
		plt.show()

def plot_scatter_km_log():
	for feat in km:
		df['log_feat'] = np.log1p(train[feat])
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Spt/Scatter/log_%s.png' % feat)
		plt.show()

def print_corr_log_price_km():
	for feat in km:
		df['feat'] = train[feat]
		corr = df[['feat', 'log_price']].corr()
		print("%s: %f" %(feat, corr['feat']['log_price']))

# fitness_km: -0.187427
# swim_pool_km: -0.209718
# ice_rink_km: -0.155672
# stadium_km: -0.217404
# basketball_km: -0.219494

def print_corr_log_price_log_km():
	for feat in km:
		df['log_feat'] = np.log1p(train[feat])
		corr = df[['log_feat', 'log_price']].corr()
		print("log_%s: %f" %(feat, corr['log_feat']['log_price']))

# log_fitness_km: -0.214209
# log_swim_pool_km: -0.227957
# log_ice_rink_km: -0.118823
# log_stadium_km: -0.214621
# log_basketball_km: -0.211306

def plot_box_count():
	for feat in count:
		df['feat'] = train[feat]
		sns.boxplot('feat', 'log_price', data=df)
		plt.title(feat)
		plt.savefig('Figure/Spt/Boxplot/%s.png' % feat)
		plt.show()

def print_corr_log_price_count():
	for feat in count:
		df['feat'] = train[feat]
		corr = df[['feat', 'log_price']].corr()
		print("%s: %f" %(feat, corr['feat']['log_price']))

# sport_objects_raion: 0.196311
# sport_count_500: 0.072449
# sport_count_1000: 0.153613
# sport_count_1500: 0.198327
# sport_count_2000: 0.213126
# sport_count_3000: 0.219429
# sport_count_5000: 0.223386

