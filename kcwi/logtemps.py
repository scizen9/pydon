#!/kroot/rel/default/bin/kpython

import KCWI.Red as Red

import ktl
import time
import sys
import logging

timestr = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    filename="dethk"+timestr+".log")


while True:
    td = Red.tempdetr()
    tp = Red.temppkgr()

    ktl_pressure = ktl.cache('krvs', 'PRESSURE')
    pressure = ktl_pressure.read()

    ktl_current = ktl.cache('krvs', 'CURRENT')
    current = ktl_current.read()

    logging.info("%s %s %s %s" % (td, tp, pressure, current))
    sys.stdout.flush()
    time.sleep(30)
