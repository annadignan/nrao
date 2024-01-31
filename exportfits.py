###PURPOSE: convert CASA image files to fits files for analysis and plotting

#make an astropy table with all of the correct and relevant file names for each source

#########################################################
#create two lists:
#(1) all of the files we want to run imregrid on and 
#(2) all of the directories containing the files from (1)
#########################################################

#import statements
import os
from pathlib import Path
from astropy.table import Table
import astropy
import glob

#change path to where the data is
path = '/lustre/cv/students/adignan/data/new/'

#ignore the misc folder
exclude='misc'

#initialize empty lists
folders = []
smoothed_files = []
jy_files = []

for (root, dirs, file) in os.walk(path):
    #ignore the misc folder
    dirs[:] = [d for d in dirs if d not in exclude]
    #creating list (2)
    for f in dirs:
        if f.startswith('NGC'):
            # added this "not in" to avoid double counting a source due to a subdirectory
            if f not in folders:
                folders.append(f)
    #creating list (1)
    for f in file:
        if 'ngc' in f and f.endswith('smoothed_ms.fits'):
            smoothed_files.append(f)
    #collecting the Jansky per beam files that imregrid uses as templates
        if 'Jyperbeam' in f and f.endswith('dt20_map_iter1_editted.fits'):
            if f not in jy_files:
                jy_files.append(f)
    #comment out this part if you're running on "new" sources
#         if 'NGC4' in f:
#             if  'Jy' in f and f.endswith('dt20_map_iter1_editted.fits'):
#                 if f not in jy_files:
#                     jy_files.append(f)

#########################################################
#create an astropy table so that for each source/folder,
#we have the corresponding Jansky per beam file, the
#smoothed files, and resolution matched files
#########################################################

#initialize empty list
rows=[]

#loop through info we collected from os.walk and store it in lists
#that we will input as rows in our astropy table
for f,j in zip(folders,jy_files):
    #make sure folder and Jansky file are for same galaxy!
#     assert f[3:] in j, 'source and jansky file do not match'
    #initialize empty lists
    temprow=[]
    temprow3=[]
    temprow5=[]
    for s in smoothed_files:
        if f[3:] in s:
            #smoothed files
            temprow1=s
            #resolution matched files
            temprow2=s.replace('.fits','')+'.gbt_resmatched'
            temprow4=s.replace('.fits','')+'.gbt_resmatched_regridded'
            temprow.append(temprow1)
            temprow3.append(temprow2)
            temprow5.append(temprow4)
    #sources/folders, Jansky files, smoothed files, resmatched files
    rows.append([f,j,temprow,temprow3,temprow5])

#naming our table "tbl"
tbl=Table(rows=rows,names=['source','jansky','smoothed','resmatched','regridded'])

#iterate through the rows in our table to run exportfits on
#each of the correct files per source
for i,j in tbl.iterrows('source','regridded'):
    #iterate over each file in resmatched (since it's a list of files)
    for value in j:
        #making save name for exportfits
        savename=value+'.fits'
        #running CASA task exportfits on each file
        exportfits(imagename=path + str(i) + '/' + str(value),fitsimage=path + str(i) + '/' + str(savename),overwrite=True)