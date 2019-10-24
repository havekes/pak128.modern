﻿#! /usr/bin/python
#  -*- coding: utf-8 -*-
#
#  Vladimír Slávik 2008-2011
#  Python 2.5-3.1
#
#  for Simutrans
#  http://www.simutrans.com
#
#  code is public domain
#

# read all dat files in all subfolders and produce list of these that have
# wrong color type (other than 24bit)

from __future__ import print_function, division

import os, glob
from socket import ntohl
from struct import unpack

badcounter = 0
allcounter = 0

png_types = {
	0: "grayscale",
	2: "RGB",
	3: "indexed",
	4: "grey+alpha",
	6: "RGBA",
}

#-----

def pngType(color, palette) :
	try :
		kind = png_types[color]
	except :
		kind = str(color)
	return " color type: %s, %d bpp" % (kind, palette)

#-----

def procFile(png) :
	global badcounter, allcounter
	f = open(png, 'rb')
	f.seek(8 + (4 + 4) + (4 + 4))
	# 8 bytes header, 4 length, 4 IHDR, 4+4 width+height
	d = unpack("B", f.read(1))[0] # read "bit depth/palette" entry
	c = unpack("B", f.read(1))[0] # read "color" entry
	
	if (c != 2) or (d != 8) :
		print(png)
		print(pngType(c, d))
		badcounter = badcounter + 1
	f.close()
	allcounter = allcounter + 1

#-----

def walkFiles(topdir) :
	for png in glob.glob(os.path.join(topdir, "*.png")) :
		procFile(png)
	for fsitem in glob.glob(os.path.join(topdir, "*")) :
		if os.path.isdir(fsitem) :
			if not os.path.exists(os.path.join(topdir, fsitem, "statsignore.conf")) :
				walkFiles(os.path.join(topdir, fsitem))


#-----

badcounter = 0
allcounter = 0

walkFiles(os.getcwd())
print("%d of %d files bad, or %.2f%%" % (badcounter, allcounter, 100*badcounter/allcounter))

# EOF
