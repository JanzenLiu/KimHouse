import sys
sys.path.append('../')
from Common import *

# TODO(Janzen): to make the figure size dependent of the feature (to achieve this,
#	we can design a class as plot helper)
#	other function possible for the plot helper: save file to the directory

hr = HouseReader()

caf_feats = train[hr.caf_feats].nunique().sort_values(ascending=True)

def preprocess(df):
	# v2 preprocessor (together with v1)
	# Score of Linear Regression is: 0.498153
	# Score of Ridge is 0.498137
	# Score (Kaggle): 0.39167
	# replace the 48 cafe counts features with the log of the shift of their most principal component

	# v6 preprocessor (together with v5)
	# Score of Linear Regression is: 0.492393
	# Score of Ridge is 0.492457
	# Score (Kaggle): 0.38162
	# transform catering_km to its natural log

	pca = PCA()
	caf_feats1 = caf_feats.index.copy()
	for feat in caf_feats.index:
		if not 'count' in feat:
			caf_feats1 = caf_feats1.drop(feat)
	pca.fit(combine[caf_feats1])
	pc1 = pca.transform(df[caf_feats1])[:,0]
	# log_pc1 = np.log1p(pc1 - pc1.min()) # -328.92996303028502
	log_pc1 = np.log1p(pc1 + 400)
	df['log_caf_pc1'] = log_pc1
	df['caf_intense1'] = df['cafe_count_500_price_high'].map(lambda x: 1 if x > 1 else 0)
	# df['caf_intense2'] = df['cafe_count_1000_price_high'].map(lambda x: 2 if x > 5 else 1 if x > 1 else 0)
	df['caf_intense2'] = df['cafe_count_1000_price_high'].map(lambda x: 1 if x > 1 else 0)
	df['log_catering_km'] = np.log(df['catering_km'])

	return df


def plot_kde():
	for feat in caf_feats.index:
		if not 'count' in feat:
			continue
		vals = np.sort(train[feat].dropna().unique())
		try:
			cols = cycle(sns.color_palette('YlOrRd', n_colors=len(vals)))
			for val in vals:
				sns.kdeplot(data = np.log(train[train[feat]==val]['price_doc']),
					color=next(cols), label=val)
			plt.title(feat)
			plt.legend(loc='upper left', borderpad=0.5, labelspacing=0.5, 
				# ncol=int((len(vals)-1)/20) +1, fontsize=8)
				ncol=int((len(vals)-1)/30) + 1, fontsize=6)
			plt.savefig('Figure/Caf/Kde/' + feat +'.png')
			# plt.show()
			plt.close()
		except Exception as e:
			print("Stop at %s (%d unique values): %s" %(feat, len(vals), e))
			break	

def plot_scatter():
	df = pd.DataFrame({'log_price': np.log(train['price_doc'])})
	for feat in caf_feats.index:
		if 'count' in feat:
			continue
		df['log_feat'] = np.log(train[feat])
		df.plot.scatter(x='log_feat', y='log_price', alpha=0.3)
		plt.title(feat)
		plt.savefig('Figure/Caf/Scatter/' + feat + '.png')
		# plt.show()
		plt.close()

def plot_boxplot():
	df = train[caf_feats.index]
	df['log_price'] = np.log(train['price_doc'])
	for feat in caf_feats.index:
		if not 'count' in feat:
			continue
		sns.boxplot(x=feat, y='log_price', data=df)
		size = df[feat].max() - df[feat].min()
		if(size > 100):
			plt.xticks(fontsize=6, rotation=90)
		elif(size > 30):
			plt.xticks(fontsize=8, rotation=30)
		plt.savefig('Figure/Caf/Boxplot/' + feat + '.png')
		# plt.show()
		plt.close()
