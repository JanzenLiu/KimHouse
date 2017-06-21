import sys
sys.path.append('../')
from Common import *

# TODO(Janzen): write a CorrelationHelper class to help evaluate the relation between two columns
# 	(not only two columns themselves, but also transformation of them after some given rules)

hr = HouseReader()

pop_feats = train[hr.pop_feats].columns
ages = ['0_6', '7_14', '0_13', '0_17', 'young', '16_29', 'work', 'ekder', 'full']
genders = ['male', 'female', 'all']
type_1 = ['16_29', 'full']
type_2 = ['0_6', '7_14', '0_13', '0_17', 'young', 'work']
type_3 = ['ekder']
types = {1:type_1, 2:type_2, 3:type_3}

def preprocess(df):
	# v3 preprocessor (together with v1, v2)
	# Score of Linear Regression is: 0.495434
	# Score of Ridge is 0.495417
	# Score (Kaggle): 0.38278
	# replace 3 types of population features by their most important components respectively
	# and transform raion_popul to its natural log

	# v4 preprocessor (together with v1, v2)
	# Score of Linear Regression is: 0.495491
	# Score of Ridge is 0.495504
	# reserve the natural log of full_all, work_all, ekder_all and raion_popul

	# v5 preprocessor
	# Score of Linear Regression is: 0.494914
	# Score of Ridge is 0.494944
	# Score (Kaggle): 0.38256
	# a combination of v3, v4
	pca = PCA()
	for key, value in types.items():
		feat_names = get_type_feat_names(key)
		pca.fit(np.log(combine[feat_names]))
		df['pop_type' + str(key)] = pca.transform(np.log(df[feat_names]))[:,0]
	df['log_full_all'] = np.log(df['full_all'])
	df['log_work_all'] = np.log(df['work_all'])
	df['log_ekder_all'] = np.log(df['ekder_all'])
	df['log_raion_popul'] = np.log(df['raion_popul'])
	return df

# copy = train.copy()
# copy['log_price'] = np.log(copy['price_doc'])
# for key, value in types.items():
# 	feat_names = get_type_feat_names(key)
# 	# pca.fit(combine[feat_names].dropna())
# 	# print(key, pca.explained_variance_ratio_)
# 	pca.fit(np.log(combine[feat_names].dropna()))
# 	print('log' ,key, pca.explained_variance_ratio_)
# 	copy['pop_type' + str(key)] = pca.transform(np.log(train[feat_names].dropna()))[:,0]
# 	copy.plot.scatter(x=('pop_type' + str(key)), y='log_price', alpha=0.3)
# 	plt.show()

def get_type_feat_names(type_id):
	feat_names = []
	for age in types[type_id]:
		for gender in genders:
			feat_names.append(get_feat_name(age, gender))
	return feat_names


def get_feat_name(age, gender):
	if(age == 'full' and gender != 'all'):
		return gender + '_f'
	else:
		return age + '_' + gender

def plot_scatter_all():
	df = pd.DataFrame({'log_price': np.log(train['price_doc'])})
	for feat in pop_feats:
		df['log_feat'] = np.log(train[feat])
		df.plot.scatter(x='log_feat', y='log_price', alpha=0.3)
		plt.title(feat)
		# plt.savefig('Figure/Caf/Scatter/' + feat + '.png')
		plt.show()
		plt.close()

def plot_kde_all():
	cols = cycle(sns.color_palette('YlOrRd', n_colors=len(pop_feats)))
	for feat in pop_feats:
		sns.kdeplot(data=np.log(combine[feat]), color=next(cols), label=feat)
	plt.legend(loc='upper left', borderpad=0.3, labelspacing=0.3, 
					ncol=2, fontsize=8)
	plt.savefig('Figure/Pop/Kde/all.png')
	# plt.show()
	plt.close()

def plot_kde_by_age():
	for age in ages:
		cols = cycle(sns.color_palette('YlOrRd', n_colors=3))
		for gender in genders:
			sns.kdeplot(data=np.log(combine[get_feat_name(age, gender)]), color=next(cols), label=gender)
		plt.title(age)
		plt.savefig('Figure/Pop/Kde/age_' + age + '.png')
		# plt.show()
		plt.close()

def plot_kde_by_gender():
	for gender in genders:
		cols = cycle(sns.color_palette('YlOrRd', n_colors=8))
		for age in ages:
			sns.kdeplot(data=np.log(combine[get_feat_name(age, gender)]), color=next(cols), label=age)
		# plt.title(gender)
		plt.savefig('Figure/Pop/Kde/gender_' + gender + '.png')
		# plt.show()
		plt.close()

def plot_kde_by_type(type_id):
	type_name = {1:type_1, 2:type_2, 3:type_3}[type_id]
	cols = cycle(sns.color_palette('YlOrRd', n_colors=len(type_name)))
	for age in type_name:
		sns.kdeplot(data=np.log(combine[get_feat_name(age, 'all')]), color=next(cols), label=age)
	plt.savefig('Figure/Pop/Kde/type_' + str(type_id) + '.png')
	# plt.show()
	plt.close()

