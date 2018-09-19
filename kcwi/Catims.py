#! /usr/bin/env python
# -*- coding: utf-8 -*-

import kcwi.wb as wb
import datetime
import glob
import astropy.io.fits as fits
import pylab as plt
import numpy as np
from scipy.stats import sigmaclip


def build_image_report(file_list=None):
    """ """
    fig = plt.figure()
    plt.ioff()
    for nf, ifile in enumerate(file_list, start=1):
        now = datetime.datetime.now()
        timestring = "made on %d-%02d-%02d at %02d:%02d:%02d" % (now.year,
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
        plt.title(ifile.split('.')[0] + ': ' + cfgstr, loc='left')
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
    import argparse

    parser = argparse.ArgumentParser(
        description=""" Create a visual catalog of images
            """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('fspec', type=str, default="*.fits",
                        help='image file specification (*.fits)')

    # ================ #
    # END of Option    #
    # ================ #
    args = parser.parse_args()

    flist = glob.glob(args.fspec)

    if len(flist) > 0:
        print("Cataloging %d observations matching %s" % (len(flist), args.fspec))
        report_filename = build_image_report(flist)
    else:
        print("No files found matching %s" % args.fspec)
