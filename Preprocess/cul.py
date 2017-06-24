import sys
sys.path.append('../')
from Common import *

# v11 preprocessor
# 42 features used (163 features discarded, 52 features engineered)
# Score of Linear Regression is: 0.472363
# Score of Ridge is 0.472698
# Score (Kaggle): 0.35941
# transform exhibition_km, park_km, theater_km to their natural logarithm
# keep leisure_count_500

# v12 preprocessor
# 43 features used
# Score of Linear Regression is: 0.471918
# Score of Ridge is 0.472309
# use the natural log of the most principle components of the leisure count features

cul_feats = hr.cul_feats

def classify_feats():
	km = []
	count = []
	for feat in cul_feats:
		if 'km' in feat:
			km.append(feat)
		else:
			count.append(feat)
	return km, count

km, count = classify_feats()

def add_feats(df):
	pca = PCA()
	pca.fit(combine[count].drop('leisure_count_500', 1))
	offset = 10
	df['log_exhibition_km'] = np.log1p(df['exhibition_km'])
	df['log_park_km'] = np.log1p(df['park_km'])
	df['log_theater_km'] = np.log1p(df['theater_km'])
	df['new_leisure_count_500'] = df['leisure_count_500']
	df['leisure_pc1'] = np.log(offset + pca.transform(df[count].drop('leisure_count_500', 1))[:,0])
	return df

def trim_feats(df):
	return df.drop(cul_feats, 1)

def preprocess(df):
	df = add_feats(df)
	df = trim_feats(df)
	return df

def plot_scatter_km():
	df = pd.DataFrame({'log_price':np.log(train['price_doc'])})
	for feat in km:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Cul/Scatter/%s.png' % feat)
		plt.show()

def plot_scatter_km_log():
	for feat in km:
		df['log_feat'] = np.log1p(train[feat])
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Cul/Scatter/log_%s.png' % feat)
		plt.show()

def plot_corr_km():
	corr = combine[km].corr()
	sns.heatmap(corr, square=True)
	plt.savefig('Figure/Cul/Corr/km_all.png')
	plt.show()

def plot_kde_count():
	for feat in count:
		sns.kdeplot(combine[feat])
		plt.savefig('Figure/Cul/Kde/%s.png' % feat)
		plt.show()

def plot_box_count():
	for feat in count:
		df['feat'] = train[feat]
		sns.boxplot('feat', 'log_price', data=df)
		plt.title(feat)
		plt.savefig('Figure/Cul/Boxplot/%s.png' % feat)
		plt.show()

def plot_corr_count():
	corr = combine[count].corr()
	sns.heatmap(corr, square=True)
	plt.savefig('Figure/Cul/Corr/count.png')
	plt.show()

def plot_corr_count_no_500():
	corr = combine[count].drop('leisure_count_500', 1).corr()
	sns.heatmap(corr, square=True)
	plt.savefig('Figure/Cul/Corr/count_no_500.png')
	plt.show()

