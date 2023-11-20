#!/usr/bin/env python
import pycalspec.io as calspec
from astropy.io import fits as pf
import matplotlib.pyplot as pl
import numpy as np
import sys
import glob


def make_std(std_file, inter=False):
    """
    Generates a *.png plot over KCWI wavelength range (3200-11000)

    :param std_file: str
    :param inter: bool
    :return:
    """

    std_name = std_file.split('.fits')[0]
    pout = std_name + '.png'

    hdul = pf.open(std_file)
    wave = hdul[1].data["WAVELENGTH"]
    flux = hdul[1].data["FLUX"]
    if "FWHM" in hdul[1].data.names:
        fwhm = hdul[1].data["FWHM"]
    else:
        fwhm = None

    dw = np.zeros(len(wave), dtype=float)

    idx = []
    for i, w in enumerate(wave):
        if i > 0:
            dw[i] = wave[i] - wave[i-1]
        if 3200 < w < 11000:
            idx.append(i)

    w = wave[idx]
    f = flux[idx]
    if fwhm is not None:
        h = fwhm[idx]
        mnfw = float(np.nanmean(h))
    else:
        h = None
        mnfw = 0.0
    d = dw[idx]
    mndw = float(np.nanmean(d))

    print("Avg dw  : %.3f A" % mndw)
    if h is not None:
        print("Avg fwhm: %.3f A" % mnfw)

    w0 = np.min(w)
    w1 = np.max(w)
    nws = len(w)

    pl.plot(wave, flux, 'x')
    pl.xlabel("Wavelength")
    pl.ylabel("Flux")
    pl.yscale("log")
    pl.xlim(3200, 11000)
    pl.ylim(np.nanmin(f), np.nanmax(f))
    pl.title(std_name + ': %.2f - %.2f A: %d pts' % (w0, w1, nws))
    pl.savefig(pout, bbox_inches="tight")
    pl.clf()
    if inter:
        pl.show()

    return float(np.nanmin(wave)), float(np.nanmax(wave)), \
        w0, w1, nws, mndw, mnfw


if __name__ == '__main__':

    slist = glob.glob('*fits')
    if len(slist) <= 0:
        print("No standard fits files found")
        sys.exit()

    slist.sort()
    print("Found %d std files" % len(slist))
    sfil = open("stds_stats.txt", 'w')
    sfil.write("# STD                 w0        w1  "
               "KCWIw0   KCWIw1  KCWInw  <KCWIdw> <KCWIfwhm>\n")

    for std in slist:
        print("Plotting %s" % std)
        wl0, wl1, wk0, wk1, nk, mdw, mfw = make_std(std)
        sfil.write("%-17s %7.2f %9.2f %6.2f %8.2f %6d %8.3f %8.3f\n" %
                   (std.split('.fits')[0], wl0, wl1, wk0, wk1, nk, mdw, mfw))

    sfil.close()
