import sys
sys.path.append('../')
from Common import *
from feature_group import FeatureGroup
 
# TODO(Janzen): further reduce dimension for population features
# TODO(Janzen): write a feature group handler class, for each instance, 
#	there's an unique directory for saving figures, and processing feature names
# TODO(Janzen): fix the drop columns code: use another reference to keep combine unchanged
# TODO(Janzen): develop an algorithm to find the best group of feature groups in between which
#	the correlation is highest or relatively very high or satisify some specified criterion

def plot_corr(df, labels=None, save=None):
    ax = sns.heatmap(df.corr(), square=True)
    if(labels):
		ax.set_xticklabels(labels)
		ax.set_yticklabels(labels)
		plt.xticks(rotation=30)
		plt.yticks(rotation=30)
    if(save):
        plt.savefig(save)
    plt.show()

def process_ofc_feat_name(df):
	cols = []
	for col in list(df.columns):
		col = col.replace("raion", "#")
		col = col.replace("count", "#")
		col = col.replace("sqm", "S")
		col = col.replace("office_", "")
		cols.append(col)
	return cols

def replace_feat_name(patterns):
	def replace(df):
		cols = []
		for col in list(df.columns):
			for key, value in patterns.items():
				if(key in col):
					col = col.replace(key, value)
			col = '_'.join(col.split('_'))
			cols.append(col)
		return cols
	return replace

process_rel_feat_name = replace_feat_name({
	"count": "#",
	"mosque": "m",
	"big_church": "C",
	"church": "c"
	})

hr = HouseReader()
hl = Logger("../Log/feats_group.txt")
cafs = hr.df[hr.caf_feats].drop(['catering_km'], 1)
pops = hr.df[hr.pop_feats]
rels = hr.df[hr.rel_feats]
ofcs = hr.df[hr.ofc_feats]

sns.heatmap(combine.corr(), square=True)
plt.savefig("../Figure/Raw/Corr/all_corr.png")
plt.show()

combine = combine.drop(cafs.columns, 1)
plot_corr(combine, save="../Figure/Raw/Corr/1_no_cafe.png")
# Notice that there is an area very hot at the upper left of the Figurec
corr = combine.corr()
hl.log((corr>0.9).sum().sort_values(ascending=False),
"Number other features that highly correlated to")
# Seems population features are highly correlated to each other

plot_corr(pops, "../Figure/Population/raw_corr.png")
# Learn three things from the plot
# 1. Except from those all and 16_29 population, all of them are highly correlated, 
# which explains the 21's appeared in the num of more than 0.9 correlated features
# 2. Interestingly, those all and 16_29 population are correlated highly, too
# 3. Those elder population also behave differently
# Have a more detailed insight here
hl.log((pop_corr>0.8).sum(), "Counts of feats with more than 0.8 correlation")
ind0 = (pop_corr>0.8)[(pop_corr>0.8).sum()<=6].index
ind1 = pd.Index(["ekder_all", "ekder_male", "ekder_female"])
ind2 = pops.columns.drop(ind0).drop(ind1)
pops0 = pops[ind0]
pops1 = pops[ind1]
pops2 = pops[ind2]
plot_corr(pops0, "../Figure/Population/corr_type1.png")
plot_corr(pops1, "../Figure/Population/corr_ekder.png")
plot_corr(pops2, "../Figure/Population/corr_type2.png")
# Since the lowest correlation are all large than 0.95, we can do PCA directly now to reduce dimension

pca = PCA()
pca.fit(pops0)
print(pca.explained_variance_ratio_)
pca.fit(pops1)
print(pca.explained_variance_ratio_)
pca.fit(pops2)
print(pca.explained_variance_ratio_)
# TODO 1: to add codes here...


combine = combine.drop(pops.columns, 1)
corr = combine.corr()
plot_corr(combine, save="../Figure/Raw/Corr/2_no_population.png")
hl.log((corr>0.9).sum().sort_values(ascending=False),
	"Numbers of other features more than 0.9 correlated to")
hl.log(corr['office_count_3000'].sort_values(ascending=False),
	"Correlation between office_count_3000 and other features")
# Seems those office, church and leisure things are highly correlated
hl.log(corr['church_count_3000'].sort_values(ascending=False),
	"Correlation between church_count_3000 and other features")
# Maybe we can examine the correlation in between religion objects and office object first
ofc_rel = pd.concat([ofcs, rels], axis=1)
ofc_labels = process_ofc_feat_name(ofcs)
rel_labels = process_rel_feat_name(rels)
labels = ofc_labels.append(rel_labels)
if(not os.path.exists("../Figure/Raw/Office")):
	os.makedirs("../Figure/Raw/Office")
