import urllib2, os, Image
from bs4 import BeautifulSoup

def getImageUrl(url='https://webmail.iitg.ernet.in'):
	proxy_handler = urllib2.ProxyHandler({})
	opener = urllib2.build_opener(proxy_handler)
	urllib2.install_opener(opener)
	req = urllib2.Request('https://webmail.iitg.ernet.in')
	r = opener.open(req)
	result = r.read()
	soup = BeautifulSoup(result)
	return url + soup.find_all('img')[1]['src']
	
for i in range(5):
	os.makedirs(str(i))
	cdir = os.getcwd()
	os.chdir(cdir + '/' + str(i))
	os.system('wget -O im.png ' + getImageUrl())
	im = Image.open('im.png')
	cr = im.crop((0,0,55,65))
	cr.save(str(0),'png')
	cr = im.crop((55,0,105,65))
	cr.save(str(1),'png')
	cr = im.crop((105,0,155,65))
	cr.save(str(2),'png')
	cr = im.crop((155,0,205,65))
	cr.save(str(3),'png')
	cr = im.crop((205,0,252,65))
	cr.save(str(4),'png')
	os.chdir(cdir)
