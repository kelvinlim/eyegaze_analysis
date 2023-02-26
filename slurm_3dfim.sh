#!/bin/bash
#SBATCH --job-name=eg_3dfim
#SBATCH --time=10:00:00
#SBATCH --array=3-105    # number of jobs

# SLURM_ARRAY_TASK_ID

# load python 3.8
module load python3
# load afni
module load afni

# subtract 1 from SLURM_ARRAY_TASK_ID
let BEG=$SLURM_ARRAY_TASK_ID-1
let END=$BEG+1
DIR=/scratch.global/eyegaze_corr
./run3dfim.py --main $DIR --start $BEG --end $END --cmd 3dvolreg --singledir
./run3dfim.py --main $DIR --start $BEG --end $END --cmd 3dfim --singledir

# to run $ sbatch <scriptname>.sh
# to check status $ squeue --me