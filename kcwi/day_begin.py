#!/kroot/rel/default/bin/kpython

import ktl
import time
import os
import glob
import logging

timestr = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

# Get data date directories
fspec = '/data/2?????'
dirlist = sorted([d for d in glob.glob(fspec) if os.path.isdir(d)],
                 reverse=True)  # most recent first

next_image_number = -1

# Look for fits files
for d in dirlist:
    ffspec = d + '/kr?????.fits'
    flist = glob.glob(ffspec)
    if not flist:
        logging.info("No fits files in %s" % d)
        continue
    else:
        flist = sorted(flist, reverse=True)     # most recent first
        # Parse frame number from filename
        current_image_number = int(flist[0].split('kr')[-1].split('.fits')[0])
        logging.info("Current FRAMENO: %d from %s" % (current_image_number,
                                                      flist[0]))
        next_image_number = current_image_number + 1
        break

if next_image_number > 0:
    # set the next image number in server
    logging.info("Setting FRAMENO to %d" % next_image_number)
    ktl_frameno = ktl.cache('krds', 'FRAMENO')
    ktl_frameno.write(next_image_number)
else:
    # warn that we couldn't find the next number
    logging.warning("Could not set FRAMENO")

# set output directory to date string
outdir_str = '/data/' + time.strftime("%y%m%d")
logging.info("Setting output directory to: %s" % outdir_str)

# check if it already exists
if not os.path.isdir(outdir_str):
    os.mkdir(outdir_str)        # create as needed
    logging.info("Created directory: %s" % outdir_str)
else:
    logging.info("Directory already exists: %s" % outdir_str)

# set the keyword in the server
ktl_outdir = ktl.cache('krds', 'OUTDIR')
ktl_outdir.write(outdir_str)

# set the file prefix to match our convention
ktl_outfile = ktl.cache('krds', 'OUTFILE')
ktl_outfile.write('kr')

logging.info("OUTFILE set to 'kr' and OUTDIR set to %s" % outdir_str)
logging.info("Can start data taking now!")
