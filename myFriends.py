# -*- encoding: utf-8 -*-

import requests
import re
import urllib

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def login():
	global s
	s = requests.session()
	r = s.get("http://3g.renren.com")
	html = r.text.encode('utf-8')
	reg = r'<img src=".*" alt='
	imgRe = re.compile(reg)
	img = re.findall(imgRe, html)
	imgUrl = img[0][10:-6]
	urllib.urlretrieve(imgUrl, '%s.png' % "yanzhengma")
	verifykey = imgUrl[52:-22]
	reg = r'name="lbskey" value=".*".*name="c" '
	lbskeyRe = re.compile(reg)
	lbskey = re.findall(lbskeyRe, html)[0][21:-34]
	yanzhengma = raw_input("请输入验证码")
	login_data = {
					'origURL': '',
				    'lbskey': lbskey,
					'c': '',
					'pq': '',
					'appid': '',
					'ref': 'http://m.renren.com/q.do?null',
					'email': '406716870@qq.com', 
					'password': 'yhfYHFyhf127', 
					'verifykey': verifykey,
					'verifycode': yanzhengma
				}
	s.post('http://3g.renren.com/login.do?autoLogin=true&', login_data)
	r = s.get('http://3g.renren.com')
	html = r.text.encode('utf-8')
	return html

def getFriendsListUrl(html):
	reg = '<a href="http://3g.renren.com/friendlist.do\?&amp\;sid=\w{2}-\w{19}&amp.{3,20}>'
	friendsListUrl = re.search(reg, html).group(0)[9:-2]
	return friendsListUrl

def getNextPageLink(html):
	reg = 'href="http://3g.renren.com/friendlist.do\?curpage=\d{1,3}&amp;sid=\w{2}-\w{19}&amp.{3,20}>'
	nextPageLink = re.search(reg, html).group(0)[6:-2]
	return nextPageLink

def getFriends(html):
	reg = '<td><a href="http://3g.renren.com/profile.do\?id=(\d{9})&amp;sid=\w{2}-\w{19}&amp;.{4,8}>(.{0,20})</a>'
	friendsLinks = re.findall(reg, html)
	for friend in friendsLinks:
		friendId = friend[0]
		friendName = friend[1]
		f.write(friendId + ', ')
		

	
def getFriendsPages(friendsListUrl):
	html = s.get(friendsListUrl).text.encode('utf-8')
	getFriends(html)
	while True:
		print "yiye"
		nextPageLink = getNextPageLink(html)
		html = s.get(nextPageLink).text.encode('utf-8')
		if "末页" not in html:
			getFriends(html)
			break 
		else:
			getFriends(html)
	print "end"



if __name__ == "__main__":
	html = login()
	f = open('data.py', 'w')
	f.write('')
	f.close()
	f = open('data.py', 'a')
	f.write("myFriendsIds = (")
	friendsListUrl = getFriendsListUrl(html)
	getFriendsPages(friendsListUrl)
	f.write(')')
	f.close()

