from reader import *

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
# Therefore we can consider drop those feature concerning mosque

num_feats_3 = cr.df[cr.num_feats].loc[:,(cr.df[cr.num_feats].nunique() == 3)].columns
log(num_feats_3,
	"Numeric Features with only 3 values")
# Among which those two mosque things we have already studied
for feat in num_feats_3.drop(['mosque_count_3000', 'mosque_count_5000']):
	log(cr.df[feat].value_counts())
# It's about school, so what about without the criteion top20?
log(cr.df['school_education_centers_raion'].value_counts())
# The number of values is a bit more, but still, only 14, with maximum 14 and minimum 0

