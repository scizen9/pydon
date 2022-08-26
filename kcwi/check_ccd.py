#!/kroot/rel/default/bin/kpython

import ktl
import time
import os
import glob
import logging

timestr = time.strftime("%Y%m%d-%H%M%S")

# is krds running?
stream = os.popen('pgrep -af krds_service')
output = stream.readlines()
# Yes, it's running
if len(output) == 1:
    ktl_ccdpower = ktl.cache('krds', 'CCDPOWER')
    ccdpower = ktl_ccdpower.read()
    if ccdpower:
        print(timestr + ": CCDPOWER ON!")
    else:
        print(timestr + ": CCDPOWER OFF")
else:
    print("KRDS not running")
