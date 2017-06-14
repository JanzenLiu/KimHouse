from header import *

# TODO: remove the redundant xlabel of timestamp plot
# TODO: eliminate the influence of start/end time in the middle of a year to timestamp distribution
# TODO: fix int represented as float problem (cause: existence of NaN data)
# TODO: set text rotation for xlabel globally
# TODO: refactor the code

# combine['timestamp'].nunique()
# 1435

# combine['timestamp'].value_counts().sort_values(ascending=False).head()
# 2014-12-16    160
# 2014-12-09    147
# 2014-06-30    133
# 2014-12-18    118
# 2014-11-25     93

# combine['timestamp'].sort_values().iloc[0]
# combine['timestamp'].sort_values().iloc[-1]
# 2011-08-20
# 2016-05-30

combine['trans_year'] = combine['timestamp'].apply(lambda x: int(x[:4]))
combine['trans_month'] = combine['timestamp'].apply(lambda x: int(x[5:7]))
combine['trans_day'] = combine['timestamp'].apply(lambda x: int(x[8:]))

def plot_timestamp_count()
	plt.figure(figsize=(12,8))
	sns.countplot(x='timestamp', data=combine) # TODO 1
	plt.show()

def plot_split_timestamp_count(): # TODO 2
	plt.figure(figsize=(12,15))
	plt.subplot(311)
	sns.countplot(x='trans_year', data=combine)
	plt.subplot(312)
	sns.countplot(x='trans_month', data=combine)
	plt.subplot(313)
	sns.countplot(x='trans_day', data=combine)
	plt.show()

# np.sort(combine['floor'].dropna().unique())
# np.sort(combine['max_floor'].dropna().unique())
# array([  0.,   1.,   2.,   3.,   4.,   5.,   6.,   7.,   8.,   9.,  10.,
#         11.,  12.,  13.,  14.,  15.,  16.,  17.,  18.,  19.,  20.,  21.,
#         22.,  23.,  24.,  25.,  26.,  27.,  28.,  29.,  30.,  31.,  32.,
#         33.,  34.,  36.,  37.,  38.,  40.,  41.,  44.,  77.])
# array([   0.,    1.,    2.,    3.,    4.,    5.,    6.,    7.,    8.,
#           9.,   10.,   11.,   12.,   13.,   14.,   15.,   16.,   17.,
#          18.,   19.,   20.,   21.,   22.,   23.,   24.,   25.,   26.,
#          27.,   28.,   29.,   30.,   31.,   32.,   33.,   34.,   35.,
#          36.,   37.,   38.,   39.,   40.,   41.,   42.,   44.,   45.,
#          47.,   48.,   57.,   99.,  117.])
# Issue: existence of some extremely tall builings

def plot_floors():
	plt.figure(figsize=(14,12))
	plt.subplot(211)
	sns.countplot(x='floor', data=combine)
	plt.xticks(rotation=75)
	plt.subplot(212)
	sns.countplot(x='max_floor', data=combine)
	plt.xticks(rotation=75)
	plt.show()

def plot_material():
	plt.figure(figsize=(12,8))
	sns.countplot(x='material', data=combine)
	plt.xticks(rotation=75)

# combine[combine['material'] == 3][['id', 'material']]
#  			   id 	material
# 24715 	24718 	3.0
# 36780 	36783 	3.0
# Issue: only two transation where the material of the house is 3

def plot_buildyear():
	plt.figure(figsize=(15,8))
	sns.countplot(x='build_year', data=combine)
	plt.xticks(rotation=90)
	plt.show()

# combine[combine['build_year'] < 1900]['build_year'].value_counts().sort_index()
# 0.0       899
# 1.0       555
# 2.0         1
# 3.0         2
# 20.0        1
# 71.0        1
# 215.0       2
# 1691.0      1
# 1860.0      2
# 1875.0      1
# 1876.0      1
# 1886.0      1
# 1890.0      7
# 1895.0      2
# 1896.0      2
# 1898.0      1
# Issue: existence of some build_year that do not make sense

def plot_nroom():
	plt.figure(figsize=(12,8))
	sns.countplot(x='num_room', data=combine)
	plt.show()

# combine['num_room'].value_counts()
# 2.0     11229
# 1.0     10457
# 3.0      6229
# 4.0       551
# 5.0        59
# 0.0        14
# 6.0        10
# 7.0         3
# 8.0         3
# 10.0        2
# 19.0        2
# 17.0        1
# 9.0         1
# Issue: the extremely uneven distribution of num_room

def plot_state():
	plt.figure(figsize=(12,8))
	sns.countplot(x='state', data=combine)
	plt.show()

# combine['state'].value_counts()
# 2.0     8506
# 3.0     7703
# 1.0     7121
# 4.0      549
# 33.0       1
# Issue: special value and uneven frequency for state 4

def plot_productype():
	plt.figure(figsize=(12,8))
	sns.countplot(x='product_type', data=combine)
	plt.show()

