import sys
sys.path.append('../')
from Common import *

# v14 preprocessor
# 53 features used
# Score of Linear Regression is: 0.468905
# Score of Ridge is 0.469270
# Score (Kaggle): 0.34739
# keep the natural logarithm of three of the km features
# keep incineration_raion after mapping to 1/0

# TODO(Janzen): to add two misclassified features back to cul.py

ind_feats = hr.ind_feats.copy()
# ind_feats.remove('culture_objects_top_25_raion')
# ind_feats.remove('culture_objects_top_25')

def classify_feats():
	km = []
	part = []
	count = []
	for feat in ind_feats:
		if 'culture' in feat:
			continue
		if 'km' in feat:
			km.append(feat)
		elif 'part' in feat:
			part.append(feat)
		else:
			count.append(feat)
	return km, part, count

km, part, count = classify_feats()

def add_feats(df):
	# print(ind_feats)
	# df['log_nuclear_reactor_km'] = np.log1p(df['nuclear_reactor_km'])
	df['log_radiation_km'] = np.log1p(df['radiation_km'])
	df['log_power_transmission_line_km'] = np.log1p(df['power_transmission_line_km'])
	# df['log_thermal_power_plant_km'] = np.log1p(df['thermal_power_plant_km'])
	# df['log_ts_km'] = np.log1p(df['ts_km'])
	df['log_workplaces_km'] = np.log1p(df['workplaces_km'])
	df['incineration'] = df['incineration_raion'].map(lambda x: 1 if 'yes' else 0)
	df['new_culture_top_25'] = df['culture_objects_top_25'].map(lambda x: 1 if 'yes' else 0)
	df['new_culture_top_25_raion'] = df['culture_objects_top_25_raion'].map(lambda x: x if x < 3 else 0)
	return df

def trim_feats(df):
	# print(ind_feats)
	df = df.drop(ind_feats, 1)
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
		plt.savefig('Figure/Ind/Scatter/%s.png' % feat)
		plt.show()

def plot_scatter_km_log():
	for feat in km:
		df['log_feat'] = np.log1p(train[feat])
		df.plot.scatter('log_feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Ind/Scatter/log_%s.png' % feat)
		plt.show()

def print_corr_log_price_log_km():
	for feat in km:
		df['log_feat'] = np.log1p(train[feat])
		corr = df[['log_feat', 'log_price']].corr()
		print("log_%s: %f" %(feat, corr['log_feat']['log_price']))

# log_industrial_km: 0.033206
# log_incineration_km: -0.022491
# log_oil_chemistry_km: -0.069030
# log_nuclear_reactor_km: -0.211255
# log_radiation_km: -0.192786
# log_power_transmission_line_km: -0.153532
# log_thermal_power_plant_km: -0.192011
# log_ts_km: -0.174551
# log_workplaces_km: -0.209001

def plot_corr_km():
	corr = np.log1p(combine[km]).corr()
	sns.heatmap(corr, square=True)
	plt.xticks(fontsize=7, rotation=30)
	plt.yticks(fontsize=7, rotation=30)
	plt.savefig('Figure/Ind/Corr/km_all.png')
	plt.show()

def plot_corr_km_part():
	sns.heatmap(corr.iloc[3:, 3:], square=True)
	plt.xticks(fontsize=8, rotation=30)
	plt.yticks(fontsize=8, rotation=30)
	plt.savefig('Figure/Ind/Corr/km_part.png')
	plt.show()

def print_scatter_part():
	for feat in part:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Ind/Scatter/%s.png' % feat)
		plt.show()

def print_corr_log_price_part():
	for feat in part:
		df['feat'] = train[feat]
		corr = df[['feat', 'log_price']].corr()
		print("%s: %f" %(feat, corr['feat']['log_price']))

# indust_part: -0.067228
# prom_part_500: 0.003689
# prom_part_1000: -0.039707
# prom_part_1500: -0.041266
# prom_part_2000: -0.024995
# prom_part_3000: 0.034568
# prom_part_5000: 0.086629

def plot_box_count():
	for feat in count:
		df['feat'] = train[feat]
		sns.boxplot('feat', 'log_price', data=df)
		plt.title(feat)
		plt.savefig('Figure/Ind/Boxplot/%s.png' % feat)
		plt.show()

def plot_kde_yes_no_count():
	for feat in count:
		df1 = np.log(train[train[feat] == 'yes']['price_doc'])
		df2 = np.log(train[train[feat] == 'no']['price_doc'])
		sns.kdeplot(df1, color='r', label='yes')
		sns.kdeplot(df2, color='y', label='no')
		plt.title(feat)
		plt.savefig('Figure/Ind/Kde/%s.png' % feat)
		plt.show()