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

#  add cwd to beginning of path to insure import is from current directory
sys.path.insert(0, os.getcwd())
import dicomlist

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