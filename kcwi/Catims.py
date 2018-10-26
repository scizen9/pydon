#! /usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import pydon.kcwi.wb as wb
except ImportError:
    import kcwi.wb as wb
import datetime
import astropy.io.fits as fits
import pylab as plt
import numpy as np
from scipy.stats import sigmaclip


def build_image_report(file_list=None):
    """ """
    fig = plt.figure()
    plt.ioff()
    ofile = 'catim.png'
    for nf, ifile in enumerate(file_list, start=1):
        now = datetime.datetime.now()
        timestring = "created %d-%02d-%02d at %02d:%02d:%02d" % (now.year,
                                                                 now.month,
                                                                 now.day,
                                                                 now.hour,
                                                                 now.minute,
                                                                 now.second)

        # footer = pil.get_buffer([20, 1], timestring, fontsize=15,
        #                         textprop=dict(color="0.5"), barcolor="k")
        logstr, cfgstr = wb.get_log_string(ifile)

        # Output file
        ofile = 'catim_' + ifile.split('.')[0] + '.png'

        # read image
        image_data = fits.getdata(ifile, ext=0)
        good_data, low, upp = sigmaclip(image_data)
        image_median = np.nanmedian(good_data)
        image_stdev = np.nanstd(good_data)
        vmin = image_median - image_stdev
        vmax = image_median + 3. * image_stdev

        plt.imshow(image_data, vmin=vmin, vmax=vmax, cmap='hsv')
        plt.colorbar()
        plt.figtext(0.05, .95, ifile.split('.')[0] + ': ' + cfgstr,
                    ha='left', fontsize=12)
        plt.figtext(0.45, .9, timestring, fontsize=7, ha='center')
        plt.savefig(ofile)
        print("%03d/%03d Saved %s: %s" % (nf, len(file_list), ofile, cfgstr))
        plt.clf()
    plt.close(fig)
    del fig
            
    return ofile


#################################
#
#   MAIN 
#
#################################
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage - catims <fspec>")
    else:
        flist = sys.argv[1:]
        if len(sys.argv[1:]) > 0:
            print("Cataloging %d observations" % len(sys.argv[1:]))
            report_filename = build_image_report(sys.argv[1:])
        else:
            print("No files found.")
