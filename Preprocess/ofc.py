import sys
sys.path.append('../')
from Common import *

# v8 preprocessor (together with v7)
# 27  features used
# Score of Linear Regression is: 0.484154
# Score of Ridge is 0.484424
# Score (Kaggle): 0.37148
# use the log of the shift of most principal components for the sqm and counts features respectively
#	(sqm_500 and count_500 unused)
# map lower than 12 office_raion to 12
# transform office_count_5000 to its natural logarithm
# transform office_sqm_5000 to the natural log of itself after some mapping

def classify_feats():
	km = []
	sqm = []
	count = []
	for feat in ofc_feats:
		if 'km' in feat:
			km.append(feat)
		elif 'sqm' in feat:
			sqm.append(feat)
		else:
			count.append(feat)
	return km, sqm, count

ofc_feats = hr.ofc_feats
km, sqm, count = classify_feats()
pca = PCA()

def add_feats(df):
	offset1 = 100
	offset2 = 2000000
	df['new_ofc_raion'] = df['office_raion'].map(lambda x: x if x < 12 else 12)
	df['log_ofc_count_5000'] = np.log1p(df['office_count_5000'])
	df['log_ofc_sqm_5000'] = np.log(df['office_sqm_5000'].map(lambda x: 22000 if x < 22000 else x))
	pca.fit(combine[count].drop(['office_count_500', 'office_raion'], 1))
	df['log_ofc_count_pc1'] = np.log(pca.transform(df[count].drop(['office_count_500', 'office_raion'], 1))[:,0] + offset1)
	pca.fit(combine[sqm].drop('office_sqm_500', 1))
	df['log_ofc_sqm_pc1'] = np.log(pca.transform(df[sqm].drop('office_sqm_500', 1))[:,0] + offset2)
	return df

def trim_feats(df):
	return df.drop(ofc_feats, 1)

def savefig(relpath):
	plt.savefig('Figure/Ofc/' + relpath)

def showvar(pca):
	print(pca.explained_variance_ratio_)

def plot_kde_all():
	for feat in ofc_feats:
		plt.close()
		sns.kdeplot(combine[feat].values)
		plt.title(feat)
		savefig('Kde/' + feat + '.png')
		plt.show()

def plot_kde_log_sqm():
	for feat in sqm:
		plt.close()
		sns.kdeplot(np.log(combine[feat].values))
		plt.title(feat)
		savefig('Kde/log_' + feat + '.png')
		plt.show()

def plot_scatter_km():
	for feat in km:
		plt.close()
		df = pd.DataFrame({('log_feat'):np.log1p(train[feat]), 'log_price':np.log(train['price_doc'])})
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		savefig('Scatter/' + feat + '.png')
		plt.show()

def plot_kde_km_threshold(threshold):
	df1 = train[np.log1p(train['office_km']) >= threshold]
	df2 = train[np.log1p(train['office_km']) < threshold]
	plt.close()
	sns.kdeplot(np.log(df1['price_doc']), color='b', label='office-intensive')
	sns.kdeplot(np.log(df2['price_doc']), color='r', label='office-sparse')
	plt.title('threshold = ' + str(threshold))
	savefig('Kde/km_threshold_' + threshold + '.png')
	plt.show()

def plot_scatter_sqm():
	for feat in sqm:
		plt.close()
		df = pd.DataFrame({('log_feat'):np.log1p(train[feat]), 'log_price':np.log(train['price_doc'])})
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		savefig('Scatter/' + feat + '.png')
		plt.show()

def plot_scatter_count():
	for feat in count:
		plt.close()
		df = pd.DataFrame({('feat'):train[feat], 'log_price':np.log(train['price_doc'])})
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		savefig('Scatter/' + feat + '.png')
		plt.show()

def plot_scatter_count_log():
	for feat in count:
		plt.close()
		df = pd.DataFrame({('log_feat'):np.log(train[feat]), 'log_price':np.log(train['price_doc'])})
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		savefig('Scatter/log_' + feat + '.png')
		plt.show()

def plot_box_count():
	for feat in count:
		plt.close()
		df = pd.DataFrame({('feat'):train[feat], 'log_price':np.log(train['price_doc'])})
		sns.boxplot(x='feat', y='log_price', data=df)
		plt.title(feat)
		savefig('Scatter/Boxplot/' + feat + '.png')
		plt.show()

def plot_corr_sqm(ignore_500=False):
	plt.close()
	plt.figure(figsize=(10,8))
	corr = combine[sqm].corr()
	figname = 'sqm'
	if(ignore_500):
		corr = combine[sqm].corr().drop('office_sqm_500').drop('office_sqm_500',1)
		figname += '_ignore500'
	sns.heatmap(corr, square=True)
	plt.xticks(fontsize=8, rotation=30)
	plt.yticks(fontsize=8, rotation=30)
	savefig('Corr/' + figname + '.png')
	plt.show()

def plot_corr_count(ignore_500=False):
	plt.close()
	plt.figure(figsize=(10,8))
	corr = combine[count].corr()
	figname = 'count'
	if(ignore_500):
		corr = combine[count].corr().drop('office_count_500').drop('office_count_500',1)
		figname += '_ignore500'
	sns.heatmap(corr, square=True)
	plt.xticks(fontsize=8, rotation=30)
	plt.yticks(fontsize=8, rotation=30)
	savefig('Corr/' + figname + '.png')
	plt.show()

# pca = PCA()
# pca.fit(combine[sqm])
# showvar(pca)
# pca.fit(combine[sqm].drop('office_count_500', 1))
# showvar(pca)
# pca.fit(combine[count])
# showvar(pca)
# pca.fit(combine[count].drop(['office_count_500', 'office_raion'], 1))
# showvar(pca)
