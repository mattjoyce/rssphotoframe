#!/usr/bin/env python
import urllib
import yaml
import datetime
import rss
from shutil import copyfile
import os
import Image
import hashlib
import imghdr

debug=True

def debug(text):
    if debug:
      print text

def download_web_image(image_source_url,localfsp):
    """Copy the contents of a file from a given URL to a local file."""
    debug('downloading '+image_source_url)
    debug('saved as '+localfsp)
    webFile = urllib.urlopen(image_source_url)
    localFile = open(localfsp,'w')
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()

def convert_localfile_to_jpg(local_image_file,local_jpg_file):
  debug('converting to jpeg')
  debug("  "+local_image_file)
  debug("  "+local_jpg_file)
  im=Image.open(local_image_file)
  if im.mode != "RGB":
    im = im.convert("RGB")
    im.save(local_jpg_file)

frameconfig=yaml.load(open('/home/matt/framer/frameconfig.yaml','r').read())
feed=frameconfig['feedinfo']
resources=frameconfig['resources']

local_dir=feed['localdir']+"/"
rss=rss.rss(feed['localdir']+"/"+feed['filename'],feed['title'],feed['description'])

#download each image, convert it to jpg if nessesary, move to folder and build rss
for item in resources:
    # use a hash for the file name as some urls are horrendous looking filenames
    md5= hashlib.sha224(item['uri']).hexdigest()
    localfsp=local_dir+md5

    # type can be file or web
    if item['type']=='file':
      debug('file')
      debug('copying '+item['uri']+' to '+localfsp)
      copyfile(item['uri'], localfsp)
    else:
      debug('web')
      download_web_image(item['uri'],localfsp)
      if not imghdr.what(localfsp)=='jpeg':
        convert_localfile_to_jpg(localfsp,localfsp+'.jpeg')

    rss.additem(item['title'],feed['link']+md5)

rss.save()
print rss.xml
print rss.fsp
