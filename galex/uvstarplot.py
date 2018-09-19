import pylab, pyfits, os
from numpy import log10
from matplotlib.font_manager import FontProperties

__version__ = "$Id"
# $Source: /users/neill/cvshome/pylib/pydon/galex/uvstarplot.py,v $

def starplot(file):	# plot UV star predictions compared with observed values
	"""Produce a plot of UV predicted countrates versus observed values."""
	tbdata = pyfits.open(file)[1].data
	obs = tbdata.field('flux')
	pred = tbdata.field('mchflux')
	g = (obs > 50.).nonzero()
	obs = obs[(obs > 50.).nonzero()]
	pred = pred[(obs > 50.).nonzero()]
	a = pylab.axes([0.15,0.52,0.75,0.38])
	pylab.plot(obs,pred-obs,'go')
	xran = pylab.xlim()
	pylab.title(file)
	pylab.plot(xran,(0.,0), linestyle=':')
	pylab.setp(a, xticks=[], xlim=(50.,xran[1]))
	pylab.ylabel('PRED - OBS Flux')
	b = pylab.axes([0.15,0.1,0.75,0.38])
	pylab.plot(obs,pred/obs,'go')
	pylab.plot(pylab.xlim(),(1.,1))
	pylab.setp(b, xlim=(50.,xran[1]))
	pylab.ylabel('PRED / OBS Flux')
	pylab.xlabel('OBS Flux > 50. ct/s')
	pylab.grid()

def cumplot(field, nuv=True, fmt='ro'):
	"""Produce a plot of UV predicted magnitudes versus observed values."""
	if nuv:
		tail = '-nd-cat_mch_flagstar.fits'
		mg0 = 20.08	# NUV zero point
	else:
		tail = '-fd-cat_mch_flagstar.fits'
		mg0 = 18.82	# FUV zero point
	if os.access(field+tail,os.R_OK):
		f = pyfits.open(field+tail)
		filt = f[0].header['starflux']
		tbdata = f[1].data
		obs = -2.5 * log10(tbdata.field('flux')) + mg0
		pred = -2.5 * log10(tbdata.field('mchflux')) + mg0
		pylab.plot(obs,obs-pred, fmt, label=field)
	else:
		print 'No data found for: '+field+tail
		return
	pylab.setp(pylab.gca(), xlim=(10,25),ylim=(-6,14))
	pylab.title(filt)
	pylab.ylabel(filt+' FLUX OVERPRIDICTION IN ABMag')
	pylab.xlabel('OBS '+filt+' ABMag')
	pylab.grid(True)

def cumplots(nuv=True, output=True):
	if nuv:
		targ = "nd"
		nuvB = True
		fmt = 'r'
	else:
		targ = "fd"
		nuvB = False
		fmt = 'b'
	pylab.clf()
	shapes = 'o^v<>s+xDd1234hHp'
	p = 0
	for file in os.listdir('./'):
		if file.find(targ) > -1 and file.find("fits") > -1:
			pfmt = fmt + shapes[ (p % len(shapes)): \
					(p % len(shapes))+1 ]
			cumplot(file[:file.find(targ)-1],fmt=pfmt,nuv=nuvB)
			p = p + 1
	pylab.legend(loc=2,numpoints=1,handletextsep=0.01, \
			prop=FontProperties(size='smaller') )
	if output:
		pylab.savefig(targ+'.pdf')

def cmdplot(field, output=True, sbplot=111):
	"""Produce a plot of UV predicted magnitudes versus observed values."""
	nuvtail = '-nd-cat_mch_flagstar.fits'
	fuvtail = '-fd-cat_mch_flagstar.fits'
	if os.access(field+nuvtail,os.R_OK):
		mg0 = 20.08	# NUV zero point
		f = pyfits.open(field+nuvtail)
		tbdata = f[1].data
		nuv_obs = -2.5 * log10(tbdata.field('flux')) + mg0
		nuv_pred = -2.5 * log10(tbdata.field('mchflux')) + mg0
		pylab.subplot(sbplot)
		pylab.plot(nuv_obs,nuv_obs-nuv_pred,'ro', \
				label=f[0].header['starflux'])
		if os.access(field+fuvtail,os.R_OK):
			mg0 = 18.82	# FUV zero point
			f = pyfits.open(field+fuvtail)
			tbdata = f[1].data
			fuv_obs = -2.5 * log10(tbdata.field('flux')) + mg0
			fuv_pred = -2.5 * log10(tbdata.field('mchflux')) + mg0
			pylab.plot(fuv_obs,fuv_obs-fuv_pred,'bo', \
					label=f[0].header['starflux'])
	else:
		print 'No NUV data found for field: '+field
		return
	pylab.setp(pylab.gca(), xlim=(12,24),ylim=(-6,12))
	pylab.title(field)
	pylab.ylabel('FLUX OVERPRIDICTION IN ABMag')
	pylab.xlabel('OBS ABMag')
	pylab.legend(loc=2,numpoints=1,handletextsep=0.01)
	pylab.grid(True)
	if output:
		pylab.savefig(field+'.pdf')

def magplot(file):	# plot UV star predictions compared with observed values
	"""Produce a plot of UV predicted magnitudes versus observed values."""
	f = pyfits.open(file)
	prihdr = f[0].header
	lab = prihdr['starflux']
	if prihdr['band'] == 1:
		mg0 = 20.08
		fmt = 'ro'
	else:
		mg0 = 18.82
		fmt = 'bo'
	tbdata = f[1].data
	obs = -2.5 * log10(tbdata.field('flux')) + mg0
	pred = -2.5 * log10(tbdata.field('mchflux')) + mg0
	pylab.plot(obs,pred,fmt,label=lab)
	pylab.legend(loc=2)
	pylab.title(file)
	pylab.plot((10,24),(10,24), linestyle='-', color='g', label='OBS = PRED')
	pylab.ylabel('PRED ABMag')
	pylab.xlabel('OBS  ABMag')
	pylab.grid(False)
