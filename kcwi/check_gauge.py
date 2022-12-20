#!/kroot/rel/default/bin/kpython

import ktl
import time
import sys

timestr = time.strftime("%Y-%m-%d %H:%M:%S")

verbose = False
pthresh = 5.e-3     # Pressure threshhold

if len(sys.argv) > 1:
    for par in sys.argv[1:]:
        if 'v' in par:
            verbose = True
        else:
            try:
                tt = float(par)
                pthresh = tt
            except ValueError:
                print("parameter? - %s" % par)

try:
    ktl_pressure = ktl.cache('krgs', 'pgpress')
except:
    if verbose:
        print(timestr + ': KRGS server not running!')
    sys.exit(0)

pressure = float(ktl_pressure.read())
# Pressure exceeds threshhold
if pressure > pthresh:
    print(timestr + ": Pressure exceeds %.3e: %.3e" % (pthresh, pressure))
else:
    if verbose:
        print(timestr + ": Pressure is %.3e" % pressure)
        print(timestr + ": Threshold pressure is %.3e" % pthresh)
