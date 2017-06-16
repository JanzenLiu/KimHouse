from reader import *

# TODO(Janzen): Rewrite manually selecting feats with certain n_unique to calling Reader function
# TODO(Janzen): Write a funciton for selecting feats with n_unique, filter by some criterion and show. And then rewrite all staff doing it to calling function
# TODO(Janzen): Rewrite all calls of feats_with_nunique() as the function definintion at the class was changed
# TODO(Janzen): Rewrite the creation of the class
# TODO(Janzen): Rewrite all calls of log as it was moved from the header file to the Reader class

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


num_feats_11to20 = cr.feats_with_nunique(11,21)
log(num_feats_11to20,
	"Numeric Features with only 11-20 values")
for feat in num_feats_11to20:
	log(cr.df[feat].value_counts())
# The distribution of neighbouring cafe things is still heavily tailed, which solidate our mind to merge them to one feature
# So do the church things
# Most of the features concerning neighbouring education facility here is a bit weird. We will consider them later


# We will no more show details about neighbouring counts feature now, for simplicity
num_feats_21to50 = cr.feats_with_nunique(21,51)
log(num_feats_21to50,
	"Numeric Features with only 21-50 values")
kwds = ["church", "trc", "market", "cafe", "leisure"]
for feat in num_feats_21to50:
	flag = True
	for kwd in kwds:
		if kwd in feat:
			flag = False
	if(flag):
		log(cr.df[feat].value_counts())
# We can transform the big road ID to category, if necessary
# The distribution of nearby office feature is heavily tailed
# New topic appeared: floor
# Notice some neighborhood feature count by distance, and some simply count raion. Interesting
# Nothing else special happened
kwds.append("sport")
kwds.append("office")
kwds.append("build_count")
kwds.append("big_road")


# From now on we only print details for little features, since 50 and even hundreds of lines is a significant space waste
# We just print it to the console and determine whether to record it later
num_feats_51to150 = cr.feats_with_nunique(51,151)
rmd = [] # stands for remained
log(num_feats_51to150,
	"Numeric Features with only 51-150 values")
for feat in num_feats_51to150:
	flag = True
	for kwd in kwds:
		if kwd in feat:
			flag = False
	if(flag):
		# log(cr.df[feat].value_counts())"_part"
		rmd.append(feat)
log(rmd, "After filtering")
print(len(rmd)) # 39
for feat in rmd[:3]:
	print(cr.df[feat].dropna().astype(int).value_counts(sort=False))
# We just have a glance on them. Since the num of unique values are really large, we don't study the details now
# We'll deal with them later after studying their distribution plot
kwds.append("male")
kwds.append("female")
kwds.append("all")
kwds.append("_part")
kwds.append("preschool")
kwds.append("school")
kwds.append("hospital")
kwds.append("ID_railroad")


num_feats_151to1000 = cr.feats_with_nunique(151,1001)
rmd = [] # stands for remained
log(num_feats_151to1000,
	"Numeric Features with only 151-1000 values")
# Look at some type we haven't met
print(cr.df['cafe_sum_500_min_price_avg'].describe())
print(cr.df['cafe_sum_500_max_price_avg'].describe())
for feat in num_feats_151to1000:
	flag = True
	for kwd in kwds:
		if kwd in feat:
			flag = False
	if(flag):
		# log(cr.df[feat].value_counts())"_part"
		rmd.append(feat)
log(rmd, "After filtering")
print(len(rmd)) # 3
# It's about square meter of living area and metro, study them later


num_feats_1001to10000 = cr.feats_with_nunique(1001,10001)
rmd = [] # stands for remained
log(num_feats_1001to10000,
	"Numeric Features with only 1001-10000 values")
for feat in num_feats_1001to10000:
	flag = True
	for kwd in kwds:
		if kwd in feat:
			flag = False
	if(flag):
		# log(cr.df[feat].value_counts())"_part"
		rmd.append(feat)
log(rmd, "After filtering")
print(len(rmd)) # 1
# Only one! And it's sqaure meter again
# There are really a lot of cafe ORZ


num_feats_10001p = cr.feats_with_nunique(10001,50000) # stands for 10001 plus
rmd = [] # stands for remained
log(num_feats_10001p,
	"Numeric Features with only 10001+ values")
for feat in num_feats_10001p:
	flag = True
	for kwd in kwds:
		if kwd in feat:
			flag = False
	if(flag):
		# log(cr.df[feat].value_counts())"_part"
		rmd.append(feat)
log(rmd, "After filtering")
print(len(rmd)) # 47
# We should discard ID at the beginning, what a mistake
# Except from ID all are distances... No wonder that much unqiue values. We will process them later