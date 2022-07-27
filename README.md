# eyegaze_analysis

This is code for doing the eyegaze analysis.

## eyegaze task
Need to automate the running of the following command line across multiple 
cases.

```
3dfim+ -input /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-803/ses-1503/func/sub-803_ses-1503_task-eyegazeall_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz 
-nfirst 4 
-ideal_file /home/share/eyegaze_BIDS/Derivs/fmriprep/timeseries/CondBandC_SHIFTandSMOOTH.1D 
-ort_file /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-803/ses-1503/func/sub-803_ses-1503_task-eyegazeall_run-1_regressors.1D 
-out Correlation 
-bucket  /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-803/ses-1503/func/sub-803_ses-1503_task-eyegazeall_CondBandC_CorrReg.nii.gz

```

## to run
```

./run3dfim.py --main /home/share/eyegaze_BIDS/Derivs/fmriprep --start 1
```

## causal analysis - extract Tso rois, perform CDA to determine causal relationships

```bash3dmaskave -mask /home/share/eyegaze_BIDS/Derivs/fmriprep/scripts/ROI_Tso/masks_3mm/TsoROI_Left_IPL_3mm.nii.gz -quiet /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-835/ses-1535/func/sub-835_ses-1535_task-eyegazeall_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz > /home/share/eyegaze_BIDS/Derivs/fmriprep/ROI_timeseries_output/Left_IPL.txt


# to change permission to group fmri for directory tree
sudo chgrp -R fmri * 
```

Tso ROIs will be in this folder
```
/home/share/eyegaze_BIDS/Derivs/fmriprep/scripts/ROI_Tso/masks_3mm

TsoROI_Left_IPL_3mm.nii.gz  TsoROI_Left_pMFC_3mm.nii.gz  TsoROI_Left_pSTS_3mm.nii.gz  TsoROI_Left_Visual_3mm.nii.gz  TsoROI_Right_IPL_3mm.nii.gz  TsoROI_Right_pMFC_3mm.nii.gz  TsoROI_Right_pSTS_3mm.nii.gz  TsoROI_Right_Visual_3mm.nii.gz

```

Need to loop for each subject, each scan, each roi

## Processing of rois and then cda analysis

```
# extract the Tso rois and place in the dataorig directory
# this took about 90 minutes for 94 cases
./extractroi.py 

# standardize the data columns, new files are placed in data directory
./stddata.py --diag

# run the fges with lr
./causalwrap_lr.py 

# run the sem
./sem_multi.py 
```
## Want to look at data under 5 conditions

1. Condition A - 0 deg
2. Condition B - 10 deg
3. Condition C - 30 deg
4. Condition D - shapes
5. Condition E - all

Filenames are in form of:
```
*eyegazeall_run_cX.csv
```
Where X is the condition.

Steps:

1. Extract out conditions from rawdata in dataorig. This has the 8 rois but with no std.

    parse4cond.py

    Needs to take the raw data from dataorig
    and parse the conditions out (time) and write back into dataorig (since not yet std)

2. Standardize the data from dataorig and write into the data directory

    stddata.py

3. Run  causalwrap_lr.py - run the fges with likelihood-ratio

    ```
    ./causalwrap_lr.py 
    ```
4. run the sem

    The tee is used to save the files which failed due to No model available.
    ```
    ./sem_multi.py | tee 20220718_semlog.txt
    ```
   


5. Transfer the sem data to the dganalysis_fmri proj_eyegaze/semdata

    ```
    cp output/*semopy.csv ../dganalysis_fmri/proj_eyegaze/semdata
    ```

6. run roi regional connectivity analysis in the dganalysis_fmri folder

    ```
    ./dganalysis.py --proj eyegaze --cmd rcon
    ```

## Quantifying the connections

These are the ROIS

1. Left_IPL
2. Left_Visual
3. Left_pMFC
4. Left_pSTS
5. Right_IPL
6. Right_Visual
7. Right_pMFC
8. Right_pSTS

Tso et al. 2021 only seem to use the Right side

1. Right_IPL
2. Right_Visual
3. Right_pMFC
4. Right_pSTS

So we have the a total of 12 different directed edges for these 4 regions


