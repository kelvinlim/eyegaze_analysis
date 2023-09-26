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
                 index = [0,None],
                 cmd = '3dfim',
                 list = False,
                 singledir=False
        ):

        self.maindir = maindir
        self.test = test
        self.index = index
        self.list = list
        self.cmd = cmd
        self.singledir = singledir

        # get list of files
        hint ="*task-eyegazeall*regress*.1D"
        self.onedfiles = self.getfiles(hint = hint)
        hint = "*task-eyegazeall*preproc_bold*.gz"
        self.preproc_files = self.getfiles(hint=hint)

        if self.list:
            count=0
            total = len(self.onedfiles)
            for item in self.onedfiles:
                print(f"{count}/{total} {os.path.basename(item)}")
                count += 1
                
            count=0
            total = len(self.preproc_files)
            for item in self.preproc_files:
                print(f"{count}/{total} {os.path.basename(item)}")
                count += 1                
                
            exit(0)
            
        # run the commands
        
        if self.cmd == '3dfim':
            self.run_cmds()
        elif self.cmd == '3dvolreg':
            self.run_3dvolreg()
        else:
            print(f"Command {self.cmd} not found.")
        pass

    def run_3dvolreg(self):
        """
        Run 3dvolreg for the nifti files
        
        3dvolreg -dfile sub-800_ses-1500_task-eyegazeall_run-1_regressors.1D sub-800_ses-1500_task-eyegazeall_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz
        
        last one sub-858_ses-1558_task-eyegazeall_run-1_regressors.1D, then stuck
        
        """

        for filepath in self.preproc_files[self.index[0]: self.index[1]]:
            dirname = os.path.dirname(filepath)
            basename = os.path.basename(filepath)
            base = basename.split(',')[0]
            
            # build the name of the 1D file for the dfile argument
            tailend = '_task-eyegazeall_run-1_regressors.1D'
            parts = basename.split('_')[0:2]  # get first two
            frontend = "_".join(parts)
            dfilename = frontend + tailend
            
            cmd  = "3dvolreg "
            cmd += "-dfile "
            cmd += f"{os.path.join(dirname, dfilename)} "
            cmd += filepath
            
            print(cmd)
            
            if not self.test:
                # run command
                try:
                    os.system(cmd)
                except:
                    print("An exception occurred")
            pass
                    
        # use the regressor file to derive the sub and ses

        pass

    def run_cmds(self):
        # run the commands
        conditions = ['CondA', 'CondB', 'CondC', 'CondBandC','CondBvsA','CondCvsA','CondBvsC']

        file_count = 0
        total = len(self.onedfiles)
        # use the regressor file to derive the sub and ses
        for file in self.onedfiles[self.index[0]: self.index[1]]:
            # get the sub and ses from the 1d file name
            subt, sest = os.path.basename(file).split('_')[0:2]
            sub = subt.split('-')[1]
            ses = sest.split('-')[1]
            
            print(f"FileCount: {file_count}/{total}")
                     
            # loop for conditions
            for condition in conditions:
                
                if self.singledir:
                    cmd = self.create_3dfim_single_directory_cmd(self.maindir,
                                                sub, ses,
                                                condition)
                else:
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
            file_count += 1

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

    def create_3dfim_single_directory_cmd(self, maindir, sub, ses, condition ):
        cmd  = "3dfim+ -input "
        cmd += f"{maindir}/"
        cmd += f"sub-{sub}_ses-{ses}_task-eyegazeall_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz "
        cmd += "-nfirst 4 -ideal_file "
        cmd += f"{maindir}/timeseries/{condition}_SHIFTandSMOOTH.1D "
        cmd += "-ort_file "
        cmd += f"{maindir}/sub-{sub}_ses-{ses}_task-eyegazeall_run-1_regressors.1D "
        cmd += "-out Correlation "
        cmd += "-bucket "
        cmd += f"{maindir}/sub-{sub}_ses-{ses}_task-eyegazeall_{condition}_CorrReg.nii.gz"

        return cmd
    
    def getfiles(self,hint="*task-eyegazeall*regress*.1D"):
        # return list of file matching the str
        
        files = glob.glob(os.path.join(
            self.maindir,'**', hint), recursive=True)
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
    parser.add_argument("--cmd", type = str,
                        help="Command to execute [3dfim, 3dregvol ] default 3dfim \
                        ",
                        default='3dfim')
    parser.add_argument("--list", help="list the files to be processed",
                        action = "store_true")
    parser.add_argument("--singledir", help="flat for single directory, default false",
                        action = "store_true", default=False)
    parser.add_argument("--test", help="create the cmd but don't execute",
                        action = "store_true", default = False)
    args = parser.parse_args()

    # setup default values
    if args.end != None:
        args.end = int(args.end)
    
    test = False
    
    if test:
        c = Run3dfim(index = [args.start, args.end],
                    maindir = '/home/limko/shared/eyegaze_corr',  # args.main,
                    test =args.test,
                    list = True,
                    cmd = '3dvolreg',
                    singledir=True
            )
    else:
        c = Run3dfim(index = [args.start, args.end],
                maindir = args.main,
                test =args.test,
                list = args.list,
                cmd = args.cmd,
                singledir = args.singledir
            )
