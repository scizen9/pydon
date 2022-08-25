#!/kroot/rel/default/bin/kpython

import ktl
import time
import os
import glob
import logging

timestr = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

fspec = '/data/22????'
dirlist = sorted([d for d in glob.glob(fspec) if os.path.isdir(d)],
                 reverse=True)

next_image_number = -1
for d in dirlist:
    ffspec = d + '/kr?????.fits'
    flist = glob.glob(ffspec)
    if not flist:
        logging.info("No fits files in %s" % d)
        continue
    else:
        flist = sorted(flist, reverse=True)
        current_image_number = int(flist[0].split('kr')[-1])
        logging.info("Current FRAMENO: %d from %s" % (current_image_number,
                                                      flist[-1]))
        next_image_number = current_image_number + 1

if next_image_number > 0:
    logging.info("Setting FRAMENO to %d" % next_image_number)
    ktl_frameno = ktl.cache('krds', 'FRAMENO')
    ktl_frameno.write(next_image_number)
else:
    logging.warning("Could not set FRAMENO")

outdir_str = '/data/' + time.strftime("%y%m%d")
logging.info("Setting output directory to: %s" % outdir_str)

if not os.path.isdir(outdir_str):
    os.mkdir(outdir_str)
    logging.info("Created directory: %s" % outdir_str)
else:
    logging.info("Directory already exists: %s" % outdir_str)

ktl_outdir = ktl.cache('krds', 'OUTDIR')
ktl_outdir.write(outdir_str)


