try:
	from .header import *
except Exception as e:
	from header import *
else:
	pass	
finally:
	pass

# TODO(Janzen): rewrite class fields: take non-grouped features out of the dicationary, take them as a field

class FeatureClassifier:
	def __init__(self, feats):
		self.feats = feats
		self.groups = {}
		self.groups['none'] = list(feats) # stands for features without assigned group

	def classify(self, keywords, className, overlap=False):
		if(type(keywords) == str):
			kwds = [keywords]
		else:
			kwds = list(keywords) # clone the keywords object
		self.groups[className] = []
		if(not overlap):
			cols = self.groups['none']
		else:
			cols = list(feats)
		for col in cols:
			for kwd in kwds:
				if kwd in col:
					self.groups[className].append(col)
					break
		for col in self.groups[className]:
			if col in self.groups['none']:
				self.groups['none'].remove(col)
		print("%d features selected" % len(self.groups[className]))
		print(self.groups[className])
		print("%d features unassigned" % len(self.groups["none"]))
		print(self.groups["none"])

	def toString(self):
		msg = ""
		for key, value in self.groups.items():
			if(key != "none"):
				msg += format("%d features concerning %s:\n" % (len(value), key))
				msg += format(value)
				msg += "\n"
		msg += format("%d features not assigned to any group yet:\n" % len(self.groups["none"]))
		msg += format(self.groups["none"])

	def print(self):
		print(self.toString())