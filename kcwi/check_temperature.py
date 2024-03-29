#!/kroot/rel/default/bin/kpython

import ktl
import time
import sys

timestr = time.strftime("%Y-%m-%d %H:%M:%S")

verbose = False
tthresh = -100      # Temperature threshold

if len(sys.argv) > 1:
    for par in sys.argv[1:]:
        if 'v' in par:
            verbose = True
        else:
            try:
                tt = float(par)
                tthresh = tt
            except ValueError:
                print("parameter? - %s" % par)

try:
    ktl_temperature = ktl.cache('krds', 'tempdet')
except:
    if verbose:
        print(timestr + ': KRDS server not running!')
    sys.exit(0)

temperature = float(ktl_temperature.read())
# Pressure exceeds threshhold
if temperature > tthresh:
    print(timestr + ": CCD Temperature exceeds %.1f: %.1f" % (tthresh,
                                                              temperature))
else:
    if verbose:
        print(timestr + ": CCD Temperature is %.1f" % temperature)
        print(timestr + ": Threshold temp  is %.1f" % tthresh)
