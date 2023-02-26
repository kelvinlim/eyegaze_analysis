#! /usr/bin/env python3

"""
Find the missing cases
"""

import os
import argparse
import glob

class FindMissing:
    
    def __init__(self, maindir=''):
        self.maindir = maindir
        pass
    
    def getfiles(self,hint="*task-eyegazeall*regress*.1D"):
    # return list of file matching the str
    
        files = glob.glob(os.path.join(
            self.maindir,'**', hint), recursive=True)
        files.sort()

        return files
    
def main():

    maindir = '/scratch.global/eyegaze_corr'

    c = FindMissing(maindir=maindir)
    

    # get the 1D files
    files = c.getfiles()
    
    for file in files:
        # get the sub and ses from the 1d file name
        subt, sest = os.path.basename(file).split('_')[0:2]
        sub = subt.split('-')[1]
        ses = sest.split('-')[1]
        
        checkfile = f"sub-{sub}_ses-{ses}_task-eyegazeall_CondA_CorrReg.nii.gz"
        
        filefound = glob.glob(os.path.join(
            maindir,'**', checkfile), recursive=True)
        
        if not filefound:
            print(f"CondA not found for {checkfile}")
        pass

    
if __name__ == "__main__":
    main()

