"""Update GLGA thumbnail images.

Tests source jpgs for revision and updates corresponding thumbnails,
if needed.

"""

___version__ = "$Id: updt_glga_thumbs.py,v 1.2 2012/01/15 00:41:48 neill Exp $"
# $Source: /users/neill/cvshome/pylib/pydon/glga/updt_glga_thumbs.py,v $

import os
import glob
import subprocess

GLGA_ROOT = '/Users/neill/glga/data/'
# Dictionary where the filter designation defines the source jpeg file.
# The input string in the format definition is the object id.
thdict = {
        'fd' : 'uv/jpg/%s_fd_2color.jpg',
        'nd' : 'uv/jpg/%s_nd_2color.jpg',
        'xd' : 'uv/jpg/%s_xd_2color.jpg',
         'u' : 'sdss/jpg/%s_u.jpg',
         'g' : 'sdss/jpg/%s_g.jpg',
         'r' : 'sdss/jpg/%s_r.jpg',
         'i' : 'sdss/jpg/%s_i.jpg',
         'z' : 'sdss/jpg/%s_z.jpg',
         'x' : 'sdss/jpg/%s_x.jpg',
         'w' : 'sdss/jpg/%s_w.jpg',
         'j' : '2mass/jpg/%s_j.jpg',
         'h' : '2mass/jpg/%s_h.jpg',
         'k' : '2mass/jpg/%s_k.jpg',
        '2x' : '2mass/jpg/%s_x.jpg',
        'w1' : 'wise/jpg/%s_w1.jpg',
        'w2' : 'wise/jpg/%s_w2.jpg',
        'w3' : 'wise/jpg/%s_w3.jpg',
        'w4' : 'wise/jpg/%s_w4.jpg',
        'wx' : 'wise/jpg/%s_wx.jpg',
        'ww' : 'wise/jpg/%s_ww.jpg'
        }

# GLGA_ROOT contains one directory per degree
for dd in range(360):
    rute = GLGA_ROOT + '%03dD/' % dd
    # Find the existing thumbs
    for th in glob.glob(rute + 'thumbs/*.jpg'):
        # Get thumb modification time
        thmtime = os.path.getmtime(th)
        # Construct source jpeg image filename
        bname = os.path.basename(th)
        obj  = bname.split("_")[0]
        filt = bname.split("_")[1]
        # Use filter and object with thdict
        jpg = glob.glob( rute + thdict[filt] % obj )
        # If jpeg image exists
        if len(jpg) > 0:
            # Get jpeg modification time
            jpgmtime = os.path.getmtime(jpg[0])
            # If jpeg is more recent
            if jpgmtime > thmtime:
                # Use 'convert' to create new thumb
                print 'update ' + th
                subprocess.call(["convert","-thumbnail","100",jpg[0],th])


