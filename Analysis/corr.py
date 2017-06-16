import sys
sys.path.append('../')
from Common import *
 
# TODO(Janzen): To further reduce dimension for population features

def plot_corr(df, save=None):
    sns.heatmap(df.corr(), square=True)
    if(save):
        plt.savefig(save)
    plt.show()

hr = HouseReader()
hl = Logger("../Log/feats_group.txt")
cafs = hr.df[hr.caf_feats].drop(['catering_km'], 1)
pops = hr.df[hr.pops_feats]

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
pca.fit(pops1)
pca.fit(pops2)
# TODO 1: to add codes here...


combine = combine.drop(pops.columns, 1)
corr = combine.corr()
plot_corr(combine, save="../Figure/Raw/Corr/2_no_population.png")