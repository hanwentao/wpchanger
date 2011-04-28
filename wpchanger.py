#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2011 Wentao Han
# All rights reserved
#

import os
import os.path
import re
import sys
import urllib

from appscript import app
from appscript import mactypes

WALLPAPER_URL_BASE = 'http://interfacelift.com'
WALLPAPER_INDEX_URL = WALLPAPER_URL_BASE + '/wallpaper/downloads/random/widescreen/1440x900/'
WALLPAPER_CACHE = '/Users/hanwentao/Downloads/wallpapers'
WALLPAPER_URI_PATTERN = re.compile(r'<a href="(/wallpaper/\w+/\w+\.jpg)">')

def read_url(url):
    f = urllib.urlopen(url)
    content = f.read()
    f.close()
    return content

def write_file(path, data):
    f = open(path, 'wb')
    f.write(data)
    f.close()

def main(argv):
    page = read_url(WALLPAPER_INDEX_URL)
    uri = WALLPAPER_URI_PATTERN.findall(page)[0]
    url = WALLPAPER_URL_BASE + uri
    filename = os.path.basename(uri)
    path = os.path.join(WALLPAPER_CACHE, filename)
    data = read_url(url)
    write_file(path, data)
    app('Finder').desktop_picture.set(mactypes.File(path))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
