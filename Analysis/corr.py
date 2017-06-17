import sys
sys.path.append('../')
from Common import *
 
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

