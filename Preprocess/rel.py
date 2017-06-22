import sys
sys.path.append('../')
from Common import *

# v9 preprocessor
# 33 features used (130 features discarded, 23 features engineered)
# Score of Linear Regression is: 0.472966
# Score of Ridge is 0.473329
# Score (Kaggle): 0.36032
# transform big_church_km, mosque_km and church_count_1000 to their natural logarithm (np.log1p)
# remain mosque_count_1000
# use the first and second principal components of the count features for church and big_church

rel_feats = hr.rel_feats

def classify_feats():
	mosque = []
	church = []
	big_church = []
	km = []
	count = []
	for feat in rel_feats:
		if 'km' in feat:
			km.append(feat)
		else:
			count.append(feat)
		if 'mosque' in feat:
			mosque.append(feat)
		elif 'big_church' in feat:
			big_church.append(feat)
		else:
			church.append(feat)
	return mosque, church, big_church, km, count

mosque, church, big_church, km, count = classify_feats()

def add_feats(df):
	pca = PCA()
	pca.fit(combine[church + big_church].drop(['big_church_km', 'church_synagogue_km'],1))
	tr = pca.transform(df[church + big_church].drop(['big_church_km', 'church_synagogue_km'], 1)) # stands for transformed
	df['log_mosque_km'] = np.log1p(df['mosque_km'])
	# df['log_church_km'] = np.log1p(df['church_synagogue_km'])
	df['log_big_church_km'] = np.log1p(df['big_church_km'])
	df['log_church_count_5000'] = np.log1p(df['church_count_5000'])
	df['mosque_nearby'] = df['mosque_count_1000']
	df['rel_count_pc1'] = tr[:,0]
	df['rel_count_pc2'] = tr[:,1]
	return df

def trim_feats(df):
	return df.drop(rel_feats, 1)

def savefig(relpath):
	plt.savefig('Figure/Rel/' + relpath)

def showvar(pca):
	print(pca.explained_variance_ratio_)

def create_dir(dirname):
	if not os.path.exists(dirname):
		os.makedirs(dirname)

def make_dirs():
	base = 'Figure/Rel'
	create_dir(base)
	for dirname in ['Kde', 'Scatter', 'Boxplot', 'Corr', 'Distplot']:
		create_dir(os.path.join(base, dirname))

# make_dirs()

def plot_kde_all():
	for feat in rel_feats:
		plt.close()
		sns.kdeplot(combine[feat].values)
		plt.title(feat)
		savefig('Kde/' + feat + '.png')
		plt.show()

def plot_dist_all():
	for feat in count:
		plt.close()
		sns.distplot(combine[feat], kde=False)
		plt.title("%s (%d unique values)" % (feat, combine[feat].dropna().nunique()))
		savefig('Distplot/' + feat + '.png')
		plt.show()

def plot_box_all():
	train['log_price'] = np.log(train['price_doc'])
	for feat in count:
		sns.boxplot(feat, 'log_price', data=train)
		plt.title(feat)
		savefig('Boxplot/' + feat + '.png')
		plt.show()

def plot_kde_mosque_count():
	for feat in mosque:
		if 'km' in feat:
			continue
		cols = cycle(sns.color_palette('YlOrRd', n_colors=3))
		for value in train[feat].dropna().unique():
			df = train[train[feat] == value]
			sns.kdeplot(df['log_price'], color=next(cols), label=value)
		plt.title(feat)
		savefig('Kde/log_price_' + feat + '.png')
		plt.show()

def plot_scatter_km():
	train['log_price'] = np.log(train['price_doc'])
	for feat in km:
		plt.close()
		train.plot.scatter(feat, 'log_price', alpha=0.2)
		savefig('Scatter/' + feat + '.png')
		plt.show()

def plot_scatter_km_log():
	for feat in km:
		plt.close()
		df = pd.DataFrame({'log_feat': np.log1p(train[feat]), 'log_price': np.log(train['price_doc'])})
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		savefig('Scatter/log_' + feat + '.png')
		pltshow()

def plot_scatter_count():
	train['log_price'] = np.log(train['price_doc'])
	for feat in count:
		if 'mosque' in feat:
			continue
		plt.close()
		train.plot.scatter(feat, 'log_price', alpha=0.2)
		savefig('Scatter/' + feat + '.png')
		plt.show()

def plot_scatter_count_log():
	df = pd.DataFrame()
	df['log_price'] = np.log(train['price_doc'])
	for feat in count:
		if 'mosque' in feat:
			continue
		plt.close()
		df['log_feat'] = np.log1p(train[feat])
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		savefig('Scatter/log_' + feat + '.png')
		plt.show()

# df = pd.DataFrame()
# df['log_price'] = np.log(train['price_doc'])
# df['log_feat'] = np.log1p(train['church_count_5000']).map(lambda x: x if x > 2.5 else (1.5 + x/2.5))
# df.plot.scatter('log_feat', 'log_price', alpha=0.2)
# plt.show()

# pca.fit(combine[church + big_church].drop(['big_church_km', 'church_synagogue_km'],1))
# showvar(pca)
# pca.fit(combine[church].drop('church_synagogue_km',1))
# showvar(pca)
# pca.fit(combine[big_church].drop('big_church_km',1))
# showvar(pca)
