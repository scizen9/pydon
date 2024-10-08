#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import glob
from astropy.io import fits

flist = glob.glob('*.raw')
for file in flist:
    sz = file.split('_')[-2]
    nx = int(sz.split('x')[0])
    ny = int(sz.split('x')[1])
    ofname = file.split('.')[0] + '.fits'
    d = np.fromfile(file,dtype=np.uint16)
    fits.writeto(ofname, d.reshape((nx, ny)))
    print(file+' ('+str(nx)+'x'+str(ny)+') fits image to '+ofname)

print('done')