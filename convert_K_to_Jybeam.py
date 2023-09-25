# Converts GBT fits from Kelvin to Jy/beam
# Also adds beam info to header

#import statements
from astropy.io import fits
from astropy import units as u
import pandas as pd

def kelvintoJybeam(file_name, outfilename, beamfile):

    # Opening fits file
    hdu=fits.open(file_name)
    
    # Opening beam info file
    beam_file=pd.read_csv(beamfile)
    
    # Extracting source ID from file name (subject to change!)
    filename_split=file_name.split('/')
    source_id=filename_split[6]
    
    # Picking out beam info based on source ID
    beam_filt=beam_file.loc[beam_file['source'] == source_id]
    # Converting beam info from arcseconds to degrees
    bmaj=(beam_filt['bmaj'].values * u.arcsec).to(u.deg)
    bmin=(beam_filt['bmin'].values * u.arcsec).to(u.deg)
    bmaj=bmaj/u.deg
    bmin=bmin/u.deg

    # Calling data (science image, weight image) and header
    data0, data1, header = hdu[0].data, hdu[1].data, hdu[0].header
    # data0 == science image
    # data1 == weight image

    # Reading parameters from the header
    antgain= float(header['ANTGAIN'])

    # Updating parameters in the header
    header['UNITS']=str('Jy/beam')
    
    # Adding beam info to header
    header['BMAJ']=(float(bmaj),'Length of beam major axis (degrees)')
    header['BMIN']=(float(bmin),'Length of beam minor axis (degrees)')
    header['BPA']=(0.0,'Beam position angle (degrees)')

    # Creating new fits image in Jy/beam units after dividing ANTGAIN per the pixel values in Kelvin
    #new_hdu=fits.PrimaryHDU(header=header, data=[data0/antgain, data1])
    new_hdu=fits.PrimaryHDU(header=header,data=[data0/antgain])
    wtmap_hdu=fits.ImageHDU(header=hdu[1].header,data=data1,name='wtmap')
    new_hdul=fits.HDUList([new_hdu,wtmap_hdu])
    # Write file, outputfilename should include the path
    outfile=new_hdu.writeto(outfilename,overwrite=True)
    return outfile

# Run file as a script to make fits files
# List of fits files that need to be converted, filenames need to have the full path!
### CHANGE THIS LIST AS NEEDED
galaxy_maps = ['/lustre/cv/students/adignan/data/NGC0337/Kelvin_NGC0337_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_M_PdoCals_dt20_m$
'/lustre/cv/students/adignan/data/NGC0628/Kelvin_NGC0628_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_L_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC0925/Kelvin_NGC0925_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_L_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC2146/Kelvin_NGC2146_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC2798/Kelvin_NGC2798_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC2841/Kelvin_NGC2841_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_L_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC3049/Kelvin_NGC3049_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC3184/Kelvin_NGC3184_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC3190/Kelvin_NGC3190_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC3198/Kelvin_NGC3198_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_L_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC3351/Kelvin_NGC3351_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC3521/Kelvin_NGC3521_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_L_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC3627/Kelvin_NGC3627_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_L_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC3773/Kelvin_NGC3773_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_L_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC3938/Kelvin_NGC3938_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC6946/Kelvin_NGC6946_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits',
'/lustre/cv/students/adignan/data/NGC7331/Kelvin_NGC7331_2asp_pca6_qm2_fitel_0f09-to-41f0Hz_qc_1p2rr_L_PdoCals_dt20_map_iter1.fits'
]

# Generate list of output file names 
output_maps = [galaxy_maps[i].replace('Kelvin', 'Jyperbeam') for i in range(len(galaxy_maps))]
# make the fits! 
# load in csv file with beam info to add to header
beamfile='/lustre/cv/students/adignan/beam_info.csv'

for i in range(len(galaxy_maps)):
    kelvintoJybeam(galaxy_maps[i],output_maps[i],beamfile)
