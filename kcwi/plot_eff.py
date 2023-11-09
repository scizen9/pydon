#! /usr/bin/env python

import matplotlib.pyplot as pl
from astropy.io import fits as pf
import numpy as np
import sys
import os

area = 760000.0

in_ea = sys.argv[1]

date = "_".join(os.path.basename(in_ea).split('_')[:2])

if 'kb' in in_ea:
    chan = 'BLUE'
elif 'kr' in in_ea:
    chan = 'RED'
else:
    print("BAD file: ", in_ea)
    sys.exit()

hdul = pf.open(in_ea)

data = hdul[0].data
hdr = hdul[0].header

hdul.close()

dd = 100.0 * data[0, :] / area
ff = 100.0 * data[1, :] / area

ww = hdr['CRVAL1'] + np.arange(len(dd)) * hdr['CDELT1']

if 'BLUE' in chan:
    grat = hdr['BGRATNAM']
    cwav = hdr['BCWAVE']
    filt = hdr['BFILTNAM']
else:
    grat = hdr['RGRATNAM']
    cwav = hdr['RCWAVE']
    filt = ''

ifu = hdr['IFUNAM']

wg0 = hdr['WAVGOOD0']
wg1 = hdr['WAVGOOD1']

if wg0 < 3650:
    wg0 = 3650.
    blue_lim = True
else:
    blue_lim = False

pngf = date + '_' + ifu + '_' + grat + '_%.0f.png' % cwav

wg0i = min([i for i in np.arange(len(ww)) if ww[i] >= wg0])
wg1i = max([i for i in np.arange(len(ww)) if ww[i] <= wg1])

ddt = dd[wg0i:wg1i]
fft = ff[wg0i:wg1i]
wwt = ww[wg0i:wg1i]

pl.plot(wwt, ddt)
pl.plot(wwt, fft)

pl.axvline(wg0, color='red')
pl.axvline(wg1, color='red')
if blue_lim:
    pl.axvline(3650., color='black')

pl.axvline(cwav, color='green')

pl.axhline(np.nanmax(fft), color='black', linestyle='dashed')
pl.axhline(np.nanmean(fft), color='blue', linestyle='dotted')

pl.xlabel("WAVE (A)")
pl.ylabel("TEL + INST EFF (%)")

pl.ylim(0, np.nanmax(fft)*1.05)

pl.title(date + " " + ifu + " " + grat + " %.0f A" % cwav)

pl.savefig(pngf, bbox_inches="tight")
pl.show()
