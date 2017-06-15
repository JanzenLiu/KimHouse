from header import *
from reader import Reader

# TODP(Janzen): to plot the fluctuation of all macro index by the time series

mr = Reader(macro, "log_macro.txt")
mr.log(mr.cat_feats,
	title=format("%d Categorical Features:" % len(mr.cat_feats)))

mr.log("...",
	# mr.num_feats,
	title=format("%d Numerical Features:" % len(mr.num_feats)))
mr.log(mr.df.shape,
	"Shape of macro")


mr.log(mr.df[mr.cat_feats].nunique(),
	"Number of unique values of categorical features")
mr.log(mr.df["timestamp"].min(), "Earliest time in macro")
mr.log(mr.df["timestamp"].max(), "Latest time in macro")
mr.log(combine["timestamp"].min(), "Earliest transcation time")
mr.log(combine["timestamp"].max(), "Latest transcation time")
# 365*5+366*2-31-30-12
# therefore all date of transcation can be indexed in macro, that's great
for feat in mr.cat_feats:
	if(feat == "timestamp"):
		continue
	mr.log(mr.df[feat].value_counts())
# Something weired appeared
# Firstly, all category seem to present with year
# Secondly, what the hell is #! ?
mr.log(
	mr.df[mr.df["child_on_acc_pre_school"] == "7,311"]["timestamp"].apply(lambda x: x[:4]).value_counts(),
	"Year Distribution of records with '7,311' child_on_acc_pre_school")
# Well, it's very likely that those feature appear with year. We will study them later


mr.log(mr.df[mr.num_feats].nunique().sort_values().values, "Num of unique values of numeric features")
# Seems good. There're quite a lot of values with only few unique values. And possibly appear with year?

feats_7m = mr.feats_with_nunique(1, 8, "num") # stands for 7 minus
mr.log(feats_7m, "Numeric features with up to 7 values")
mr.log(len(feats_7m), "And number of feats") # 64
mr.log("", "The distribution of them")
for feat in feats_7m:
	mr.log(mr.df[feat].value_counts())
# Though not examine yet, we can say they're highly possibly to appear with year