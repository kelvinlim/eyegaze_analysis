#! /usr/bin/env python
# read the data

import os
import pandas as pd
import glob
import argparse
from sklearn.preprocessing import StandardScaler

class StdData:
    
    """
    Standardize the data
    
    """
    
    def __init__(self, index=[0,None], diag=False, list=False):
        
        self.diag = diag
        self.list = list
        self.std = True
        self.args = {
            'dataorig': 'dataorig' ,
            'datanew': 'data',
            }
        
        #self.testfile = "dataorig/sub-10014_ses-54531_task-rest_acq-eyesclosedPA_run-01_glasser19vol.ptseries.csv"
    
        #self.read_file(self.testfile)
        
        #print(self.testfile)

        self.no_std = True       
        self.work( index=index)
        
    
    def read_file(self, filepath):
        # read in the data file into a dataframe
        self.dforig = pd.read_csv(filepath)
        
        # get column names
        
        #df.rename(columns=colrenames, inplace=True)
        
        
    def standardize_df_col(self):
        """
        standardize the columns in the dataframe
        https://machinelearningmastery.com/normalize-standardize-machine-learning-data-weka/
        
        * get the column names for the dataframe
        * convert the dataframe into into just a numeric array
        * scale the data
        * convert array back to a df
        * add back the column names
        * set to the previous df
        """
        
        # describe original data - first two columns
        if self.diag:
            print(self.newdf.iloc[:,0:2].describe())
        # get column names
        colnames = self.newdf.columns
        # convert dataframe to array
        data = self.newdf.values
        # standardize the data
        data = StandardScaler().fit_transform(data)
        # convert array back to df, use original colnames
        self.newdf = pd.DataFrame(data, columns = colnames)
        # describe new data - first two columns
        if self.diag:
            print(self.newdf.iloc[:,0:2].describe())

        
    def work(self, index=[0,None]):
        # get the csv files from the data directory
    
        self.files = glob.glob(os.path.join(self.args['dataorig'], "*.csv"))
        self.files.sort()

        if self.list:
            i = 0
            for file in self.files:
                print(f"{i}/{len(self.files)}: {file} ")
                i+=1
            exit()    

        i = 0
        for file in self.files[index[0]:index[1]]:
            print(f"{i}: {file}")
            # read in the data
            self.newdf = pd.read_csv(file)
            

            # standardize ?
            if self.std:
                self.standardize_df_col()
                
            newfilepath = os.path.join(self.args['datanew'], 
                                       os.path.basename(file))
            self.newdf.to_csv(newfilepath, index=False)

            i+=1
            pass

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="standardize csv files of data in dataorig folder and place in data folder"
    )
    parser.add_argument("--start", type = int,
                        help="beginning file list index , default 0",
                        default = 0)
    parser.add_argument("--end", type = str,
                        help="end file list index, default None",
                        default=None)
    parser.add_argument("--diag", help="show some diagnostics",
                        action = "store_true",
                        default=False)    
    parser.add_argument("--list", help="list the files to be processed",
                        action = "store_true",
                        default=False)

    args = parser.parse_args()

    # setup default values
    if args.end != None:
        args.end = int(args.end)
 
    #c = RenameData(drop_columns='90') # to drop 90%
    #c = RenameData(drop_columns='') # keep all columns; do all files
    c = StdData(index=[args.start,args.end], diag=args.diag, list=args.list)



