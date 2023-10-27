#import statements

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import aplpy

from astropy.table import join
from astropy.io import ascii
from astropy.io import fits
from astropy import units as u
from astropy import wcs
from astropy.coordinates import SkyCoord

from photutils.aperture import SkyCircularAperture
from photutils.aperture import CircularAnnulus, CircularAperture
from photutils.aperture import SkyCircularAnnulus
from photutils.aperture import aperture_photometry

#common path to all files
path='/lustre/cv/students/adignan/data/'

#read in relevant data files
jy_data = fits.open(path+'NGC0337/Jyperbeam_NGC0337_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits')[0]
file3=fits.open(path+'NGC0337/ngc0337_3GHz_r0.5_smoothed_ms.pbcor.gbt_resmatched_regridded.fits')[0]
file15=fits.open(path+'NGC0337/ngc0337_15GHz_r0.5_smoothed_ms.pbcor.gbt_resmatched_regridded.fits')[0]
file33=fits.open(path+'NGC0337/ngc0337_33GHz_r0.5_smoothed_ms.pbcor.gbt_resmatched_regridded.fits')[0]

#only read in relevant axes
data3=file3.data[0,0,:,:]
data15=file15.data[0,0,:,:]
data33=file33.data[0,0,:,:]
datajy=jy_data.data[0,:,:]

#read in photometry sources Google Sheet
data = ascii.read('/lustre/cv/students/adignan/photometry_sources.csv', format='csv')

#read in Sean's catalog
df = ascii.read('/lustre/cv/students/adignan/Linden2020_table5.csv', format='csv')

#make one catalog based on my Google Sheet and Sean's catalog
minitbl=df[['Source ID','RA_J2000','Decl_J2000']]
tbl=join(data,minitbl,'Source ID')

#get the world coordinate system info
wcs3=wcs.WCS(file3).dropaxis(3).dropaxis(2)
wcs15=wcs.WCS(file15).dropaxis(3).dropaxis(2)
wcs33=wcs.WCS(file33).dropaxis(3).dropaxis(2)
wcsjy=wcs.WCS(jy_data).dropaxis(2)

#make a list of WCS info for later use (for loop)
wcss=[wcs3,wcs15,wcs33,wcsjy]

#ra and dec for this particular source
ras=['00h59m50.018s']
decs=['-07d34m33.9s']

#initialize list of aperture positions 
positions=[]

#get positions based on ra and dec
for r, d in zip(ras,decs):
    position=SkyCoord(ra=r,dec=d)
    positions.append(position)

#choose radii sizes based on beam axis length
fwhm =9.528282036*u.arcsec
rin = 1.5*fwhm 
rout = rin + fwhm

#creating lists of the apertures and annuli (defined in sky coordinates)
skyapertures=[]
skyannuli=[]

for p in positions:
    #convert positions to pixel coordinates for recentering plots later
    x1, y1 = wcs3.world_to_pixel(p)
    x2, y2= wcs15.world_to_pixel(p)
    x3, y3 = wcs33.world_to_pixel(p)
    x4, y4=wcsjy.world_to_pixel(p)
    #make the apertures and annuli (also in sky coordinates)
    skyaperture = SkyCircularAperture(p, r=fwhm)
    skyannulus = SkyCircularAnnulus(p, rin, rout)
    skyapertures.append(skyaperture)
    skyannuli.append(skyannulus)

#creating list of the apertures defined in pixel coordinates 
#(converting from sky coordinates)
pix_apertures=[]
pix_annuli=[]

for w in wcss:
    for i,j in zip(skyapertures,skyannuli):
        pix_aperture = i.to_pixel(w)
        pix_annulus = j.to_pixel(w)
        pix_apertures.append(pix_aperture)
        pix_annuli.append(pix_annulus)

#set up the subplots
fig = plt.figure(figsize=(15,15))

#3 GHz image
#plot the fits file
f1 = aplpy.FITSFigure(data3, figure=fig, subplot=[0.1,0.5,0.35,0.35])
#pick out a colormap to use
f1.show_colorscale(cmap='cubehelix')
#recenter based on pixel coordinates of aperture
f1.recenter(x1,y1,radius=50)
#plot the aperture
pix_apertures[0].plot(color='white',lw=2)
#plot the annulus
pix_annuli[0].plot(color='red', lw=2)
#try to add scalebar
f1.add_scalebar(0.01)

#15 GHz image
f2 = aplpy.FITSFigure(data15, figure=fig, subplot=[0.5,0.5,0.35,0.35])
f2.show_colorscale(cmap='cubehelix')
f2.recenter(x2,y2,radius=50)
pix_apertures[1].plot(color='white',lw=2)
pix_annuli[1].plot(color='red', lw=2)

#33 GHz image
f3 = aplpy.FITSFigure(data33, figure=fig, subplot=[0.1,0.1,0.35,0.35])
f3.show_colorscale(cmap='cubehelix')
f3.recenter(x3,y3,radius=50)
pix_apertures[2].plot(color='white',lw=2)
pix_annuli[2].plot(color='red', lw=2)

#90 GHz image
f4 = aplpy.FITSFigure(datajy, figure=fig, subplot=[0.5,0.1,0.35,0.35])
f4.show_colorscale(cmap='cubehelix')
f4.recenter(x4,y4,radius=50)
pix_apertures[3].plot(color='white',lw=2)
pix_annuli[3].plot(color='red', lw=2)