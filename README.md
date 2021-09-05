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


