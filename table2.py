from astropy.table import Table
from astropy.io import ascii, fits
import pandas as pd
from astropy.constants import k_B
import numpy as np
from astropy import units as u

#need list of all sources
galaxies=['NGC 0337','NGC 0628','NGC 0925','NGC 2146','NGC 2798','NGC 2841','NGC 3049',
          'NGC 3190','NGC 3184','NGC 3198','NGC 3351','NGC 3521','NGC 3627','NGC 3773',
          'NGC 3938','NGC 4254','NGC 4321','NGC 4536','NGC 4559','NGC 4569','NGC 4579',
          'NGC 4594','NGC 4625','NGC 4631','NGC 4725','NGC 5194','NGC 5474','NGC 5713',
          'NGC 6946','NGC 7331']

galaxies_final=[]

for d in galaxies:
    string=('\,'.join([d[:3], d[4:]]))
    galaxies_final.append(string)

#read in file with bmaj and bmin info 
beamfile=pd.read_csv('/users/adignan/csv/beam_info.csv')

#make a temporary dataframe from our list of sources for sorting purposes
# temp = pd.DataFrame({'source' : galaxies})

# #"sort" beamfile by galaxies list so everything is in same order
# beamfile=pd.merge(temp, beamfile,left_on='source',right_on='source',how='outer')

# print(beamfile)

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits

ras=[]
decs=[]
beam=[]
intgtimes=[]

for index, row in beamfile.iterrows():
#     print(row['jyfile'])
    hdu=fits.open(row['jyfile'])
    data0, data1, header = hdu[0].data, hdu[1].data, hdu[0].header
    c=SkyCoord(ra=header['CRVAL1']*u.degree,dec=header['CRVAL2']*u.degree)
#     print(c.ra.hms,c.dec.hms,row['source'])
    rahour,raminute,rasec=c.ra.hms
    rahour=int(rahour)
    raminute=int(raminute)
    dechour,decminute,decsec=c.dec.hms
    dechour=int(dechour)
    decminute=int(decminute)
#     sec=str(round(sec, 5))
#     sec=(sec.zfill(4))
#     sec=sec.ljust(6,'0')
    ras.append(f'{rahour:02d} {raminute:02d} {rasec:0.2f}')
    decs.append(f'{dechour:02d} {decminute:02d} {decsec:0.2f}')
    beam.append(f'{row.bmaj:0.2f}'+r'$\arcsec$')
    intgtimes.append(header['INTGTIME']/3600)
    
#     print(f'{rahour:02d}h {raminute:02d}m {rasec:0.2f}s',
#           f'{dechour:02d}h {de    print(sigma_tb_kelvin)cminute:02d}m {decsec:0.2f}s',
#          row['source'])

# data={'Galaxy':galaxies, 'R.A.':f'{rahour:02d}h {raminute:02d}m {rasec:0.2f}s', 
#       'Decl.':f'{dechour:02d}h {decminute:02d}m {decsec:0.2f}s', 
#       'Synthesized Beam':beamfile['bmaj']}

sigma_tbs=[]
noises=[]

for index,row in beamfile.iterrows():
    hdu=fits.open(row['jyfile'])
    data0, data1, header = hdu[0].data, hdu[1].data, hdu[0].header
    a_beam_arcsec=2*np.pi*((row['bmaj']*u.arcsec/(np.sqrt(8*np.log(2))))**2)
    a_beam_deg=a_beam_arcsec.to(u.degree**2)
    a_pix=(np.abs(header['CDELT1']))**2 #CDELT1 keyword is in units of degree / pixel
    rms_final=row['noise']/np.sqrt(a_beam_deg/a_pix) #take ratio, both in degrees squared
#     print(rms_final)
#     omega= 2*np.pi*(row['bmaj']*u.arcsec.to(u.radian))**2 #solid angle of beam 
#     sigma_tb_kelvin=((0.1)**2*(row['noise'])*10**(-26))/ (2*(k_B)*omega) #final brightness temp sensitivity
#     sigma_tb_mk=(sigma_tb_kelvin.value*10**3)
    sigma_tb_mk=(1216*((rms_final)*10**6))/(row['bmaj']*row['bmin']*(90)**2)
    sigma_tb_mk=round(sigma_tb_mk.value,2)
#     print(sigma_tb_mk)
    sigma_tbs.append(sigma_tb_mk)
    noises.append(round(rms_final.value*10**6,2))

data={'Galaxy':galaxies_final, 'R.A.':ras, 'Decl.':decs, 'Synthesized Beam':beam,
     'Point-source sensitivity (microJy/bm)':noises,
      'Brightness temperature sensitivity (mK)':(sigma_tbs)}

# print(np.average(beamfile['noise']*1e6))

ascii.write(data, format="latex")
