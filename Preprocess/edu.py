import sys
sys.path.append('../')
from Common import *

# v13 preprocessor
# 47 features used
# Score of Linear Regression is: 0.470858
# Score of Ridge is 0.471230
# Score (Kaggle): 0.35922 -> 0.34925 (after using the whole data set to train)
# map many_top_20_school, many_top_20_university to binary using 1 and 2 as discrimating thresholds
# transform university_km and school_km to their natural logarithm

edu_feats = hr.edu_feats

def classify_feats():
	quota = []
	children = []
	km = []
	count = []
	for feat in edu_feats:
		if 'quota' in feat:
			quota.append(feat)
		elif 'children' in feat:
			children.append(feat)
		elif 'km' in feat:
			km.append(feat)
		else:
			count.append(feat)
	return quota, children, km, count

quota, children, km, count = classify_feats()

def add_feats(df):
	df['many_top_20_school'] = df['school_education_centers_top_20_raion'].map(lambda x: 1 if x > 1 else 0)
	df['many_top_20_university'] = df['university_top_20_raion'].map(lambda x: 1 if x > 2 else 0)
	df['log_university_km'] = np.log1p(df['university_km'])
	df['log_school_km'] = np.log1p(df['school_km'])
	return df

def trim_feats(df):
	return df.drop(edu_feats, 1)

def preprocess(df):
	df = add_feats(df)
	df = trim_feats(df)
	return df

def plot_scatter_quota():
	df = pd.DataFrame({'log_price': np.log(train['price_doc'])})
	for feat in quota:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Edu/Scatter/%s.png' % feat)
		plt.show()

def plot_scatter_quota_log():
	for feat in quota:
		df['log_feat'] = np.log1p(train[feat])
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Edu/Scatter/log_%s.png' % feat)
		plt.show()

def plot_scatter_children():
	for feat in children:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Edu/Scatter/%s.png' % feat)
		plt.show()

def plot_scatter_children_log():
	for feat in children:
		df['log_feat'] = np.log1p(train[feat])
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Edu/Scatter/log_%s.png' % feat)
		plt.show()

def plot_scatter_saturity():
	df['preschool_sat'] = train['children_preschool'] / (train['preschool_quota'] + 1)
	df['school_sat'] = train['children_school'] / (train['school_quota'] + 1)
	df.plot.scatter('preschool_sat', 'log_price', alpha=0.2)
	plt.savefig('Figure/Edu/Scatter/sat_preschool.png')
	plt.show()
	df.plot.scatter('school_sat', 'log_price', alpha=0.2)
	plt.savefig('Figure/Edu/Scatter/sat_school.png')
	plt.show()

def plot_scatter_saturity_log():
	df['log_preschool_sat'] = np.log1p(df['preschool_sat'])
	df['log_school_sat'] = np.log1p(df['school_sat'])
	df.plot.scatter('log_preschool_sat', 'log_price', alpha=0.2)
	plt.savefig('Figure/Edu/Scatter/log_sat_preschool.png')
	plt.show()
	df.plot.scatter('log_school_sat', 'log_price', alpha=0.2)
	plt.savefig('Figure/Edu/Scatter/log_sat_school.png')
	plt.show()

def plot_scatter_km():
	for feat in km:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Edu/Scatter/%s.png' % feat)
		plt.show()

def plot_scatter_km_log():
	for feat in km:
		df['log_feat'] = np.log1p(train[feat])
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Edu/Scatter/log_%s.png' % feat)
		plt.show()

def plot_scatter_count():
	for feat in count:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Edu/Scatter/%s.png' % feat)
		plt.show()

def plot_box_count():
	for feat in count:
		df[feat] = train[feat]
		sns.boxplot(feat, 'log_price', data=df)
		plt.title(feat)
		plt.savefig('Figure/Edu/Boxplot/%s.png' % feat)
		plt.show()

def plot_corr_all():
	corr = combine[edu_feats].corr()
	sns.heatmap(corr, square=True)
	plt.savefig('Figure/Edu/Corr/all.png')
	plt.show()

def plot_corr_preschool_school():
	sns.heatmap(corr.iloc[:6,:6], square=True)
	plt.xticks(fontsize=7, rotation=30)
	plt.yticks(fontsize=7, rotation=30)
	plt.savefig('Figure/Edu/Corr/preschool_school.png')
	plt.show()

def plot_corr_km():
	sns.heatmap(corr.iloc[-5:,-5:], square=True)
	plt.xticks(fontsize=7, rotation=30)
	plt.yticks(fontsize=7, rotation=30)
	plt.savefig('Figure/Edu/Corr/km.png')
	plt.show()

def plot_corr_pca_preschool_school():
	preschool = corr.columns[:3]
	school = corr.columns[3:6]
	pca = PCA()
	pca.fit(combine[preschool].dropna())
	print(pca.explained_variance_ratio_)
	df['preschool_pc1'] = pca.transform(train[preschool].fillna(combine[preschool].median()))[:,0]
	df['log_preschool_pc1'] = np.log(7000 + df['preschool_pc1'])
	df.plot.scatter('preschool_pc1', 'log_price', alpha=0.2);plt.show()
	df.plot.scatter('log_preschool_pc1', 'log_price', alpha=0.2);plt.show()
	pca.fit(combine[school].dropna())
	print(pca.explained_variance_ratio_)
	df['school_pc1'] = pca.transform(train[school].fillna(combine[school].median()))[:,0]
	df.plot.scatter('school_pc1', 'log_price', alpha=0.2);plt.show()

def plot_kde_school_top_20():
	df0 = train[train['school_education_centers_top_20_raion'] <= 1 ]
	df1 = train[train['school_education_centers_top_20_raion'] > 1]
	# df2 = train[train['school_education_centers_top_20_raion'] == 2]
	sns.kdeplot(np.log(df0['price_doc']), color='b', label='Less Equal to 1')
	sns.kdeplot(np.log(df1['price_doc']), color='r', label='Greater than 1')
	# sns.kdeplot(np.log(df2['price_doc']), color='r', label=2)
	plt.title('school_education_centers_top_20_raion')
	plt.savefig('Figure/Edu/Kde/school_top_20.png')
	plt.show()

def plot_kde_university_top_20():
	cols = cycle(sns.color_palette('YlOrRd', n_colors=4))
	for value in combine['university_top_20_raion'].dropna().unique():
		df3 = train[train['university_top_20_raion'] == value]
		sns.kdeplot(np.log(df3['price_doc']), color=next(cols), label=value)
	plt.show()

def plot_kde_university_top_20_split_at_2():
	df4 = train[train['university_top_20_raion'] <= 2]
	df5 = train[train['university_top_20_raion'] > 2]
	sns.kdeplot(np.log(df4['price_doc']), color='b', label='Less Equal to 2')
	sns.kdeplot(np.log(df5['price_doc']), color='r', label='Greater than 2')
	plt.savefig('Figure/Edu/Kde/university_top_20.png')
	plt.show()