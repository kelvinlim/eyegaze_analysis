#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 12:26:31 2021

@author: kelvin
"""

import os
import sys
import pandas as pd

maindir='/home/share/eyegaze_BIDS/Derivs/fmriprep'
fpath = os.path.join(maindir, 'dicomlist.py')

def summarize(list):
    # summarize the data
    df = pd.DataFrame(list, columns=['dir','sub','ses'])
    # change order of columns
    df = df[['sub','ses','dir']]
    # create a group column
    grp = []
    
    for item in list:
        dir = item[0]
        
        for gp in ['ARM','PT','NC','SB']:
            if gp in dir:
                grp.append(gp)
    
    # add column to df
    df['grp'] = grp
    
    # sort by sub and ses
    df.sort_values(by=['sub','ses'], inplace=True)
    
    df = df[['sub','ses','grp','dir']]

    # write out data
    df.to_csv('eg_sub_summary.csv', index=False)
    pass 


#  add cwd to beginning of path to insure import is from current directory
sys.path.insert(0, os.getcwd())
import dicomlist

summarize(dicomlist.datasets)

# create list of the PT and NC
info = {}
info['PT'] = {}
info['NC'] = {}
sublist = {}

for grp in ['PT', 'NC']:
    for item in dicomlist.datasets:
        if grp in item[0]:
            # add the case 
            info[grp][item[1]] = item[0]
            
            sublist[item[1]] = grp


#df = pd.DataFrame(sublist)
# print all subjects in order
ids = list(sublist.keys())
ids.sort()
print('id',',','grp', sep='')
for id in ids:
    print(id, ',',sublist[id], sep='')    
        
pass 