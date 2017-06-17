import sys
sys.path.append('../')
from Common import *

class FeatureGroup:
	def __init__(self, df, name, figdir=None, logpath=None):
		assert type(df)  == pd.DataFrame
		assert type(name) == str
		self.df = df
		self.name = name
		self.corr = df.corr()
		self.set_featname_processor()
		self.set_corr_plotter()
		if(figdir):
			self.set_figdir(figdir)
		if(logpath):
			self.set_log(logpath)

	def top_corrs(self, n=20):
		au_corr = self.corr.abs().unstack()
		to_drop = redundant_pairs(self.corr)
		au_corr = au_corr.drop(labels=to_drop).sort_values(ascending=False)
		return au_corr[:n]

	def set_figdir(self, figdir):
		assert figdir
		if(not os.path.exists(figdir)):
			os.makedirs(figdir)
		self.figdir = figdir

	def set_log(self, logpath):
		assert logpath
		logdir = os.path.dirname(logpath)
		logname = os.path.basename(logpath)
		if(not os.path.exists(logdir)):
			os.makedirs(logdir)
		if(not logname):
			logname = format("%s.txt" % self.name)
		self.logdir = logdir
		self.logname = logname
		self.logpath = os.path.join(logdir, logname)
		self.log = Logger(self.logpath).log # don't know whether correct

	def set_featname_processor(self, dicts={}, delimiter="_", jointer="_"):
		self.process_featname = featnameproc_Wrapper(self, dicts, delimiter, jointer)

	def set_corr_plotter(self, labels=None, title=None):
		if(not title):
			title = self.name
		self.plot_corr = corrplot_Wrapper(self, title, labels)


def corrplot_Wrapper(self, title, labels=None):
	def plot_corr(self=self, save=False):
		ax = sns.heatmap(self.corr, square=True)
		if(labels):
			ax.set_xticklabels(labels)
			ax.set_yticklabels(labels)
			plt.xticks(rotation=30)
			plt.yticks(rotation=30)
		plt.title(title)
		if(save):
			figpath = os.path.join(self.figdir, format("%s.png" % self.name))
			plt.savefig(figpath)
		plt.show()
	return plot_corr

def featnameproc_Wrapper(self, dicts, delimiter, jointer):
	assert type(dicts) == dict
	assert type(delimiter) == str
	assert type(jointer) == str
	def process_featname(self=self):
		cols = []
		for col in list(self.df.columns):
			for key, value in dicts.items():
				if(key in col):
					col = col.replace(key, value)
			col = jointer.join(col.split(delimiter))
			cols.append(col)
		return cols
	return process_featname

def redundant_pairs(df):
	pairs = set()
	cols = df.columns
	for i in range(df.shape[1]):
		for j in range(i+1):
			pairs.add((cols[i], cols[j]))
	return pairs