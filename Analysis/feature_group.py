import sys
sys.path.append('../')
from Common import *

class FeatureGroup:
	def __init__(self, df, name, figdir=None, logpath=None):
		assert df and name
		self.df = df
		self.name = name
		self.corr = df.corr()
		self.set_featname_processor()
		if(figdir):
			self.set_figdir(figdir)
		if(logfile):
			self.set_log(logpath)
			
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

	def set_featname_processor(self, dicts={}, delimiter="@@@", jointer="@@@"):
		assert type(dicts) == dict
		assert type(delimiter) == str
		assert type(jointer) == str
		def process_featname(self):
			cols = []
			for col in list(self.df.columns):
				for key, value in dicts.items():
					if(key in col):
						col = col.replace(key, value)
				col = jointer.join(col.split(delimiter))
				cols.append(col)
			return cols
		self.process_featname = process_featname

	def set_corr_plotter(self, labels, title=None):
		def plot_corr(self, save=False):
			ax = sns.heatmap(self.corr, square=True)
		    if(labels):
				ax.set_xticklabels(labels)
				ax.set_yticklabels(labels)
				plt.xticks(rotation=30)
				plt.yticks(rotation=30)
			if(not title):
				title = self.name
			plt.title(title)
		    if(save):
		    	figpath = os.path.join(self.figdir, format("%s.png" % self.name))
		        plt.savefig(figpath)
		    plt.show()
		self.plot_corr = plot_corr
