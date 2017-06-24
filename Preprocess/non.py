import sys
sys.path.append('../')
from Common import *

# v17 preprocessor
# 60 features used
# Score of Linear Regression is: 0.467894
# Score of Ridge is 0.468368


non_feats = hr.non_feats

km, count = [], []
for feat in non_feats:
	if 'km' in feat:
		km.append(feat)
	else:
		count.append(feat)

def add_feats(df):
	df['log_detention_km'] = np.log1p(df['detention_facility_km'])
	df['log_healthcare_km'] = np.log1p(df['public_healthcare_km'])
	df['new_healthcare_count'] = df['healthcare_centers_raion']
	return df

def trim_feats(df):
	return df.drop(non_feats, 1)

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
		plt.savefig('Figure/Non/Scatter/%s.png' % feat)
		plt.show()

def plot_scatter_km_log():
	for feat in km:
		df['log_feat'] = np.log1p(train[feat])
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Non/Scatter/log_%s.png' % feat)
		plt.show()

def print_corr_km():
	for feat in km:
		df['feat'] = train[feat]
		corr = df[['feat', 'log_price']].corr()
		print("%s: %f" %(feat, corr['feat']['log_price']))

# cemetery_km: -0.031140
# hospice_morgue_km: -0.135249
# detention_facility_km: -0.205479
# public_healthcare_km: -0.181134

def print_corr_km_log():
	for feat in km:
		df['log_feat'] = np.log1p(train[feat])
		corr = df[['log_feat', 'log_price']].corr()
		print("log_%s: %f" %(feat, corr['log_feat']['log_price']))

# log_cemetery_km: -0.021323
# log_hospice_morgue_km: -0.139544
# log_detention_facility_km: -0.178356
# log_public_healthcare_km: -0.208271

def plot_box_count():
	for feat in count:
		df['feat'] = train[feat]
		sns.boxplot('feat', 'log_price', data=df)
		plt.title(feat)
		plt.savefig('Figure/Non/Boxplot/%s.png' % feat)
		plt.show()

def print_corr_count():
	for feat in count:
		df['feat'] = train[feat]
		if  df['feat'].dtype == object:
			df['feat'] = df['feat'].map(lambda x: 1 if x == 'yes' else 0)
		corr = df[['feat', 'log_price']].corr()
		print("%s: %f" %(feat, corr['feat']['log_price']))

# hospital_beds_raion: 0.098721
# healthcare_centers_raion: 0.152980
# detention_facility_raion: 0.033198
