#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2011 Wentao Han
# All rights reserved
#

import commands
import logging
import os
import os.path
import random
import re
import sys
import urllib
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import Image

WALLPAPER_URL_BASE = 'http://interfacelift.com'
WALLPAPER_INDEX_URL = WALLPAPER_URL_BASE + '/wallpaper/downloads/random/hdtv/1080p/'
WALLPAPER_CACHE = os.path.expanduser('~/Downloads/wallpapers')
WALLPAPER_URI_PATTERN = re.compile(r'<a href="(/wallpaper/\w+/\w+\.jpg)">')

logging.basicConfig(format='%(asctime)s %(levelname).1s: %(message)s',
                    level=logging.DEBUG)

def read_url(url):
    f = urllib.urlopen(url)
    content = f.read()
    f.close()
    return content

def write_file(path, data):
    dir, filename = os.path.split(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    f = open(path, 'wb')
    f.write(data)
    f.close()

def set_wallpaper_gnome(path):
    cmdline = 'gconftool-2 -t string -s /desktop/gnome/background/picture_filename "%s"' % path
    status, output = commands.getstatusoutput(cmdline)

def main(argv):
    success = False
    try:
        logging.info('reading wallpaper index page')
        page = read_url(WALLPAPER_INDEX_URL)
        uri = WALLPAPER_URI_PATTERN.findall(page)[0]
        url = WALLPAPER_URL_BASE + uri
        filename = os.path.basename(uri)
        logging.debug('wallpaper filename "%s"', filename)
        path = os.path.join(WALLPAPER_CACHE, filename)
        if not os.path.exists(path):
            logging.debug('wallpaper not exists')
            logging.info('reading wallpaper image data')
            data = read_url(url)
            logging.debug('checking wallpaper image data')
            file_obj = StringIO(data)
            image = Image.open(file_obj)
            image.load()
            logging.info('writing wallpaper image data')
            write_file(path, data)
        else:
            logging.debug('wallpaper exists')
        logging.info('changing wallpaper')
        set_wallpaper_gnome(path)
        success = True
        logging.info('all done')
    except IOError:
        logging.warn('network problem')
    except IndexError:
        logging.warn('wallpaper not found')
    if not success:
        filenames = os.listdir(WALLPAPER_CACHE)
        filename = random.choice(filenames)
        path = os.path.join(WALLPAPER_CACHE, filename)
        logging.info('changing wallpaper from cache')
        set_wallpaper_gnome(path)
        logging.info('all done')

if __name__ == '__main__':
    sys.exit(main(sys.argv))
