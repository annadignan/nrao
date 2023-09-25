###PURPOSE: run imregrid on all of the VLA data

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
path = '/lustre/cv/students/adignan/data/'

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
        if 'ngc' in f:
            smoothed_files.append(f)
    #collecting the Jansky per beam files that imregrid uses as templates
        if 'Jyperbeam' in f:
            if f not in jy_files:
                jy_files.append(f)
        if 'NGC4' in f:
            if  'Jy' in f and f.endswith('dt20_map_iter1.fits'):
                if f not in jy_files:
                    jy_files.append(f)
                    
#duplicates are 4254 and 4725
#use 07 for 4254 because that's what we have snr_iter1.fits for (and it looks okay)
#using same logic for 4725
#so remove 08 versions from list of files
jy_files.remove('Jy_NGC4725_2asp_pca6_qm2_fitel_0f08-to-41f1Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits')
jy_files.remove('Jy_NGC4254_2asp_pca6_qm2_fitel_0f08-to-41f1Hz_qc_1p2rr_M_PdoCals_dt20_map_iter1.fits')

#########################################################
#create an astropy table so that for each source/folder,
#we have the corresponding Jansky per beam file, the
#smoothed files, and resolution matched files. This will
#come in handy when we call imregrid!
#########################################################

#initialize empty list
rows=[]

#loop through info we collected from os.walk and store it in lists
#that we will input as rows in our astropy table
for f,j in zip(folders,jy_files):
    #make sure folder and Jansky file are for same galaxy!
    assert f[3:] in j, 'source and jansky file do not match'
    #initialize empty lists
    temprow=[]
    temprow3=[]
    for s in smoothed_files:
        if f[3:] in s:
            #smoothed files
            temprow1=s
            #resolution matched files
            temprow2=s.replace('.fits','')+'.gbt_resmatched'
            temprow.append(temprow1)
            temprow3.append(temprow2)
    #sources/folders, Jansky files, smoothed files, resmatched files
    rows.append([f,j,temprow,temprow3])

#naming our table "tbl"
tbl=Table(rows=rows,names=['source','jansky','smoothed','resmatched'])

#########################################################
#run imregrid!!!
######################################################### 

#iterate through the rows in our table to run imregrid on
#each of the correct files per source
for i,j,k in tbl.iterrows('source','resmatched','jansky'):
    #iterate over each file in resmatched (since it's a list of files)
    for value in j:
        #making save name for importfits
        save1=k.replace('.fits','.image')
        #making save name for imregrid
        save2=value.replace('.fits','')+'_regridded'
        #opening the Jansky fits files as CASA image files for imregrid
        importfits(fitsimage=path + str(i) + '/' + str(k),imagename=path + str(i) + '/' + str(save1),overwrite=True)
        #finally running imregrid
        imregrid(imagename=path + str(i) + '/' + str(value),template=path + str(i) + '/' + str(save1),output=path + str(i) + '/' + str(save2),overwrite=True)