#!/kroot/rel/default/bin/kpython

# import KCWI.Red as Red

import ktl
import time
import sys
import logging

timestr = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(format='%(asctime)s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    filename="dethk"+timestr+".log")


while True:

    ktl_tempdet = ktl.cache('krds', 'TEMPDET')
    tempdet = ktl_tempdet.read()

    ktl_temppkg = ktl.cache('krds', 'TEMPPKG')
    temppkg = ktl_temppkg.read()

    # td = Red.tempdetr()
    # tp = Red.temppkgr()

    ktl_pressure = ktl.cache('krvs', 'PRESSURE')
    pressure = ktl_pressure.read()

    ktl_current = ktl.cache('krvs', 'CURRENT')
    current = ktl_current.read()

    logging.info("%s %s %s %s" % (tempdet, temppkg, pressure, current))
    sys.stdout.flush()
    time.sleep(30)
