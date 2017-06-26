import sys
sys.path.append('../')
from Common import *

trp_feats = hr.trp_feats

metro = [ 'metro_min_avto', 'metro_km_avto', 'metro_min_walk', 'metro_km_walk',]
railroad = ['railroad_station_walk_km', 'railroad_station_walk_min', 
'railroad_station_avto_km', 'railroad_station_avto_min', 'railroad_km']
loc = ['mkad_km', 'ttk_km', 'sadovoe_km', 'bulvar_ring_km', 'kremlin_km', 'zd_vokzaly_avto_km']
big_road = ['big_road1_km', 'big_road2_km']
pub = ['public_transport_station_km','public_transport_station_min_walk']
ID = ['ID_metro', 'ID_railroad_station_walk', 'ID_railroad_station_avto',
'ID_big_road1', 'ID_big_road2', 'ID_railroad_terminal', 'ID_bus_terminal', 'sub_area']
bus = 'bus_terminal_avto_km'
area = 'area_m'
binary = ['railroad_terminal_raion', 'big_road1_1line','railroad_1line']

def rank_ID(feat):
	index = train.groupby(feat)['price_doc'].mean().sort_values(ascending=False).index
	ranks = dict(zip(index, range(len(index))))
	return ranks

def map_ID_to_rank(df, feat):
	ranks = rank_ID(feat)
	return df[feat].map(ranks).fillna((len(ranks) - 1) / 2)

def print_corr_ID_rank():
	for feat in ID:
		ranks = rank_ID(feat)
		df['feat'] = train[feat].map(ranks)
		print("rank of %s: %f" % (feat, df[['feat','log_price']].corr().iloc[0,1]))

# rank of ID_metro: -0.376523
# rank of ID_railroad_station_walk: -0.326867
# rank of ID_railroad_station_avto: -0.342027
# rank of ID_big_road1: -0.267521
# rank of ID_big_road2: -0.288965
# rank of ID_railroad_terminal: -0.098865
# rank of ID_bus_terminal: -0.192747
# rank of sub_area: -0.366955

def fillna(df):
	df['ID_railroad_station_walk'] = df['ID_railroad_station_walk'].fillna(df['ID_railroad_station_avto'])
	return df

def add_feats(df):
	pca = PCA()
	pca.fit(combine[metro].dropna())
	df['metro_pc1'] = pca.transform(df[metro].fillna(df[metro].median()))[:,0]
	# df['metro_pc1'] = df['metro_pc1']
	df['metro_pc1'] = df['metro_pc1'].map(lambda x: 50 + np.log1p(x - 50)  if x > 50 else x)
	pca.fit(combine[railroad[:-1]].dropna())
	df['railroad_pc1'] = pca.transform(df[railroad[:-1]].fillna(df[railroad[:-1]].median()))[:,0]
	df['new_railroad_km'] = np.log1p(df['railroad_km'])
	# discard other location km features and do not use pca
	df['new_zd_vokzaly_avto_km'] = df['zd_vokzaly_avto_km'] # best to be alone among loc 
	df['new_big_road_km'] = df['big_road2_km']
	df['new_public_transport'] = df['public_transport_station_min_walk']
	df['new_mun_area'] = np.log1p(df['area_m'])
	df['new_big_road'] = df['big_road1_1line'].map(lambda x: 1 if x == 'yes' else 0)
	df['railroad_rank'] = df['ID_railroad_terminal'].map(lambda x: 1 if x == 113 else 0)
	df['metro_rank'] = map_ID_to_rank(df, 'ID_metro')
	# df['railroad_walk_rank'] = map_ID_to_rank(df, 'ID_railroad_station_walk')
	df['railroad_avto_rank'] = map_ID_to_rank(df, 'ID_railroad_station_avto')
	# df['bigroad1_rank'] = map_ID_to_rank(df, 'ID_big_road1')
	# df['bigroad2_rank'] = map_ID_to_rank(df, 'ID_big_road2')
	# df['bus_rank'] = map_ID_to_rank(df, 'ID_bus_terminal')
	df['area_rank'] = map_ID_to_rank(df, 'sub_area')
	return df

def trim_feats(df):
	return df.drop(trp_feats, 1)

def preprocess(df):
	df = fillna(df)
	df = add_feats(df)
	df = trim_feats(df)
	return df

def plot_corr_metro():
	corr = combine[metro].corr()
	sns.heatmap(corr, square=True)
	plt.xticks(rotation=30)
	plt.yticks(rotation=30)
	plt.savefig('Figure/Trp/metro/corr_all.png')
	plt.show()

def print_corr_metro():
	for feat in metro:
		df['feat'] = train[feat]
		print("%s: %f" % (feat, df[['feat','log_price']].corr().iloc[0,1]))

# metro_min_avto: -0.212059
# metro_km_avto: -0.195473
# metro_min_walk: -0.201722
# metro_km_walk: -0.201722

def plot_corr_railroad():
	corr = combine[railroad].corr()
	sns.heatmap(corr, square=True)
	plt.xticks(fontsize=7, rotation=15)
	plt.yticks(fontsize=7, rotation=15)
	plt.savefig('Figure/Trp/railroad/corr_all.png')
	plt.show()

def plot_corr_railroad_part():
	corr = combine[railroad].corr()
	sns.heatmap(corr.iloc[:-1,:-1], square=True)
	plt.xticks(fontsize=7, rotation=15)
	plt.yticks(fontsize=7, rotation=15)
	plt.savefig('Figure/Trp/railroad/corr_part.png')
	plt.show()

