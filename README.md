# eyegaze_analysis

This is code for doing the eyegaze analysis.

## eyegaze task
Need to autoamate the running of the following command line across multiple 
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

