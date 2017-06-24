import sys
sys.path.append('../')
from Common import *

# v10 preprocessor
# 38 features used (153 features discarded, 28 features engineered)
# Score of Linear Regression is: 0.472860
# Score of Ridge is 0.473174
# Score (Kaggle): 0.36031
# keep market_count_500
# transform market_shop_km, shopping_centers_km and trc_sqm_5000 to their natural logarithm
# use the most principal component of those trc count features

bus_feats = hr.bus_feats

def classify_feats():
	km = []
	sqm = []
	count = []
	trc = []
	market = []
	for feat in bus_feats:
		if 'km' in feat:
			km.append(feat)
		elif 'sqm' in feat:
			sqm.append(feat)
		else:
			count.append(feat)
		if 'market' in feat:
			market.append(feat)
		else:
			trc.append(feat)
	return km, sqm, count, trc, market

km, sqm, count, trc, market = classify_feats()

def classify_count():
	count_market = []
	count_trc = []
	for feat in count:
		if 'trc' in feat:
			count_trc.append(feat)
		elif 'market' in feat and not 'big' in feat:
			count_market.append(feat)
	return count_market, count_trc

count_market, count_trc = classify_count()

def add_feats(df):
	pca = PCA()
	pca.fit(combine[count_trc])
	df['log_market_shop_km'] = np.log1p(df['market_shop_km'])
	df['log_shopping_centers_km'] = np.log1p(df['shopping_centers_km'])
	df['log_trc_sqm_5000'] = np.log1p(df['trc_sqm_5000'])
	df['new_market_count_500'] = df['market_count_500']
	df['trc_count_pc1'] = pca.transform(df[count_trc])[:,0]
	return df

def trim_feats(df):
	return df.drop(bus_feats, 1)

def plot_scatter_km():
	for feat in km:
		df = pd.DataFrame({'feat': train[feat], 'log_price':np.log(train['price_doc'])})
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Bus/Scatter/%s.png' % feat)
		plt.show()

def plot_scatter_km_log():
	for feat in km:
		df = pd.DataFrame({'log_feat': np.log1p(train[feat]), 'log_price':np.log(train['price_doc'])})
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Bus/Scatter/log_%s.png' % feat)
		plt.show()

def plot_corr_km():
	corr = train[km].corr()
	sns.heatmap(corr, square=True)
	plt.savefig('Figure/Bus/Corr/km_all.png')
	plt.show()

def plot_corr_km_no_big_market():
	corr = train[km].drop('big_market_km', 1).corr()
	sns.heatmap(corr, square=True)
	plt.savefig('Figure/Bus/Corr/km_no_big_market.png')
	plt.show()

def plot_scatter_sqm():
	for feat in sqm:
		df = pd.DataFrame({'feat': train[feat], 'log_price':np.log(train['price_doc'])})
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Bus/Scatter/%s.png' % feat)
		plt.show()

def plot_scatter_sqm_log():
	for feat in sqm:
		df = pd.DataFrame({'log_feat': np.log1p(train[feat]), 'log_price':np.log(train['price_doc'])})
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Bus/Scatter/log_%s.png' % feat)
		plt.show()

def plot_corr_sqm():
	corr = train[sqm].corr()
	sns.heatmap(corr, square=True)
	plt.savefig('Figure/Bus/Corr/sqm_all.png')
	plt.show()

# pca = PCA()
# pca.fit(train[sqm].drop(['trc_sqm_500'], 1))
# print(pca.explained_variance_ratio_)

def plot_kde_count():
	for feat in count:
		if feat == 'big_market_raion':
			continue
		sns.kdeplot(combine[feat])
		plt.title(feat)
		plt.savefig('Figure/Bus/Kde/%s.png' % feat)
		plt.show()

def plot_box_count():
	for feat in count:
		df[feat] = train[feat]
		sns.boxplot(feat, 'log_price', data=df)
		plt.savefig('Figure/Bus/Boxplot/%s.png' % feat)
		plt.show()

def plot_kde_binary():
	df1 = df[df['big_market_raion'] == 'no']
	df2 = df[df['big_market_raion'] == 'yes']
	sns.kdeplot(df1['log_price'], color='y', label='no')
	sns.kdeplot(df2['log_price'], color='r', label='yes')
	plt.savefig('Figure/Bus/Kde/yes_no_big_market_raion.png')
	plt.show()

def plot_corr_count():
	corr = combine[count].drop('big_market_raion', 1).corr()
	sns.heatmap(corr, square=True)
	plt.savefig('Figure/Bus/Corr/count_all.png')
	plt.show()

def plot_corr_count_market():
	corr = combine[count_market].corr()
	sns.heatmap(corr, square=True)
	plt.savefig('Figure/Bus/Corr/count_market.png')
	plt.show()

def plot_corr_count_trc():
	corr = combine[count_trc].corr()
	sns.heatmap(corr, square=True)
	plt.savefig('Figure/Bus/Corr/count_trc.png')
	plt.show()

# pca = PCA()
# pca.fit(combine[count_trc])
# print(pca.explained_variance_ratio_)
# df['trc_pc1'] = pca.transform(train[count_trc])[:,0]
# df['trc_pc2'] = pca.transform(train[count_trc])[:,1]

# pca = PCA()
# pca.fit(combine[count_market])
# print(pca.explained_variance_ratio_)
# df['market_pc1'] = pca.transform(train[count_market])[:,0]
# df['market_pc2'] = pca.transform(train[count_market])[:,1]

# df.plot.scatter('market_pc1','log_price',alpha=0.2); plt.show()