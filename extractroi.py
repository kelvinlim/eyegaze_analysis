#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 18:24:11 2021

@author: kelvin
"""
import os
import glob
import argparse
import tempfile
import pandas as pd

class ExtractROI:
    def __init__(self,
                 maindir='/home/share/eyegaze_BIDS/Derivs/fmriprep',
                 dryrun=True,
                 index = [0,None],
                 list=False,
                 ):

        self.maindir = maindir
        self.dryrun = dryrun
        self.index = index
        self.list = list
        self.roidir = '/home/share/eyegaze_BIDS/Derivs/fmriprep/scripts/ROI_Tso/masks_3mm'

        # output directory where roi csv files are stored
        self.outdir = 'dataorig'
        # make the output data directory
        os.makedirs( self.outdir, exist_ok=True)


        # get list of processed files
        hint = "*task-eyegazeall*preproc_bold*.gz"
        self.preproc_files = self.getfiles(maindir, str=hint)

        # get list of roi files
        hint = "*_3mm.nii.gz"
        self.roi_files = self.getfiles(self.roidir, str=hint)


        if self.list:
            i = 0
            for file in self.preproc_files:
                print(f"{i}: {file}")
                i += 1
            i = 0
            for file in self.roi_files:
                print(f"{i}: {file}")
                i += 1
            exit()

        # run the commands
        self.run_cmds()

        pass

    def run_cmds(self):
        # run the commands

        # use the preproc file to derive the sub and ses
        for file in self.preproc_files[self.index[0]: self.index[1]]:
            # get the sub and ses from the 1d file name
            subt, sest = os.path.basename(file).split('_')[0:2]
            sub = subt.split('-')[1]
            ses = sest.split('-')[1]

            # get the base for the roi csv file
            roibase = os.path.basename(file).split('_run-1')[0]
            
            # create the tempdir
            temp_dir = tempfile.TemporaryDirectory()

            # loop for rois
            for roi_file in self.roi_files:

                bn = os.path.basename(roi_file).split('_')
                roi_name = f"{bn[1]}_{bn[2]}"
                tmpfile = os.path.join(temp_dir.name, roi_name+'.txt')

                cmd = self.create_3dmaskave_cmd(self.maindir, 
                        sub, ses, 
                        roi_file, 
                        tmpfile )
    
                print(cmd)
                if not self.dryrun:
                    # run command
                    try:
                        os.system(cmd)
                    except:
                        print("An exception occured")

            # combine the temporary txt files into a csv with header
            self.create_roi_csv(temp_dir.name, roibase)
            # delete the tempdir
            temp_dir.cleanup()
            pass

    def create_roi_csv(self, temp_dir, roibase):
        "Create a csv file from the temporary output files"

        # get the filename 
        # get list of roi files
        hint = "*.txt"
        roifiles = self.getfiles(temp_dir, str=hint)

        data = {}
        # read in each roifile
        for roifile in roifiles:
            roi_name = os.path.basename(roifile).split('.txt')[0]
            with open(roifile) as fp:
                # read into a list of floats and place in dict
                data[roi_name] = [float(x) for x in fp.read().splitlines()]

        # create the dataframe
        df = pd.DataFrame(data)
        # write it to csv file
        outpath = os.path.join(self.outdir, roibase + '.csv')
        df.to_csv(outpath, index=False)

        pass

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


    def create_3dmaskave_cmd(self, maindir, sub, ses, roi, tmpfile ):
        """
        3dmaskave -mask /home/share/eyegaze_BIDS/Derivs/fmriprep/scripts/ROI_Tso/masks_3mm/TsoROI_Left_IPL_3mm.nii.gz -quiet /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-835/ses-1535/func/sub-835_ses-1535_task-eyegazeall_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz > /home/share/eyegaze_BIDS/Derivs/fmriprep/ROI_timeseries_output/Left_IPL.txt
        
        """
        cmd  = "3dmaskave -mask "
        cmd += f"{roi}"
        cmd += " -quiet "
        cmd += f"{maindir}/sub-{sub}/ses-{ses}/func/"
        cmd += f"sub-{sub}_ses-{ses}_task-eyegazeall_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz "
        cmd += " > "
        cmd += f"{tmpfile}"

        return cmd

    def getfiles(self, maindir, str="*task-eyegazeall*regress*.1D"):
        # return list of file matching the str
        
        files = glob.glob(os.path.join(
            maindir,'**', str), recursive=True)
        files.sort()

        return files

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description = "Creates and runs the 3dmaskave command for the \
            eyegaze task. Places data into dataorig directory."
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
    parser.add_argument("--list", help="list the files to be processed",
                        action = "store_true")
    parser.add_argument("--dryrun", help="create the cmd but don't execute",
        action = "store_true", default = False)    
    parser.add_argument("--test", help="create the cmd but don't execute",
        action = "store_true", default = False)
    args = parser.parse_args()

    # setup default values
    if args.end != None:
        args.end = int(args.end)
    
    if args.test:
        c = ExtractROI(index = [args.start, 1],
                    maindir = args.main,
                    dryrun =args.dryrun,
                    list = args.list,
                    )
    else:
        c = ExtractROI(index = [args.start, args.end],
                 maindir = args.main,
                 dryrun =args.dryrun,
                 list = args.list,
                 )