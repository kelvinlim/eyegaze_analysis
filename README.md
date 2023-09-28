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
./run3dfim.py --main /home/share/eyegaze_BIDS/Derivs/fmriprep --cmd 3dfim --start 0

# 20230928
./run3dfim.py --main /home/share/eyegaze_BIDS/Derivs/just_preproc --cmd 3dfim  --singledir


```
## to get the regress.1D files

preproc_bold.nii.gz files are in /home/share/eyegaze_BIDS/Derivs/just_preproc

```

```

## data at msi

S3 BUCKETS:

BIDS -     s3://lnpi-eyegaze-bids
FMRIPREP - s3://lnpi-eyegaze-derivs

In the event that fmriprep outputs are scrubbed from scratch, you can pull from the S3 bucket to /scratch.global. For example: 

```
mkdir /scratch.global/eyegaze_tmp
s3cmd get --force -r s3://lnpi-eyegaze-derivs/ /scratch.global/eyegaze_tmp
```

## causal analysis - extract Tso rois, perform CDA to determine causal relationships

```bash3dmaskave -mask /home/share/eyegaze_BIDS/Derivs/fmriprep/scripts/ROI_Tso/masks_3mm/TsoROI_Left_IPL_3mm.nii.gz -quiet /home/share/eyegaze_BIDS/Derivs/fmriprep/sub-835/ses-1535/func/sub-835_ses-1535_task-eyegazeall_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz > /home/share/eyegaze_BIDS/Derivs/fmriprep/ROI_timeseries_output/Left_IPL.txt


# to change permission to group fmri for directory tree
sudo chgrp -R fmri * 
```

Tso ROIs will be in this folder
```
~/Projects/eyegaze_analysis/ROI_Tso/masks_3mm

TsoROI_Left_IPL_3mm.nii.gz  TsoROI_Left_pMFC_3mm.nii.gz  TsoROI_Left_pSTS_3mm.nii.gz  TsoROI_Left_Visual_3mm.nii.gz  TsoROI_Right_IPL_3mm.nii.gz  TsoROI_Right_pMFC_3mm.nii.gz  TsoROI_Right_pSTS_3mm.nii.gz  TsoROI_Right_Visual_3mm.nii.gz

