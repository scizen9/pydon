import KCWI.Red as Red

import time
import sys
import logging

timestr = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
    filename="tempdet"+timestr+".log")


while True:
    td = Red.tempdetr()
    tp = Red.temppkgr()
    logging.info("%s %s" % (td, tp))
    sys.stdout.flush()
    time.sleep(30)

