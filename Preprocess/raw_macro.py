from header import *
from reader import Reader

mr = Reader(macro, "log_macro.txt")
mr.log(mr.cat_feats,
	title=format("%d Categorical Features:" % len(mr.cat_feats)))
mr.log("...",
	# mr.num_feats,
	title=format("%d Numerical Features:" % len(mr.num_feats)))