```

Need to loop for each subject, each scan, each roi

## Processing of rois and then cda analysis

```
# use rsync copy selected preproc files from msi to x0-28 via rsync
rsync -avzh kolim@login.msi.umn.edu:/home/limko/shared/eyegaze/Derivs/fmriprep/sub*/ses*/func/*gazeall*preproc*nii.gz .

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
    cp output/*[ABCDE]_semopy.csv ../dganalysis_fmri/proj_eyegaze/semdata
    ```

6. run roi regional connectivity analysis in the dganalysis_fmri folder

    ```
    # generate the roi file
    ./proj_eyegaze/create_roi_file.py
    # perform the regional connectivity analysis
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


## files after sep 2022

105, before 94
```

105 

kolim@ln0005 [/home/limko/shared/eyegaze/BIDS_output] % ls su*/se*/func/*eyegazeall*nii.gz
sub-800/ses-1500/func/sub-800_ses-1500_task-eyegazeall_run-01_bold.nii.gz
sub-801/ses-1501/func/sub-801_ses-1501_task-eyegazeall_run-01_bold.nii.gz
sub-801/ses-1502/func/sub-801_ses-1502_task-eyegazeall_run-01_bold.nii.gz
sub-803/ses-1503/func/sub-803_ses-1503_task-eyegazeall_run-01_bold.nii.gz
sub-803/ses-1504/func/sub-803_ses-1504_task-eyegazeall_run-01_bold.nii.gz
sub-805/ses-1505/func/sub-805_ses-1505_task-eyegazeall_run-01_bold.nii.gz
sub-805/ses-1551/func/sub-805_ses-1551_task-eyegazeall_run-01_bold.nii.gz
sub-806/ses-1506/func/sub-806_ses-1506_task-eyegazeall_run-01_bold.nii.gz
sub-807/ses-1507/func/sub-807_ses-1507_task-eyegazeall_run-01_bold.nii.gz
sub-810/ses-1510/func/sub-810_ses-1510_task-eyegazeall_run-01_bold.nii.gz
sub-810/ses-1511/func/sub-810_ses-1511_task-eyegazeall_run-01_bold.nii.gz
sub-812/ses-1512/func/sub-812_ses-1512_task-eyegazeall_run-01_bold.nii.gz
sub-813/ses-1513/func/sub-813_ses-1513_task-eyegazeall_run-01_bold.nii.gz
sub-814/ses-1514/func/sub-814_ses-1514_task-eyegazeall_run-01_bold.nii.gz
sub-815/ses-1515/func/sub-815_ses-1515_task-eyegazeall_run-01_bold.nii.gz
sub-816/ses-1516/func/sub-816_ses-1516_task-eyegazeall_run-01_bold.nii.gz
sub-817/ses-1517/func/sub-817_ses-1517_task-eyegazeall_run-01_bold.nii.gz
sub-819/ses-1519/func/sub-819_ses-1519_task-eyegazeall_run-01_bold.nii.gz
sub-819/ses-1520/func/sub-819_ses-1520_task-eyegazeall_run-01_bold.nii.gz
sub-821/ses-1521/func/sub-821_ses-1521_task-eyegazeall_run-01_bold.nii.gz
sub-821/ses-1522/func/sub-821_ses-1522_task-eyegazeall_run-01_bold.nii.gz
sub-823/ses-1523/func/sub-823_ses-1523_task-eyegazeall_run-01_bold.nii.gz
sub-823/ses-1614/func/sub-823_ses-1614_task-eyegazeall_run-01_bold.nii.gz
sub-824/ses-1524/func/sub-824_ses-1524_task-eyegazeall_run-01_bold.nii.gz
sub-824/ses-1615/func/sub-824_ses-1615_task-eyegazeall_run-01_bold.nii.gz
sub-825/ses-1525/func/sub-825_ses-1525_task-eyegazeall_run-01_bold.nii.gz
sub-826/ses-1526/func/sub-826_ses-1526_task-eyegazeall_run-01_bold.nii.gz
sub-828/ses-1528/func/sub-828_ses-1528_task-eyegazeall_run-01_bold.nii.gz
sub-831/ses-1531/func/sub-831_ses-1531_task-eyegazeall_run-01_bold.nii.gz
sub-832/ses-1532/func/sub-832_ses-1532_task-eyegazeall_run-01_bold.nii.gz
sub-833/ses-1533/func/sub-833_ses-1533_task-eyegazeall_run-01_bold.nii.gz
sub-834/ses-1534/func/sub-834_ses-1534_task-eyegazeall_run-01_bold.nii.gz
sub-835/ses-1535/func/sub-835_ses-1535_task-eyegazeall_run-01_bold.nii.gz
sub-835/ses-1619/func/sub-835_ses-1619_task-eyegazeall_run-01_bold.nii.gz
sub-836/ses-1536/func/sub-836_ses-1536_task-eyegazeall_run-01_bold.nii.gz
sub-837/ses-1537/func/sub-837_ses-1537_task-eyegazeall_run-01_bold.nii.gz
sub-837/ses-1620/func/sub-837_ses-1620_task-eyegazeall_run-01_bold.nii.gz
sub-838/ses-1538/func/sub-838_ses-1538_task-eyegazeall_run-01_bold.nii.gz
sub-838/ses-1621/func/sub-838_ses-1621_task-eyegazeall_run-01_bold.nii.gz
sub-839/ses-1539/func/sub-839_ses-1539_task-eyegazeall_run-01_bold.nii.gz
sub-840/ses-1540/func/sub-840_ses-1540_task-eyegazeall_run-01_bold.nii.gz
sub-841/ses-1541/func/sub-841_ses-1541_task-eyegazeall_run-01_bold.nii.gz
sub-842/ses-1542/func/sub-842_ses-1542_task-eyegazeall_run-01_bold.nii.gz
sub-843/ses-1543/func/sub-843_ses-1543_task-eyegazeall_run-01_bold.nii.gz
sub-844/ses-1544/func/sub-844_ses-1544_task-eyegazeall_run-01_bold.nii.gz
sub-853/ses-1553/func/sub-853_ses-1553_task-eyegazeall_run-01_bold.nii.gz
sub-854/ses-1554/func/sub-854_ses-1554_task-eyegazeall_run-01_bold.nii.gz
sub-855/ses-1555/func/sub-855_ses-1555_task-eyegazeall_run-01_bold.nii.gz
sub-856/ses-1616/func/sub-856_ses-1616_task-eyegazeall_run-01_bold.nii.gz
sub-857/ses-1557/func/sub-857_ses-1557_task-eyegazeall_run-01_bold.nii.gz
sub-857/ses-1618/func/sub-857_ses-1618_task-eyegazeall_run-01_bold.nii.gz
sub-858/ses-1558/func/sub-858_ses-1558_task-eyegazeall_run-01_bold.nii.gz
sub-859/ses-1559/func/sub-859_ses-1559_task-eyegazeall_run-01_bold.nii.gz
sub-859/ses-1622/func/sub-859_ses-1622_task-eyegazeall_run-01_bold.nii.gz
sub-860/ses-1560/func/sub-860_ses-1560_task-eyegazeall_run-01_bold.nii.gz
sub-861/ses-1561/func/sub-861_ses-1561_task-eyegazeall_run-01_bold.nii.gz
sub-861/ses-1623/func/sub-861_ses-1623_task-eyegazeall_run-01_bold.nii.gz
sub-862/ses-1562/func/sub-862_ses-1562_task-eyegazeall_run-01_bold.nii.gz
sub-862/ses-1624/func/sub-862_ses-1624_task-eyegazeall_run-01_bold.nii.gz
sub-863/ses-1563/func/sub-863_ses-1563_task-eyegazeall_run-01_bold.nii.gz
sub-864/ses-1564/func/sub-864_ses-1564_task-eyegazeall_run-01_bold.nii.gz
sub-865/ses-1565/func/sub-865_ses-1565_task-eyegazeall_run-01_bold.nii.gz
sub-868/ses-1568/func/sub-868_ses-1568_task-eyegazeall_run-01_bold.nii.gz
sub-868/ses-1626/func/sub-868_ses-1626_task-eyegazeall_run-01_bold.nii.gz
sub-869/ses-1569/func/sub-869_ses-1569_task-eyegazeall_run-01_bold.nii.gz
sub-871/ses-1571/func/sub-871_ses-1571_task-eyegazeall_run-01_bold.nii.gz
sub-872/ses-1572/func/sub-872_ses-1572_task-eyegazeall_run-01_bold.nii.gz
sub-873/ses-1573/func/sub-873_ses-1573_task-eyegazeall_run-01_bold.nii.gz
sub-874/ses-1574/func/sub-874_ses-1574_task-eyegazeall_run-01_bold.nii.gz
sub-875/ses-1575/func/sub-875_ses-1575_task-eyegazeall_run-01_bold.nii.gz
sub-875/ses-1627/func/sub-875_ses-1627_task-eyegazeall_run-01_bold.nii.gz
sub-878/ses-1578/func/sub-878_ses-1578_task-eyegazeall_run-01_bold.nii.gz
sub-879/ses-1579/func/sub-879_ses-1579_task-eyegazeall_run-01_bold.nii.gz
sub-880/ses-1580/func/sub-880_ses-1580_task-eyegazeall_run-01_bold.nii.gz
sub-880/ses-1611/func/sub-880_ses-1611_task-eyegazeall_run-01_bold.nii.gz
sub-881/ses-1581/func/sub-881_ses-1581_task-eyegazeall_run-01_bold.nii.gz
sub-881/ses-1612/func/sub-881_ses-1612_task-eyegazeall_run-01_bold.nii.gz
sub-882/ses-1582/func/sub-882_ses-1582_task-eyegazeall_run-01_bold.nii.gz
sub-883/ses-1583/func/sub-883_ses-1583_task-eyegazeall_run-01_bold.nii.gz
sub-883/ses-1613/func/sub-883_ses-1613_task-eyegazeall_run-01_bold.nii.gz
sub-884/ses-1584/func/sub-884_ses-1584_task-eyegazeall_run-01_bold.nii.gz
sub-885/ses-1585/func/sub-885_ses-1585_task-eyegazeall_run-01_bold.nii.gz
sub-887/ses-1587/func/sub-887_ses-1587_task-eyegazeall_run-01_bold.nii.gz
sub-889/ses-1589/func/sub-889_ses-1589_task-eyegazeall_run-01_bold.nii.gz
sub-891/ses-1591/func/sub-891_ses-1591_task-eyegazeall_run-01_bold.nii.gz
sub-892/ses-1592/func/sub-892_ses-1592_task-eyegazeall_run-01_bold.nii.gz
sub-893/ses-1593/func/sub-893_ses-1593_task-eyegazeall_run-01_bold.nii.gz
sub-894/ses-1594/func/sub-894_ses-1594_task-eyegazeall_run-01_bold.nii.gz
sub-895/ses-1595/func/sub-895_ses-1595_task-eyegazeall_run-01_bold.nii.gz
sub-896/ses-1596/func/sub-896_ses-1596_task-eyegazeall_run-01_bold.nii.gz
sub-897/ses-1597/func/sub-897_ses-1597_task-eyegazeall_run-01_bold.nii.gz
sub-898/ses-1598/func/sub-898_ses-1598_task-eyegazeall_run-01_bold.nii.gz
sub-899/ses-1599/func/sub-899_ses-1599_task-eyegazeall_run-01_bold.nii.gz
sub-900/ses-1600/func/sub-900_ses-1600_task-eyegazeall_run-01_bold.nii.gz
sub-901/ses-1601/func/sub-901_ses-1601_task-eyegazeall_run-01_bold.nii.gz
sub-902/ses-1602/func/sub-902_ses-1602_task-eyegazeall_run-01_bold.nii.gz
sub-903/ses-1603/func/sub-903_ses-1603_task-eyegazeall_run-01_bold.nii.gz
sub-904/ses-1604/func/sub-904_ses-1604_task-eyegazeall_run-01_bold.nii.gz
sub-905/ses-1605/func/sub-905_ses-1605_task-eyegazeall_run-01_bold.nii.gz
sub-906/ses-1606/func/sub-906_ses-1606_task-eyegazeall_run-01_bold.nii.gz
sub-907/ses-1607/func/sub-907_ses-1607_task-eyegazeall_run-01_bold.nii.gz
sub-908/ses-1608/func/sub-908_ses-1608_task-eyegazeall_run-01_bold.nii.gz
sub-910/ses-1610/func/sub-910_ses-1610_task-eyegazeall_run-01_bold.nii.gz
sub-912/ses-1625/func/sub-912_ses-1625_task-eyegazeall_run-01_bold.nii.gz
sub-913/ses-1628/func/sub-913_ses-1628_task-eyegazeall_run-01_bold.nii.gz

```
