#!/usr/bin/env python
import yaml
import datetime
import rss
from shutil import copyfile
import os
import Image

def download(url,path,uid):
    """Copy the contents of a file from a given URL to a local file."""
    import urllib
    webFile = urllib.urlopen(url)
    localFile = open(path+uid+url.split('/')[-1], 'w')
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()

frameconfig=yaml.load(open('/home/matt/framer/frameconfig.yaml','r').read())
feed=frameconfig['feedinfo']
resources=frameconfig['resources']

local_dir=feed['localdir']+"/"

rss=rss3.rss(feed['localdir']+"/"+feed['filename'],feed['title'],feed['description'])

for item in resources:
    filename=os.path.split(item['uri'])[1]
    if item['type']=='file':
	dst=local_dir+item['uid']+filename
	copyfile(item['uri'], dst)
        rss.additem(item['title'],feed['link']+item['uid']+filename)
    else:
	download(item['uri'],local_dir,item['uid'])
	f, e = os.path.splitext(item['uid']+filename)
	if e.lower()==".jpg" or e.lower()=='jpeg':
	    print 'adding'
	    rss.additem(item['title'],item['uri'])
	else:
	    print 'converting.. '+local_dir+item['uid']+filename
	    im=Image.open(local_dir+item['uid']+filename)
	    if im.mode != "RGB":
		im = im.convert("RGB")
	    print 'saving... '+local_dir+f+'.jpg'
	    im.save(local_dir+f+'.jpg')
	    rss.additem(item['title'],feed['link']+f+'.jpg')

rss.save()
print rss.xml
print rss.fsp