def plt_subarea():
	plt.figure(figsize=(12,8))
	sns.countplot(x='sub_area', data=combine)
	plt.show()

def plot_subarea_rank():
	rank = combine['sub_area'].value_counts().index
	plt.figure(figsize=(12,8))
	sns.countplot(x='sub_area', data=combine, order=rank)
	plt.show()

# combine['sub_area'].unique()
# combine['sub_area'].unique()
# array(['Bibirevo', 'Nagatinskij Zaton', "Tekstil'shhiki", 'Mitino',
#        'Basmannoe', 'Nizhegorodskoe', "Sokol'niki", 'Koptevo', 'Kuncevo',
#        'Kosino-Uhtomskoe', 'Zapadnoe Degunino', 'Presnenskoe', 'Lefortovo',
#        "Mar'ino", "Kuz'minki", 'Nagornoe', "Gol'janovo", 'Vnukovo',
#        'Juzhnoe Tushino', 'Severnoe Tushino', "Chertanovo Central'noe",
#        'Fili Davydkovo', 'Otradnoe', 'Novo-Peredelkino', 'Bogorodskoe',
#        'Jaroslavskoe', 'Strogino', 'Hovrino', "Moskvorech'e-Saburovo",
#        'Staroe Krjukovo', 'Ljublino', 'Caricyno', 'Veshnjaki',
#        'Danilovskoe', 'Preobrazhenskoe', "Kon'kovo", 'Brateevo',
#        'Vostochnoe Izmajlovo', 'Vyhino-Zhulebino', 'Donskoe',
#        'Novogireevo', 'Juzhnoe Butovo', 'Sokol', 'Kurkino', 'Izmajlovo',
#        'Severnoe Medvedkovo', 'Rostokino', 'Orehovo-Borisovo Severnoe',
#        'Ochakovo-Matveevskoe', 'Taganskoe', 'Dmitrovskoe',
#        'Orehovo-Borisovo Juzhnoe', 'Teplyj Stan', 'Babushkinskoe',
#        'Pokrovskoe Streshnevo', 'Obruchevskoe', 'Filevskij Park',
#        'Troparevo-Nikulino', 'Severnoe Butovo', 'Hamovniki', 'Solncevo',
#        'Dorogomilovo', 'Timirjazevskoe', 'Lianozovo', 'Pechatniki',
#        'Krjukovo', 'Jasenevo', 'Chertanovo Severnoe', 'Rjazanskij',
#        'Silino', 'Ivanovskoe', 'Golovinskoe', 'Novokosino',
#        'Nagatino-Sadovniki', 'Birjulevo Vostochnoe', 'Severnoe Izmajlovo',
#        'Sokolinaja Gora', 'Vostochnoe Degunino', 'Prospekt Vernadskogo',
#        'Savelki', 'Ajeroport', 'Vojkovskoe', 'Beskudnikovskoe',
#        'Krylatskoe', 'Juzhnoportovoe', 'Perovo', 'Akademicheskoe',
#        'Horoshevo-Mnevniki', 'Shhukino', 'Kapotnja', 'Horoshevskoe',
#        'Marfino', 'Chertanovo Juzhnoe', 'Savelovskoe',
#        'Birjulevo Zapadnoe', 'Nekrasovka', 'Cheremushki', 'Sviblovo',
#        'Alekseevskoe', "Krasnosel'skoe", 'Kotlovka', 'Zjuzino',
#        'Ostankinskoe', 'Tverskoe', 'Losinoostrovskoe', 'Butyrskoe',
#        'Matushkino', 'Metrogorodok', 'Juzhnoe Medvedkovo', 'Lomonosovskoe',
#        'Jakimanka', 'Mozhajskoe', 'Levoberezhnoe', "Mar'ina Roshha",
#        'Gagarinskoe', "Zamoskvorech'e", "Altuf'evskoe", 'Ramenki',
#        'Zjablikovo', 'Meshhanskoe', 'Severnoe', 'Begovoe', 'Arbat',
#        'Poselenie Sosenskoe', 'Poselenie Moskovskij',
#        'Poselenie Pervomajskoe', 'Poselenie Desjonovskoe',
#        'Poselenie Voskresenskoe', 'Poselenie Mosrentgen', 'Troickij okrug',
#        'Poselenie Shherbinka', 'Poselenie Filimonkovskoe',
#        'Poselenie Vnukovskoe', 'Poselenie Marushkinskoe',
#        'Poselenie Shhapovskoe', 'Poselenie Rjazanovskoe',
#        'Poselenie Kokoshkino', 'Vostochnoe', 'Poselenie Krasnopahorskoe',
#        'Poselenie Novofedorovskoe', 'Poselenie Voronovskoe',
#        'Poselenie Klenovskoe', 'Poselenie Rogovskoe', 'Poselenie Kievskij',
#        'Molzhaninovskoe', 'Poselenie Mihajlovo-Jarcevskoe'])
# Issue 1: to group sub_area by name and find relation
# Issue 2: to plot a count plot by rank instead of sub_area with order (or by group)