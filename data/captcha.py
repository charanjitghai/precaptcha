import urllib2, os, Image
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from bs4 import BeautifulSoup
from scipy import misc

def getImageUrl(url='https://webmail.iitg.ernet.in'):
	proxy_handler = urllib2.ProxyHandler({})
	opener = urllib2.build_opener(proxy_handler)
	urllib2.install_opener(opener)
	req = urllib2.Request('https://webmail.iitg.ernet.in')
	r = opener.open(req)
	result = r.read()
	soup = BeautifulSoup(result)
	return url + soup.find_all('img')[1]['src']
	
def getData(x,y):
	for i in range(x,y):
		os.makedirs(str(i))
		cdir = os.getcwd()
		os.chdir(cdir + '/' + str(i))
		os.system('wget -O im.png ' + getImageUrl())
		im = Image.open('im.png')
		cr = im.crop((2,0,52,65))
		cr.save(str(0),'png')
		cr = im.crop((52,0,102,65))
		cr.save(str(1),'png')
		cr = im.crop((102,0,152,65))
		cr.save(str(2),'png')
		cr = im.crop((152,0,202,65))
		cr.save(str(3),'png')
		cr = im.crop((202,0,252,65))
		cr.save(str(4),'png')
		os.system('touch capval')
		os.chdir(cdir)

def trainData(n,q):
	X = []
	Y = []
	for i in range(n):
		if i == q:
			continue
		os.chdir('/home/cj/precaptcha/data/' + str(i))
		for j in range(5):
			X.append(misc.imread(str(j)).flatten())
		fv = open('capval','r').read().split('\n')
		for v in fv:
			if v!='':
				Y.append(ord(v))
	knn = KNeighborsClassifier(n_neighbors = 2)
	knn.fit(X,Y)
	return knn

def test(n,q):
	knn = trainData(n,q)
	os.chdir('/home/cj/precaptcha/data/' + str(q))
	X = []
	for j in range(5):
		X.append(misc.imread(str(j)).flatten())
	Y = knn.predict(X)
	return [chr(v) for v in Y]

def calcAcc(n):
	d = {}
	f = {}
	c = 0
	for i in range(n):
		pred = test(n,i)
		os.chdir('/home/cj/precaptcha/data/' + str(i))
		fv = open('capval').read().split('\n')
		fv = filter(lambda x:x!='', fv)
		a = [1 if v==w else 0 for v,w in zip(pred,fv)]
		for v in fv:
			if v not in f:
				f[v] = 0
			if v not in d:
				d[v] = 0
			f[v] += 1
		for v,w in zip(pred,fv):
			if v == w:
				if v not in d:
					d[v] = 0
				d[v] += 1
		c += sum(a)
	return (c*20)/n, d, f

# acc, d, f = calcAcc(50)
# print acc
# for v in d:
# 	print v, d[v], f[v]

print test(50, 29)