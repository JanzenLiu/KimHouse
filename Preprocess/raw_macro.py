from header import *
from reader import Reader

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
