try:
	from .variables import *
	from .header import *
	from .reader import Reader
	from .feature_classifier import FeatureClassifier
except:
	from variables import *
	from header import *
	from reader import Reader
	from feature_classifier import FeatureClassifier

class HouseReader(Reader):
	def __init__(self):
		super(HouseReader, self).__init__(combine)
	fc = FeatureClassifier(combine.columns)
	self.caf_feats = fc.classify(["cafe", "catering"], "Cafe")
	self.edu_feats = fc.classify(["school", "university", "education", "kindergarten"], "Education")
	self.pop_feats = fc.classify(["_all", "male", "popul"], "Population")
	self.rel_feats = fc.classify(["church", "mosque"], "Religion")
	self.trp_feats = fc.classify(["metro", "railroad", "transport", "station", "terminal", "road", "area",
		'mkad', 'ttk', 'sadovoe', 'bulvar_ring', 'kremlin', 'zd_vokzaly'], "TransPos") # stands for transport and position
	self.nbr_feats = fc.classify("build_count", "NbrBldg") # stands for Neighbor buildings
	self.bus_feats = fc.classify(["market", "trc", "shopping_centers"], "Business")
	self.spt_feats = fc.classify(["sport", "basketball", "stadium", "fitness", "swim_pool", "ice_rink"], "Sport")
	self.ind_feats = fc.classify(["prom_part", "workplace", "indust", 
		'power', 'incineration', 'oil', 'chemistry', 'radiation', 'nuclear', "ts"], "Industry")
	self.ofc_feats = fc.classify("office", "Office")
	self.cul_feats = fc.classify(["leisure", "culture", 
		"museum", "exhibition", "theater", "park"], "Leisure")
	self.env_feats = fc.classify(["green", "water", "ecology"], "GrZone")
	self.bld_feats = fc.classify(['full_sq', 'life_sq', 'floor', 'max_floor', 'material', 'build_year',
	 'num_room', 'kitch_sq', 'state', 'product_type'], "Building")
	self.tim_feats = fc.classify("timestamp", "Time")
	self.non_feats = fc.groups["none"]