if(not os.path.exists("../Figure/Raw/Religion")):
	os.makedirs("../Figure/Raw/Religion")
plot_corr(ofcs, labels=ofc_labels, save="../Figure/Raw/Office/raw_corr.png")
plot_corr(rels, labels=rel_labels, save="../Figure/Raw/Religion/raw_corr.png")
plot_corr(ofc_rel, labels=labels, save="../Figure/Raw/Corr/ofc_rel_corr.png")
# for office features, we may split those counts and area ones, and then study more
# for religion features, we may split big church out from church and mosque ones, and then study more
# now just do PCA on them respectively and see the results
pca.fit(ofcs)
hl.log("", "Start studying office features")
hl.log(pca.explained_variance_ratio_, "ROV explained by the principal components")
hl.log(pca.explained_variance_ratio_[:2].sum(), "ROV explained together by the 2 most principal components")
# the variance ratio explained reaches nearly 0.995 by only two PC, so we can just pause the analysis on office features here
pca.fit(rels)
hl.log("", "Start studying religion features")
hl.log(pca.explained_variance_ratio_, "ROV explained by the principal components")
hl.log(pca.explained_variance_ratio_[:3].sum(), "ROV explained together by the 3 most principal components")
# reach 0.99 with only three PC. Just stop here is acceptable


combine = combine.drop(ofcs.columns, 1).drop(rels.columns, 1)
plot_corr(combine, save="../Figure/Raw/Corr/3_no_religion_no_office.png")
# Still a lot correlation can be seen from the remained combine...
hl.log(combine.shape[1], "Columns left now:") # 161
# We can now just use 161 + (1 + 5 + 3 +1 + 1) = 172 features to represent house information now,
# whose original number of features is 290!

df = combine.drop(hr.caf_feats, 1) # version 1
df = df.drop(hr.pop_feats, 1) # version 2
df = df.drop(hr.ofc_feats, 1)
df = df.drop(hr.rel_feats, 1) # version 3

combine['railroad_terminal_raion'] = combine['railroad_terminal_raion'].map({"yes":1, "no":0})
combine['big_road1_1line'] = combine['big_road1_1line'].map({"yes":1, "no":0})
combine['railroad_1line'] = combine['railroad_1line'].map({"yes":1, "no":0})
trans = FeatureGroup(combine[hr.trp_feats], 
	name="TranPos",
	figdir="../Figure/Raw/Transportation",
	logpath="../Log/tranpos.txt")
trans.plot_corr(save=True)
trans.log(trans.top_corrs(30), "Top 30 correlated pairs")

# 'sub_area', 'area_m', 'railroad_terminal_raion', 'ID_metro',
#        'metro_min_avto', 'metro_km_avto', 'metro_min_walk', 'metro_km_walk',
#        'railroad_station_walk_km', 'railroad_station_walk_min',
#        'ID_railroad_station_walk', 'railroad_station_avto_km',
#        'railroad_station_avto_min', 'ID_railroad_station_avto',
#        'public_transport_station_km', 'public_transport_station_min_walk',
#        'mkad_km', 'ttk_km', 'sadovoe_km', 'bulvar_ring_km', 'kremlin_km',
#        'big_road1_km', 'ID_big_road1', 'big_road1_1line', 'big_road2_km',
#        'ID_big_road2', 'railroad_km', 'railroad_1line', 'zd_vokzaly_avto_km',
#        'ID_railroad_terminal', 'bus_terminal_avto_km', 'ID_bus_terminal'

railroads = []
for col in list(trans.df.columns):
	if 'railroad' in col:
		railroads.append(col)
railroads = FeatureGroup(trans.df[railroads],
	name="Railroad",
	figdir="../Figure/Raw/Transportation",
	logpath="../Log/tranpos.txt")
railroads.set_featname_processor(
	dicts={"railroad_":""})
labels = railroads.process_featname()
# railroads.set_corr_plotter(labels, "Correlation between Railroad Features")
railroads.plot_corr(save=True)

railroads2 = []
for col in list(railroads.df.columns):
	if(not "ID" in col):
		if(not "raion" in col):
			if(not "station_walk_km" in col):
				if(not "1line" in col):
					railroads2.append(col)
