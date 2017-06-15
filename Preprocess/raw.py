from reader import *

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


num_feats2 = cr.df[cr.num_feats].loc[:,(cr.df[cr.num_feats].nunique() == 2)].columns
log(num_feats2,
	"Numeric Features with only 2 values")
for feat in num_feats2:
	log(cr.df[feat].value_counts())
log(cr.df['mosque_count_3000'].value_counts())
log(cr.df['mosque_count_5000'].value_counts())
# From above we can see that how rare mosque is in the living area above in Russia
# Therefore we can consider drop those feature concerning mosque