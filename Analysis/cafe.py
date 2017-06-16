import sys
sys.path.append('../')
from Common import *

def process_feat_name(df):
	labels = []
	for feat in list(df.columns):
		feat = feat.replace("count", "#")
		feat = feat.split("_")
		feat.remove(dist)
		feat.remove("cafe")
		if("sum" in feat):
			feat.remove("sum")
		if("min" in feat or "max" in feat):
			feat.remove("avg")
		if("price" in feat):
			feat.remove("price")
		feat = " ".join(feat)
		labels.append(feat)
	return labels

def split_by_type(df):
	prices = pd.DataFrame()
	counts = pd.DataFrame()
	for i in range(6):
		base = 11 * i
		prices = pd.concat([prices, df.iloc[:,base+1:base+4]], axis=1)
		counts = pd.concat([counts, df.iloc[:,base:base+1], df.iloc[:,base+4:base+11]], axis=1)
	return prices, counts

hr = HouseReader()
hl = Logger("../Log/feats_group.txt")
hl = Logger("","Start analyzing features for Cafe")
cafs = hr.df[hr.caf_feats].drop(['catering_km'], 1)
prices, counts = split_by_type(cafs)

plt.figure(figsize=(12,8))
sns.heatmap(cafs.corr(), square=True)
plt.savefig('../Figure/Raw/Cafe/raw_corr.png')
plt.show()
# interesting pattern, right?
# let's study it further

# first split them by distance
cafs500 = cafs.iloc[:,:11]
cafs1000 = cafs.iloc[:,11:22]
cafs1500 = cafs.iloc[:,22:33]
cafs2000 = cafs.iloc[:,33:44]
cafs3000 = cafs.iloc[:,44:55]
cafs5000 = cafs.iloc[:,55:]

caf_by_dist = [cafs500, cafs1000, cafs1500, cafs2000, cafs3000, cafs5000]

pos = 230
plt.figure(figsize=(15,12))
for item in caf_by_dist:
	dist = item.columns[-1].split("_")[2]
	labels = process_feat_name(item)
	pos += 1
	plt.subplot(pos)
	sns.heatmap(item.corr(), square=True, xticklabels=labels, yticklabels=labels, vmin=0.15)
	plt.xticks(rotation=30, fontsize=8)
	plt.yticks(rotation=30, fontsize=8)
	plt.title("Distance: %s" % dist)
plt.subplots_adjust(left=0.1, right=0.9, wspace=0.2, hspace=0.4)
plt.savefig("../Figure/Raw/Cafe/corr_each_dist.png")
plt.show()
# from the figure we learn that
# 1. With the distance increases, the correlation between cafe counts increases
# 2. The min/max/avg of average price of cafe bill within the distance was very weakly positively related to the cafe counts, but after all, not negetively
# 3. The correlation between the price statistics and cafe counts decreases as the distance increases.
# 4. When the distance is 500, the price statistics are correlated to the counts of expensive cafe noticably, though not to a high level
# Maybe we can consider those 500-distance data more important? We will learn more later

pos = 230
plt.figure(figsize=(15,12))
for item in caf_by_dist:
	df = pd.concat([item.iloc[:,4:], item.iloc[:,:1]], axis=1)
	dist = item.columns[-1].split("_")[2]
	labels = process_feat_name(df)
	pos += 1
	plt.subplot(pos)
	sns.heatmap(df.corr(), square=True, xticklabels = labels, yticklabels=labels, vmin=0.6)
	plt.xticks(rotation=30, fontsize=8)
	plt.yticks(rotation=30, fontsize=8)
	plt.title("Cafe counts by distance: %s" % dist)
plt.subplots_adjust(left=0.1, right=0.9, wspace=0.2, hspace=0.4)
plt.savefig("../Figure/Raw/Cafe/count_corr_each_dist.png")
plt.show()

pos = 230
plt.figure(figsize=(15,12))
for item in caf_by_dist:
	df = item.iloc[:,1:4]
	dist = item.columns[0].split("_")[-1]
	labels = process_feat_name(df)
	pos += 1
	plt.subplot(pos)
	sns.heatmap(df.corr(), square=True, xticklabels = labels, yticklabels=labels, vmin=0.98)
	plt.xticks(rotation=30, fontsize=8)
	plt.yticks(rotation=30, fontsize=8)
	plt.title("Cafe avg bill by distance: %s" % dist)
plt.subplots_adjust(left=0.1, right=0.9, wspace=0.2, hspace=0.4)
plt.savefig("../Figure/Raw/Cafe/price_corr_each_dist.png")
plt.show()
# from the pictures we can see that, with the distance fixed, counts are very highly correlated, so do those price statistics
# Maybe we can reconstruct all those cafe features to no more than 5 features, which will significantly save time and computational power for us


pca = PCA()
hl.log(counts.isnull().sum(), "Number of nan in counts features")
# see, there is no NaN in counts, therefore we can do PCA directly
pca.fit(counts)
hl.log(format("Reduced to %d components" % pca.n_components_),"Doing PCA on raw counts features...")
hl.log(pca.explained_variance_ratio_, "ROV explained by the principal components")
hl.log(pca.explained_variance_ratio_[:2].sum(), "ROV explained together by the 2 most principal components")
# the 1st principle component explains more than 0.95 of the variance,
# and together with the 2nd explain more than 0.99 (nearly 0.999).
# Maybe we don't need to further study in these cafe features... 
# Just use one or two features to represent them seems reasonable
# But we need to preserve some significant signal for high/low house price. We will consider it later

hl.log(prices.isnull().sum(), "Number of nan in prices features")
# to much NaN in those 500 featues
# notice that the NaN within a given distance seem to appear together
prices_filled = prices.fillna(prices.mean())
# we simply fill NaN with mean to keep the variance, I know it may affect the result but just ignore it now
hl.log(format("Reduced to %d components" % pca.n_components_), "Doing PCA on prices features, imputed by their mean")
pca.fit(prices_filled)
hl.log(pca.explained_variance_ratio_, "ROV explained by the principal components")
hl.log(pca.explained_variance_ratio_[:5].sum(), "ROV explained together by the 5 most principal components")
# 5 components together explain 0.96, acceptable. We'll discuss later
