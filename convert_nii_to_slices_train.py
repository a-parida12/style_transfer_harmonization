#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 19:43:12 2020

@author: bigting84
"""
import numpy as np
import nibabel as nib
import os
import matplotlib
import argparse
import matplotlib.pyplot as plt
import glob
from tqdm import tqdm

def slicer(data_files, save_path, ds=''):
    id = 0
    thr = 0.1

    for f in tqdm(sorted(data_files)):
    
        img = nib.load(f)
        
        a = img.get_fdata()
        a[np.where(a<0)] = 0
        
        for s in range(1, a.shape[2]-1):
            
            b = a[:, :, s]/a.max()
            b = b[..., np.newaxis]
            bn = a[:, :, s-1]/a.max()
            bn = bn[..., np.newaxis]
            bp = a[:, :, s+1]/a.max()
            bp = bp[..., np.newaxis]
            
            if b.sum() > thr and bp.sum() > thr and bn.sum() > thr:

                c = np.concatenate((bn,b,bp), axis=2)
                savename = save_path + ds +str(id).zfill(9) + '.png'#str(id).zfill(6) + '.png' 
                matplotlib.image.imsave(savename, c)
            id += 1
        
        for s in range(1, a.shape[1]-1):
            
            b = a[:, s, :]/a.max()
            b = b.squeeze()
            b = b[..., np.newaxis]
            bn = a[:, s-1, :]/a.max()
            bn = bn.squeeze()
            bn = bn[..., np.newaxis]
            bp = a[:, s+1, :]/a.max()
            bp = bp.squeeze()
            bp = bp[..., np.newaxis]
            
            if b.sum() > thr and bp.sum() > thr and bn.sum() > thr:

                c = np.concatenate((bn,b,bp), axis=2)
                savename = save_path + ds+ str(id).zfill(9) + '.png'#str(id).zfill(6) + '.png' 
                matplotlib.image.imsave(savename, c)
            id += 1
       
        for s in range(1, a.shape[0]-1):
            
            b = a[s, :, :]/a.max()
            b = b.squeeze()
            b = b[..., np.newaxis]
            bn = a[s-1, :, :]/a.max()
            bn = bn.squeeze()
            bn = bn[..., np.newaxis]
            bp = a[s+1, :, :]/a.max()
            bp = bp.squeeze()
            bp = bp[..., np.newaxis]
            
            if b.sum() > thr and bp.sum() > thr and bn.sum() > thr:

                c = np.concatenate((bn,b,bp), axis=2)
                savename = save_path + ds + str(id).zfill(9) + '.png'#str(id).zfill(6) + '.png' 
                matplotlib.image.imsave(savename, c)
            id += 1

parser = argparse.ArgumentParser()

# model arguments
parser.add_argument('--load_path', type=str, default='test',
                    help='file path where the npy file from the 3 orientations of harmonization files were located')
parser.add_argument('--save_path', type=str, default='test',
                    help='file path where the outputs are saved')

args = parser.parse_args()


save_path_train = args.save_path + '/train/'
save_path_val = args.save_path + '/val/'
os.makedirs(save_path_train, exist_ok=True)
os.makedirs(save_path_val, exist_ok=True)

search_parameter = os.path.join(args.load_path, '**/*.nii.gz')
data_files = sorted([file for file in glob.glob(search_parameter, recursive=True) if 't1' in file])


slicer(data_files[:int(0.8*len(data_files))], save_path_train, args.load_path.split('/')[-1])
slicer(data_files[int(0.8*len(data_files)):], save_path_val, args.load_path.split('/')[-1])


    
    
