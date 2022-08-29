#!/kroot/rel/default/bin/kpython

import ktl
import time
import os
import sys
from datetime import datetime

timestr = time.strftime("%Y-%m-%d %H:%M:%S")

verbose = len(sys.argv) > 1

# is krds running?
stream = os.popen('pgrep -af krds_service')
output = stream.readlines()
# Yes, it's running
if len(output) == 1:
    ktl_ccdpower = ktl.cache('krds', 'CCDPOWER')
    ccdpower = int(ktl_ccdpower.read())
    # power is on
    if ccdpower == 1:
        print(timestr + ": CCDPOWER ON!")
        # check last file
        ktl_loutfile = ktl.cache('krds', 'LOUTFILE')
        loutfile = ktl_loutfile.read()
        # loutfile is set
        if len(loutfile.strip()) > 0:
            ts = os.path.getmtime(loutfile)
            ftime = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print("Last file at " + ftime + ": " + loutfile)
        else:
            print("Last file not recorded by server")
    else:
        if verbose:
            print(timestr + ": CCDPOWER OFF")
else:
    if verbose:
        print("KRDS not running")
