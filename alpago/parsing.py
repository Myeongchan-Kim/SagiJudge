import urllib2
import lxml.html as html
from BeautifulSoup import BeautifulSoup

url = 'http://tomarazzi7.tistory.com/entry/%EB%AA%B8%EC%97%90-%EC%A2%8B%EC%9D%80-%EA%B0%95%ED%99%A9-%ED%9A%A8%EB%8A%A5%ED%9A%A8%EA%B3%BC-%ED%83%90%EA%B5%AC'

req = urllib2.Request(url)
res = urllib2.urlopen(req)
page = res.read()


html.fromstring(page)

soup = BeautifulSoup(page)
print ' '.join(soup.findAll(text=True))
