""" Update gals.db from GLGA data directory """

import os
import errno
import glob
import sqlite3
import pyfits

def db_update(galsdb_dir='/Users/neill/gals/db', verbose=False):
    """
    Update the gals.db database.
    """

    # connect to db
    conn = sqlite3.connect(galsdb_dir+'/gals.db')
    c = conn.cursor()

    # get updated exposure time dictionary (only applies to GALEX data)
    exp_dict = updated_exptime(verbose=verbose)
    # get updated photometry dictionary
    pht_dict = updated_phot(verbose=verbose)
    # loop over exposure dictionary
    print 'updating {} exposure times'.format(len(exp_dict))
    for k, data in exp_dict.iteritems():
        # extract galid and filter from key
        dbstr = k.split('_')
        galid = dbstr[0]
        filt = dbstr[1]
        # check if entry esists
        c.execute("select count(*) from galdat where galid='"+galid+"'")
        if c.fetchone()[0] == 0:
            if verbose: print 'no record for {}'.format(galid)
            incmd = "insert into galdat (galid, {0}_exptime) values ('{1}', {2})".format(filt,galid,data)
            if verbose: print incmd
            c.execute(incmd)
            conn.commit()
        # update existing entry
        else:
            # build exposure time update command
            upcmd = 'update galdat set '+filt+'_exptime='+data+','+ \
                    "mod_time=DATETIME('NOW') where galid='"+galid+"'"
            if verbose: print upcmd
            c.execute(upcmd)

    # loop over photometry dictionary
    print 'updating {} photometric points'.format(len(pht_dict))
    for k, data in pht_dict.iteritems():
        # extract galid and filter from key
        dbstr = k.split('_')
        galid = dbstr[0]
        filt = dbstr[1]
        # check if entry esists
        c.execute("select count(*) from galdat where galid='"+galid+"'")
        if c.fetchone()[0] == 0:
            if verbose: print 'no record for {}'.format(galid)
            incmd = "insert into galdat (galid, {0}_int_mag, {0}_int_magerr, {0}_int_src, ra, dec, coo_src, m_ra, m_dec, majax, minax, pa, m_majax, m_minax, m_pa) values ('{1}', {2}, {3}, {4}, {5}, {6}, 'GLGA', {5}, {6}, {7}, {8}, {9}, {7}, {8}, {9})".format(filt,galid,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
            if verbose: print incmd
            c.execute(incmd)
            conn.commit()
        # update existing entry
        else:
            # build photometry update command
            upcmd = 'update galdat set '+filt+'_int_mag='+data[0]+','+ \
                filt+'_int_magerr='+data[1]+',' + \
                filt+'_int_src='+data[2]+',' + \
                'ra='+data[3]+',dec='+data[4]+",coo_src='GLGA'," + \
                'm_ra='+data[3]+',m_dec='+data[4]+',' + \
                'majax='+data[5]+',minax='+data[6]+',pa='+data[7]+',' + \
                'm_majax='+data[5]+',m_minax='+data[6]+',m_pa='+data[7]+',' + \
                "mod_time=DATETIME('NOW') where galid='"+galid+"'"
            if verbose: print upcmd
            c.execute(upcmd)

    # Close database connection
    conn.commit()
    conn.close()

def updated_exptime(galsdb_dir='/Users/neill/gals/db', verbose=False):
    """
    Return a dictionary of ids and exposure times updated since the
    last update to gals.db.  Unique entries in the dictionary are
    created by joining the galid and filter by an underscore "_". For
    example: 'NGC6744_NUV' is the dictionary key for the updated NUV 
    exposure time of NGC6744.  The only exposure times stored in the
    database are for GALEX data
    """
    # check if gals.db imfile is there
    try:
        galdb_info = os.stat(galsdb_dir+"/gals.db")
    except OSError as e:
        if e.errno == errno.ENOENT:
            print "imfile not found: "+galsdb_dir+"/gals.db"
            quit()
        else:
            raise
    else:
        # intialize imfile mod times
        galdb_mtime = galdb_info.st_mtime
        # intialize dictionary
        exp_dict = {}
        # root GLGA data directory
        dd = '/Users/neill/glga/data/'
        # loop over RA degree directories
        for d in range(0,360):
            dstr =  dd + '{}'.format(d).zfill(3)+'D/uv/fits/'
            if verbose: print dstr
            # check image files
            for name in glob.glob(dstr+'*-int.fits.gz'):
                exp_info = os.stat(name)
                # are we newer than gals.db?
                if exp_info.st_mtime > galdb_mtime:
                    # extract information from imfile name
                    imfile = os.path.split(name)[1]
                    strs = imfile.split("-")
                    galid = strs[0]
                    filt = strs[1]
                    # set correct filter
                    if filt[0] == 'f':
                        filt = 'FUV'
                    else:
                        filt = 'NUV'
                    key = galid+'_'+filt
                    if verbose: print key
                    # read fits header
                    hdr = pyfits.getheader(name)
                    # add to dictionary
                    exp_dict[key] = '{}'.format(hdr['exptime'])
                    if verbose: print exp_dict[key]
    return exp_dict

def updated_phot(galsdb_dir='/Users/neill/gals/db', verbose=False):
    """
    Return a dictionary of ids and photometry measured since the
    last update to gals.db.  Unique entries in the dictionary are
    created by joining the galid and filter by an underscore "_". For
    example: 'NGC6744_NUV' is the dictionary key for updated NUV 
    photometry of NGC6744.
    """
    # check if gals.db phfile is there
    try:
        galdb_info = os.stat(galsdb_dir+"/gals.db")
    except OSError as e:
        if e.errno == errno.ENOENT:
            print "phfile not found: "+galsdb_dir+"/gals.db"
            quit()
        else:
            raise
    else:
        # Source dictionary for GLGA photometry
        src_dict = dict(FUV='36', NUV='36',             # GALEX
                u='37', g='37', r='37', i='37', z='37', # SDSS
                j='39', h='39', k='39',                 # 2MASS
                w1='42', w2='42', w3='42', w4='42')     # WISE
        # intialize phfile mod times
        galdb_mtime = galdb_info.st_mtime
        # intialize dictionary
        pht_dict = {}
        # root GLGA data directory
        dd = '/Users/neill/glga/data/'
        # loop over RA degree directories
        for d in range(0,360):
            dstr =  dd + '{}'.format(d).zfill(3) + 'D/photometry/'
            if verbose: print dstr
            # check photometry files
            for name in glob.glob(dstr+'*_aperture.dat'):
                pht_info = os.stat(name)
                # are we newer than gals.db?
                if pht_info.st_mtime > galdb_mtime:
                    # extract information from phfile name
                    rute = os.path.split(name)[0]
                    phfile = os.path.split(name)[1]
                    strs = phfile.split("_")
                    galid = strs[0]
                    filt = strs[1]
                    key = galid+'_'+filt
                    if verbose: print key
                    # read photometry
                    with open(name,'r') as f:
                        for line in f:
                            if line.find('#') == -1:
                                phdat = line.split()
                    # read ellipse
                    with open(rute+'/'+key+'_ellipsepar.dat','r') as f:
                        for line in f:
                            if line.find('#') == -1:
                                eldat = line.split()
                                # convert semi-major/minor to major/minor
                                majax = '{}'.format(float(eldat[2])*2.)
                                minax = '{}'.format(float(eldat[3])*2.)
                                # add to dictionary:
                    pht_dict[key] = (phdat[1],       # int_mag
                                     phdat[2],       # int_magerr
                                     src_dict[filt], # source GLGA pht number
                                     eldat[0],       # ra
                                     eldat[1],       # dec
                                     majax,          # major axis (arcsec)
                                     minax,          # minor axis (arcsec)
                                     eldat[4])       # position angle (degrees)
                    if verbose: print pht_dict[key]
    return pht_dict


