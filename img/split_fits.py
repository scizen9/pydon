#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""split_fits - break out multi-unit fits files into individual images
"""
from astropy.io import fits as pf
import numpy as np


def split_img(hdul, unit_list, filename=None):
    if filename is not None:
        out_prefix = filename.split('.')[0]
    else:
        out_prefix = 'img'
    header = hdul[0].header
    for un in unit_list:
        data = hdul[un].data
        if 'VIDEOINP' in hdul[un].header:
            header['VIDEOINP'] = hdul[un].header['VIDEOINP']
        new_hdu = pf.PrimaryHDU(data, header=header)
        new_hdu.writeto("%s_%02d.fits" % (out_prefix, un))


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage - split_fits <filename> <n_images>")
    else:
        hdu_list = pf.open(sys.argv[1])
        ulist = np.arange(1, int(sys.argv[2])+1)
        split_img(hdu_list, ulist, filename=sys.argv[1])
        hdu_list.close()
