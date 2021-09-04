# code for creating the full command to be executed

"""
to find files

find . -name "*task-eyegazeall[kelvin@x-192-168-1-20 fmriprep]$ find . -name "*task-eyegazeall*preproc_bold*.gz" | wc
     94      94   10716*preproc_bold*.gz"

find . -name "*task-eyegazeall*regress*.1D" | wc
     84      84    6450


"""

import difflib as dl # use t o show difference in strings


def create_3dfim_cmd(maindir, sub, ses, condition ):
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

orig="3dfim+ -input /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-803/ses-1503/func/sub-803_ses-1503_task-eyegazeall_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz -nfirst 4 -ideal_file /home/share/eyegaze_BIDS/Derivs/fmriprep/timeseries/CondBandC_SHIFTandSMOOTH.1D -ort_file /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-803/ses-1503/func/sub-803_ses-1503_task-eyegazeall_run-1_regressors.1D -out Correlation -bucket /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-803/ses-1503/func/sub-803_ses-1503_task-eyegazeall_CondBandC_CorrReg.nii.gz"

"""
3dfim+ -input /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-803/ses-1503/func/sub-803_ses-1503_task_eyegazeall_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz  -nfirst 4 -ideal_file /home/share/eyegaze_BIDS/Derivs/fmriprep/timeseries/CondBandC_SHIFTandSMOOTH.1D -ort_file /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-803/ses-1503/func/sub-803_ses-1503_task-eyegazeall_run-1_regressors.1D -out Correlation -bucket f(maindir}/sub-{sub}/ses-{ses}/func/sub-{sub}_ses-{ses}_task-eyegazeall_CondBandC_CorrReg.nii.gz
"""
sub=803
ses=1503
condition="CondBandC"
maindir="/home/share/eyegaze_BIDS/Derivs/fmriprep"

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

#print(cmd)

# compare with orig and str creation
for diff in dl.context_diff(orig, cmd):
    print(diff)

print("String Match: ",(orig==cmd))

# compare with orig and function creation
cmd = create_3dfim_cmd(maindir, sub, ses, condition )
for diff in dl.context_diff(orig, cmd):
    print(diff)

print("Function Match: ",(orig==cmd))

pass
