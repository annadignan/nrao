#import statement
from astropy.io import ascii

#read in table with source ID, frequency, RA and Dec, and radius info
table=ascii.read('/users/adignan/NEW_photometry_results.csv',format='csv')

#loop through each row in the table
for row in table:
    
    #create a file for each source at each of our four frequencies
    f=open('/users/adignan/regfiles/new/'+str(row['source ID']) + '_' + str(row['freq (GHz)'])+'GHz.reg',"w")
    #write header for file based on region file convention
    f.write('global color=red dashlist=8 3 width=3 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1 \n')
    #write out info for our aperture and annuli
    f.write(
        'circle'+' '+str(row['RA (deg)']) + ' ' + str(row['Dec (deg)'])+' '+str(row['radius (arcsec)']) +'"' 
        + ' #color=white' + '\n' 
        + 'circle'+' '+ str(row['RA (deg)']) + ' ' + str(row['Dec (deg)']) + ' ' + str(1.5*row['radius (arcsec)']) +'"' 
        + '\n' 
        + 'circle'+ ' ' + str(row['RA (deg)']) + ' ' + str(row['Dec (deg)']) + ' ' + str(1.5*row['radius (arcsec)'] + row['radius (arcsec)']) +'"') 
    #close file
    f.close()