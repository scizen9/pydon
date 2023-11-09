#! /usr/bin/env python

import matplotlib.pyplot as pl
from astropy.io import fits as pf
import numpy as np
import sys

area = 760000.0

in_ea = sys.argv[1]

if 'kb' in in_ea:
    chan = 'BLUE'
    date = in_ea.split('kb')[-1].split('_')[0]
elif 'kr' in in_ea:
    chan = 'RED'
    date = in_ea.split('kr')[-1].split('_')[0]
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

wg0i = min( [i for i in np.arange(len(ww)) if ww[i] >= wg0] )
wg1i = max( [i for i in np.arange(len(ww)) if ww[i] <= wg1] )

pl.plot(ww[wg0i:wg1i],dd[wg0i:wg1i])
pl.plot(ww[wg0i:wg1i],ff[wg0i:wg1i])

pl.axvline(wg0, color='red')
pl.axvline(wg1, color='red')

pl.axvline(cwav, color='green')

pl.axhline(np.nanmax(ff), color='black', linestyle='dashed')
pl.axhline(np.nanmean(ff), color='blue', linestyle='dotted')

pl.xlabel("WAVE (A)")
pl.ylabel("TEL + INST EFF (%)")

pl.ylim(0, np.nanmax(dd[wg0i:wg1i])*1.05)

pl.title(date + " " + ifu + " " + grat + " %.0f A" % cwav)
pl.show()

