#!/usr/bin/env python
import pycalspec.io as calspec
from astropy.io import fits as pf
import matplotlib.pyplot as pl
import numpy as np
import sys


def make_std(std_name, out_name):
    """
    Convert STScI CALSPEC standard into KCWI_DRP format standard

    Also generates a *.png plot over KCWI wavelength range (3200-10300)

    :param std_name: str
    :param out_name: str
    :return:
    """

    fout = out_name + '.fits'
    pout = out_name + '.png'

    wave, flux, var = calspec.std_spectrum(std_name)
    dw = np.zeros(len(wave), dtype=float)

    idx = []
    for i, w in enumerate(wave):
        if i > 0:
            dw[i] = wave[i] - wave[i-1]
        if 3200 < w < 11000:
            idx.append(i)

    w = wave[idx]
    f = flux[idx]
    d = dw[idx]

    print("Avg dw: %.3f A" % np.nanmean(d))

    w0 = np.min(w)
    w1 = np.max(w)

    pl.plot(wave, flux, 'x')
    pl.xlabel("Wavelength")
    pl.ylabel("Flux")
    pl.yscale("log")
    pl.xlim(3200, 11000)
    pl.ylim(np.nanmin(f), np.nanmax(f))
    pl.title(out_name + ': %.2f - %.2f A: %d pts' % (w0, w1, len(w)))
    pl.savefig(pout, bbox_inches="tight")
    pl.show()


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: calspec2drp std_name out_name")
        sys.exit()

    std = sys.argv[1]
    out = sys.argv[2]
    make_std(std, out)
