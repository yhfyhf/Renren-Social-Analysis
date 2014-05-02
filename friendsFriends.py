# -*- encoding: utf-8 -*-
import urllib, urllib2, cookielib
import re
from data import myFriendsIds
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


import requests

s = requests.session()
r = s.get("http://renren.com")
html = r.text.encode('utf-8')
imgUrl = "http://icode.renren.com/getcode.do?t=web_login&rnd=Math.random()"
urllib.urlretrieve(imgUrl, 'verifyCode.png')
verifyCode = None
if "icode" in html:
	verifyCode = raw_input("请输入验证码")
login_data = {'email': '406716870@qq.com', 'autoLogin':'true', 'password': 'yhfYHFyhf127', 
			  'domain':'renren.com', 'icode': verifyCode}
s.post('http://www.renren.com/PLogin.do', login_data)
r = s.get('http://www.renren.com')
# print r.text.encode('utf-8')

def getFriendsFriends(f, html, id):
	reg = '<a href="http://www.renren.com/profile.do\?id=(\d{9})">(.{2,20})</a>'
	friendsLinks = re.findall(reg, html)
	for friend in friendsLinks:
		friendId = friend[0]
		friendName = friend[1]
		if friendId == str(id):
			continue
		f.write(str(id)+', '+friendId+'\n')
	

f = open('data.csv', 'w')
f.write('')
f.close()
f = open('data.csv', 'a')

for id in myFriendsIds: 
	i = 0
	while True: 
		friendsFriendsLink = "http://friend.renren.com/GetFriendList.do?curpage=%d&id=%s" % (i, str(id))
		html = s.get(friendsFriendsLink).text.encode('utf-8')
		if "最后页" not in html:
			j = i
			for k in xrange(j, j+3):
				friendsFriendsLink = "http://friend.renren.com/GetFriendList.do?curpage=%d&id=%s" % (k, str(id))
				html = s.get(friendsFriendsLink).text.encode('utf-8')
				getFriendsFriends(f, html, id)
				# print "yiye"
			break
		else:
			getFriendsFriends(f, html, id)
			# print "yiye"
			i = i + 1

f.close()
