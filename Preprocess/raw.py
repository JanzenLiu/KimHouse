from reader import *

# TODO(Janzen): Rewrite manually selecting feats with certain n_unique to calling Reader function

cr = Reader(combine)

log(cr.cat_feats,
	title=format("%d Categorical Features:" % len(cr.cat_feats)))
log("...",
	# cr.num_feats,
	title=format("%d Numerical Features:" % len(cr.num_feats)))


log(cr.df[cr.cat_feats].nunique(),
	title="Category counts for categorical features")
# Categorical features to explore further
# timestamp: map to new feature later
# sub_area: large number of categories
# ecology: not 2
log(cr.df['ecology'].value_counts())
log(cr.df['sub_area'].value_counts())
# Further exploration:
# sub_area: sub_area names seem consisting of different levels of area
# ecology: no data, poor, satisfactory, good, excellent (can map to integer)


log(cr.df[cr.num_feats].nunique(),
	title="Value counts for numeric features")
log(cr.df[cr.num_feats].nunique().sort_values().values,
	"Num of unique values of numeric features")


num_feats_2 = cr.df[cr.num_feats].loc[:,(cr.df[cr.num_feats].nunique() == 2)].columns
log(num_feats_2,
	"Numeric Features with only 2 values")
for feat in num_feats_2:
	log(cr.df[feat].value_counts())
log(cr.df['mosque_count_3000'].value_counts())
log(cr.df['mosque_count_5000'].value_counts())
# From above we can see that how rare mosque is in the living area above in Russia
# Therefore we can consider drop those features concerning mosque
# Maybe we can transform those features to one, "Religious", we'll consider it later


num_feats_3 = cr.df[cr.num_feats].loc[:,(cr.df[cr.num_feats].nunique() == 3)].columns
log(num_feats_3,
	"Numeric Features with only 3 values")
# Among which those two mosque things we have already studied
for feat in num_feats_3.drop(['mosque_count_3000', 'mosque_count_5000']):
	log(cr.df[feat].value_counts())
# It's about school, so what about without the criteion top20?
log(cr.df['school_education_centers_raion'].value_counts())
# The number of values is a bit more, but still, only 14, with maximum 14 and minimum 0


num_feats_4to5 = cr.df[cr.num_feats].loc[:,((cr.df[cr.num_feats].nunique() == 4) + (cr.df[cr.num_feats].nunique() == 5))].columns
# log(num_feats_4to5,
# 	"Numeric Features with 4 to 5 values")
for feat in num_feats_4to5:
	log(cr.df[feat].value_counts())
# From here we learn that state is a 4-value faeture, maybe same as those "excellent", "good" things, we can consider it as a categorical feature
# For neighbouring building material feature, we left it behind together with other features silimar
# For the university feature, it's the only university feature in this data set, we will learn it with other features concerning education later
# For those two features left, it's reasonable for them to include only 4 or 5 values, we left them behind, together with features of their concern
# Noticably for the cafe counts thing, we may merge its simlaer features to one, "Prosperous". We'll consider it later


num_feats_6to10 = cr.feats_with_nunique(6,11)
log(num_feats_6to10,
	"Numeric Features with only 6-10 values")
for feat in num_feats_6to10:
	log(cr.df[feat].value_counts())
# For material, we may consider it as a categorical feature. And clearly, the distribution of it is uneven. Noticably, counts of material No.3 is only two, let's see whether anything special for these two records
# For the cultural object things, there's something weird: there's a 10 with a significant counts, is it a typo of 2? We'll consider it later
# For the railway terminal ID, we could transform it to categorical, since it's only a label, with its value meaningless
# The distribution of nearby leisure facility counts is quite uneven, maybe transfore or leisure things to one "Leisure" feature?
# For the trc and those market features, we will consider them together later
# We encounter the cafe thing again, and still, a lot of building get a 0. We'll consider it later


