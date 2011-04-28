#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2011 Wentao Han
# All rights reserved
#

import logging
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

logging.basicConfig(level=logging.DEBUG)

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
    try:
        logging.info('reading wallpaper index page')
        page = read_url(WALLPAPER_INDEX_URL)
        uri = WALLPAPER_URI_PATTERN.findall(page)[0]
        url = WALLPAPER_URL_BASE + uri
        filename = os.path.basename(uri)
        logging.debug('wallpaper filename "%s"', filename)
        path = os.path.join(WALLPAPER_CACHE, filename)
        logging.info('reading wallpaper image data')
        data = read_url(url)
        logging.info('writing wallpaper image data')
        write_file(path, data)
        logging.info('changing wallpaper')
        app('Finder').desktop_picture.set(mactypes.File(path))
        logging.info('all done')
    except IOError:
        logging.error('network problem')
        return 1
    except IndexError:
        logging.error('wallpaper not found')
        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
