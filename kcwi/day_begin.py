import KCWI.Red as Red

import ktl
import time
import sys
import logging

timestr = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

outdir_str = '/data/' + time.strftime("%y%m%d")
ktl_outdir = ktl.cache('krds', 'OUTDIR')
ktl_outdir.write(outdir_str)

logging.info("Set output directory to: %s" % outdir_str)