def print_corr_railroad():
	for feat in railroad:
		df['feat'] = train[feat]
		print("%s: %f" % (feat, df[['feat','log_price']].corr().iloc[0,1]))

# railroad_station_walk_km: -0.127578
# railroad_station_walk_min: -0.127578
# railroad_station_avto_km: -0.127898
# railroad_station_avto_min: -0.145649
# railroad_km: -0.093365

def plot_corr_loc():
	corr = combine[loc].corr()
	sns.heatmap(corr, square=True)
	plt.xticks(fontsize=7, rotation=15)
	plt.yticks(fontsize=7, rotation=15)
	plt.savefig('Figure/Trp/loc/corr_all.png')
	plt.show()

def plot_corr_loc_part():
	corr = combine[loc].corr()
	sns.heatmap(corr.iloc[1:,1:], square=True)
	plt.xticks(fontsize=7, rotation=15)
	plt.yticks(fontsize=7, rotation=15)
	plt.savefig('Figure/Trp/loc/corr_part.png')
	plt.show()

def print_corr_loc():
	for feat in loc:
		df['feat'] = train[feat]
		print("%s: %f" % (feat, df[['feat','log_price']].corr().iloc[0,1]))

# mkad_km: -0.068037
# ttk_km: -0.242854
# sadovoe_km: -0.246473
# bulvar_ring_km: -0.242107
# kremlin_km: -0.242356
# zd_vokzaly_avto_km: -0.248681

def plot_corr_big_road():
	corr = combine[big_road].corr()
	sns.heatmap(corr, square=True)
	plt.xticks(fontsize=7, rotation=15)
	plt.yticks(fontsize=7, rotation=15)
	plt.savefig('Figure/Trp/big_road/corr_all.png')
	plt.show()

def print_corr_big_road():
	for feat in big_road:
		df['feat'] = train[feat]
		print("%s: %f" % (feat, df[['feat','log_price']].corr().iloc[0,1]))

# big_road1_km: -0.084173
# big_road2_km: -0.142271

def print_corr_big_road_log():
	for feat in big_road:
		df['log_feat'] = np.log1p(train[feat])
		print("log_%s: %f" % (feat, df[['log_feat','log_price']].corr().iloc[0,1]))

# log_big_road1_km: -0.079646
# log_big_road2_km: -0.132347

def plot_corr_pub():
	corr = combine[pub].corr()
	sns.heatmap(corr, square=True)
	plt.xticks(fontsize=7, rotation=15)
	plt.yticks(fontsize=7, rotation=15)
	plt.savefig('Figure/Trp/pub/corr_all.png')
	plt.show()

def print_corr_pub():
	for feat in pub:
		df['feat'] = train[feat]
		print("%s: %f" % (feat, df[['feat','log_price']].corr().iloc[0,1]))

# public_transport_station_km: -0.145745
# public_transport_station_min_walk: -0.145745

def plot_scatter_metro():
	for feat in metro:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Trp/metro/scatter_%s.png' % feat)
		plt.show()

def plot_scatter_railroad():
	for feat in railroad:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Trp/railroad/scatter_%s.png' % feat)
		plt.show()

def plot_scatter_loc():
	for feat in loc:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Trp/loc/scatter_%s.png' % feat)
		plt.show()

def plot_scatter_big_road():
	for feat in big_road:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Trp/big_road/scatter_%s.png' % feat)
		plt.show()

def plot_scatter_pub():
	for feat in pub:
		df['feat'] = train[feat]
		df.plot.scatter('feat', 'log_price', alpha=0.2)
		plt.title(feat)
		plt.savefig('Figure/Trp/pub/scatter_%s.png' % feat)
		plt.show

def plot_scatter_bus():
	df['feat'] = train[bus]
	df.plot.scatter('feat', 'log_price', alpha=0.2)
	plt.title(bus)
	plt.savefig('Figure/Trp/bus/scatter.png')
	plt.show()

def plot_scatter_area():
	df['feat'] = train[area]
	df.plot.scatter('feat', 'log_price', alpha=0.2)
	plt.title(area)
	plt.savefig('Figure/Trp/area/scatter.png')
	plt.show()

def plot_scatter_area_log():
	df['log_feat'] = np.log1p(train[area])
	df.plot.scatter('log_feat', 'log_price', alpha=0.2)
	plt.title(area)
	plt.savefig('Figure/Trp/area/scatter_log.png')
	plt.show()

def plot_box_binary():
	for feat in binary:
		df[feat] = train[feat]
		sns.boxplot(feat, 'log_price', data=df)
		plt.savefig('Figure/Trp/binary/%s.png' % feat)
		plt.show()

def print_corr_area_log():
	df['feat'] = np.log1p(train[area])
	print("log_%s: %f" % (area, df[['feat','log_price']].corr().iloc[0,1]))

# log_area_m: -0.151145

def print_corr_area():
	df['feat'] = train[area]
	print("%s: %f" % (area, df[['feat','log_price']].corr().iloc[0,1]))

# area_m: -0.156493

def plot_box_ID_by_rank():
	for feat in ID:
		index = train.groupby(feat)['price_doc'].mean().sort_values(ascending=False).index
		df[feat] = train[feat]
		sns.boxplot(train[feat], df['log_price'], order=index)
		plt.xticks(rotation=30, fontsize=7)
		plt.savefig('Figure/Trp/ID/%s.png' % feat)
		# plt.show()
		plt.close()



