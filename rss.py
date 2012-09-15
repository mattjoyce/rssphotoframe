#!/usr/bin/env python
import datetime
import hashlib

class rss:
    def __init__(self,fsp,title,link,pubdate=datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +1000")):
    
	self.fsp=fsp
	self.pubdate=pubdate
	self.xml="<?xml version='1.0' encoding='utf-8'?>"
	self.xml+="<rss version='2.0' xmlns:media='http://search.yahoo.com/mrss/'>"
	self.xml+="<channel><title>"+title+"</title>"
	self.xml+="<ttl>2</ttl>"
	self.xml+="<description>"+title+"</description>"
	self.xml+="<link>"+link+"</link>"

    def additem(self,title,url):
	self.xml+="<item><title>"+title+"</title>"
	self.xml+="    <link>"+url+"</link>"
	self.xml+="    <description>"+title+"</description>"
	self.xml+="    <pubDate>" + self.pubdate + "</pubDate>"
	self.xml+="    <guid isPermaLink='false'>"+hashlib.md5(url+self.pubdate).hexdigest()+"</guid>"
	self.xml+="    <media:content url='"+url+"' type='image/jpeg' />"
	self.xml+="  </item>"

    def save(self):
	xml=self.xml+"</channel></rss>"
	f=open(self.fsp,'w')
	f.write(xml)
	f.close()


pubdate = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +1000")
myrss=rss("/var/www/power/rss.xml","test","http://www.lostplot.com",pubdate)
myrss.additem("test1","http://www.lostplot.com/power/test1.jpg")
myrss.additem("test2","http://www.lostplot.com/power/test2.jpg")
myrss.save()

