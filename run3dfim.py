#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 18:24:11 2021

@author: kelvin
"""
import os
import glob
import argparse

class Run3dfim:
    def __init__(self,
                 maindir='/home/share/eyegaze_BIDS/Derivs/fmriprep',
                 test=True,
                 index = [0,None]
                 ):

        self.maindir = maindir
        self.test = test
        self.index = index

        # get list of files
        hint ="*task-eyegazeall*regress*.1D"
        self.onedfiles = self.getfiles(str = hint)
        hint = "*task-eyegazeall*preproc_bold*.gz"
        self.preproc_files = self.getfiles(str=hint)

        # run the commands
        self.run_cmds()

        pass

    def run_cmds(self):
        # run the commands
        conditions = ['CondA', 'CondB', 'CondC', 'CondBandC','CondBvsA','CondCvsA']

        # use the regressor file to derive the sub and ses
        for file in self.onedfiles[self.index[0]: self.index[1]]:
            # get the sub and ses from the 1d file name
            subt, sest = os.path.basename(file).split('_')[0:2]
            sub = subt.split('-')[1]
            ses = sest.split('-')[1]
            
            # loop for conditions
            for condition in conditions:
                cmd = self.create_3dfim_cmd(self.maindir,
                                            sub, ses,
                                            condition)
                print(cmd)
                if not self.test:
                    # run command
                    try:
                        os.system(cmd)
                    except:
                        print("An exception occured")


    def create_3dfim_cmd(self, maindir, sub, ses, condition ):
        cmd  = "3dfim+ -input "
        cmd += f"{maindir}/sub-{sub}/ses-{ses}/func/"
        cmd += f"sub-{sub}_ses-{ses}_task-eyegazeall_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz "
        cmd += "-nfirst 4 -ideal_file "
        cmd += f"{maindir}/timeseries/{condition}_SHIFTandSMOOTH.1D "
        cmd += "-ort_file "
        cmd += f"{maindir}/sub-{sub}/ses-{ses}/func/sub-{sub}_ses-{ses}_task-eyegazeall_run-1_regressors.1D "
        cmd += "-out Correlation "
        cmd += "-bucket "
        cmd += f"{maindir}/sub-{sub}/ses-{ses}/func/sub-{sub}_ses-{ses}_task-eyegazeall_{condition}_CorrReg.nii.gz"

        return cmd

    def getfiles(self,str="*task-eyegazeall*regress*.1D"):
        # return list of file matching the str
        
        files = glob.glob(os.path.join(
            self.maindir,'**', str), recursive=True)
        files.sort()

        return files

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description = "Creates and runs the 3dfim command for the \
            eyegaze task."
    )
    parser.add_argument("--start", type = int,
                        help="beginning file list index , default 0",
                        default = 0)
    parser.add_argument("--end", type = str,
                        help="end file list index, default None",
                        default=None)
    parser.add_argument("--main", type = str,
                        help="The main directory location, typically \
                        this is the Derivs/fmriprep directory",
                        default='/home/share/eyegaze_BIDS/Derivs/fmriprep')
    parser.add_argument("--list", help="TODO list the files to be processed",
                        action = "store_true")
    parser.add_argument("--test", help="create the cmd but don't execute",
        action = "store_true", default = False)
    args = parser.parse_args()

    # setup default values
    if args.end != None:
        args.end = int(args.end)
    
    c = Run3dfim(index = [args.start, args.end],
                 maindir = args.main,
                 test =args.test)