railroads2 = FeatureGroup(trans.df[railroads2], "Subrailroad")
railroads2.plot_corr()
pca = PCA()
pca.fit(railroads2.df.fillna(railroads2.df.mean()))
print(pca.explained_variance_ratio_)

x = trans.df[trans.corr.index]
pca.fit(x.fillna(x.mean()))
trans.log(pca.explained_variance_ratio_, "ROV explained by the principal components of TransPos features")
# The 1st principal components nearly explaine all...
# so move on to other feature groups now.
# 128 raw features left, with 1 + 5 + 3 +1 + 1 + 1 = 12 principal components for others
# magic numbers: 74


df = combine.drop(hr.trp_feats, 1) # version 4
fg = FeatureGroup(df,
	name="v4",
	figdir="../Figure/Raw/Corr")
fg.plot_corr(save=True)
fg.top_corrs(50)
# subcorr = fg.corr.iloc[50:90,50:90]
# sns.heatmap(subcorr, square=True);plt.show()
# subcorr = fg.corr.iloc[45:75,45:75]
# sns.heatmap(subcorr, square=True);plt.show()
# subcorr = fg.corr.iloc[45:74,45:74]
# sns.heatmap(subcorr, square=True);plt.show()
subcorr = fg.corr.iloc[50:74,50:74]
sns.heatmap(subcorr, square=True);plt.show()
subcorr = fg.corr.iloc[57:74,57:74]
sns.heatmap(subcorr, square=True);plt.show()
subcorr = fg.corr.iloc[50:74,50:74]
subcols = subcorr.columns
subdf = df[subcols]
pca.fit(subdf)
print(pcs.explained_variance_ratio_)
subcols=fg.corr.columns[50:74]
subdf=df[subcols]
pca.fit(subdf)
print(pca.explained_variance_ratio_)
subcols=fg.corr.columns[57:74]
pca.fit(subdf)
subdf=df[subcols]
pca.fit(subdf)
print(pca.explained_variance_ratio_[:5].sum())
subcols=fg.corr.columns[50:56]
subdf=df[subcols]
pca.fit(subdf)
print(pca.explained_variance_ratio_)
indcols = hr.ind_feats
indcols.remove('culture_objects_top_25')
indcols.remove('culture_objects_top_25')
indcols.remove('culture_objects_top_25_raion')
inds = combine[indcols]
sns.heatmap(inds.corr(), square=True);plt.show()
pca.fit(inds)
edus = hr.edu_feats
edus = combine[edus]
sns.heatmap(edus.corr(), square=True); plt.show()
educols1=edus.columns[:6]
educols2=edus.columns[-5:]
edus1 = edus[educols1]
edus2 = edus[educols2]
sns.heatmap(edus1.corr(), square=True); plt.show()
sns.heatmap(edus2.corr(), square=True); plt.show()
print(edus1.isnull().sum())
edus1v1 = edus.fillna(edus.mean())
pca.fit(edus1)
print(pca.explained_variance_ratio_)
pca.fit(edus1v1)
print(pca.explained_variance_ratio_)
print(pca.explained_variance_ratio_[:2].sum())
pca.fit(edus2)
print(pca.explained_variance_ratio_)
print(pca.explained_variance_ratio_[:2].sum)
buss = df[hr.bus_feats]
sns.heatmap(buss.corr(), square=True);plt.show()
sns.heatmap(inds.corr(), square=True);plt.show()
spts = df[hr.spt_feats]
sns.heatmap(spts.corr(), square=True);plt.show()
spts.shape
sns.heatmap(spts.corr(), square=True);plt.show()
spts1 = spts.iloc[:,1:6]
spts2 = spts.drop(spts.columns[1:6],1)
sns.heatmap(spts1.corr(), square=True);plt.show()
sns.heatmap(np.log(spts1).corr(), square=True);plt.show()
sns.heatmap(spts2.corr(), square=True);plt.show()
pca.fit(spts1)
print(pca.explained_variance_ratio_)
print(pca.fit(spts2);pca.explained_variance_ratio_)
# for spts2, it's acceptable to transform those 7 features to 1
culcols = hr.cul_feats
culs = df[culcols]
sns.heatmap(culs.corr(), square=True);plt.show()
envcols = hr.env_feats
envs = df[envcols]
sns.heatmap(envs.corr(), square=True);plt.show()
nbrcols = hr.nbr_feats
nbrs = df[nbrcols]
sns.heatmap(nbrs.corr(), square=True);plt.show()
bldcols = hr.bld_feats
blds = df[bldcols]
sns.heatmap(blds.corr(), square=True);plt.show()
