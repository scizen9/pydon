#!/usr/bin/env python
from astropy.io import fits as pf
import glob
import sys

prf = "kb"

if len(sys.argv) > 1:
    if 'RED' in sys.argv[1].upper():
        prf = "kr"

if "kr" in prf:
    print("Operating on RED images only")
else:
    print("Operating on BLUE images only")

done = False

while not done:
    q = input("Filename number range (int, int): ")
    if len(q) > 0:
        s = q.split(',')
        sfno = int(s[0])
        if len(s) > 1:
            efno = int(s[1]) + 1
        else:
            efno = sfno + 1
        k = input("Keyword (str): ")
        v = input("Value (str): ")
        t = input("Type (str): ")
        if len(t) > 0:
            if 'int' in t:
                vs = int(v)
            elif 'float' in t:
                vs = float(v)
            elif 'str' in t:
                vs = v
            else:
                print("Warning, unknown type: %s" % t)
                vs = v
        else:
            vs = v

        for fi in range(sfno, efno):
            fspec = "%05d" % fi
            flist = glob.glob(prf + "*%s.fits" % fspec)
            if len(flist) == 1:
                print(flist[0])
                pf.setval(flist[0], k, value=vs)
            elif len(flist) < 1:
                print("no files found with fspec: *%s.fits" % fspec)
            else:
                print("too many files found with fspec: *%s.fits" % fspec)
    else:
        done = True
