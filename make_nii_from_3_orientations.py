#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 19:43:12 2020

@author: bigting84
"""
import numpy as np
import nibabel as nib
import os
from os import listdir
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import argparse
import scipy.ndimage



parser = argparse.ArgumentParser()

# model arguments
parser.add_argument('--input_img', type=str, default='test',
                    help='Input image file, with file path')
parser.add_argument('--load_path', type=str, default='test',
                    help='file path where the npy file from the 3 orientations of harmonization files were located')
parser.add_argument('--save_path', type=str, default='test',
                    help='file path where the outputs are saved')
parser.add_argument('--is_src', type=bool, default=False,
                    help='determin whether the output is the harmonized image or the normalization of the src image')


args = parser.parse_args()
print(args)

input_img = args.input_img
save_path = args.save_path
save_path = save_path + '/'
load_path = args.load_path
load_path = load_path + '/'
is_src = args.is_src


#input_img = '/ifs/loni/faculty/hkim/mengting/harmonization/ADNI_55-65/nii_ds/116_S_4199_20120907_A2_T1_3T_accel_Preproc_ds.nii.gz'
#load_path = '/ifs/loni/faculty/hkim/mengting/harmonization/test/npy'
#save_path = load_path

(fpath, f) = os.path.split(input_img)
f1 = os.path.splitext(f)
f2 = os. path. splitext(f1[0])
ID = f2[0]
print(ID)

orient = ['axial', 'coronal', 'sagittal']

for ori in orient:

    print(ori)
    if is_src is False:
        a = np.load(load_path + '/' + ID + '_' + ori + '_harm.npy')
    else:
        a = np.load(load_path + '/' + ID + '_' + ori + '_src.npy')
    print(a.shape)

    nslice = a.shape[0] + 2
    nimg = np.zeros((nslice, 256, 256))
    for i in range(1, nslice-1):
        nimg[i-1:i+2, :, :] = nimg[i-1:i+2, :, :] + np.squeeze(a[i-1,:,:,:])
        #nimg[i, :, :] = a[i-1, 1, :, :]

    nimg[[1,nslice-2],:,:] = nimg[[1,nslice-2],:,:]/2;
    nimg[2:nslice-2,:,:] = nimg[2:nslice-2,:,:]/3;

    nimg_rs = nimg
    #newsize = (nslice,  nslice)
    #nimg_rs = np.zeros((nslice, nslice, nslice))
    #for i in range(0, nslice):
    #    nimg_rs[i, :, :] = cv2.resize(np.squeeze(nimg[i, :, :]), newsize, cv2.INTER_NEAREST)
    
    if ori == 'axial':
        oneimg = nimg_rs#np.moveaxis(nimg_rs, 0, -1)
        oneimg = scipy.ndimage.zoom(oneimg, np.array([256]*3)/np.array(oneimg.shape))
    elif ori == 'coronal':
        twoimg = np.moveaxis(nimg_rs, 0, 1)
        twoimg = scipy.ndimage.zoom(twoimg, np.array([256]*3)/np.array(twoimg.shape))
    else:
        threeimg = np.moveaxis(nimg_rs,0,-1)
        threeimg = scipy.ndimage.zoom(twoimg, np.array([256]*3)/np.array(twoimg.shape))
 
nimg = (oneimg + twoimg + threeimg)/3
nimg[nimg < -1] = -1
nimg[nimg > 1] = 1

inp = nib.load(input_img)
b = nib.Nifti1Image(nimg,inp.affine,inp.header)
if is_src is False:
    nib.save(b, save_path + '/' + ID + '_harm.nii.gz')
else:
    nib.save(b, save_path + '/' + ID + '_src.nii.gz')







