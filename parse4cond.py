#! /usr/bin/env python3

import os
import semopy
import pandas as pd
from sklearn.preprocessing import StandardScaler
import argparse
import yaml
import glob

class Parse4cond:
    
    """
    Parse the 4 conditions (ABCD) from the eyegaze task fmri dataset.
    """
    
    def __init__(self, index=[0,None], mdir='.', list=True, stub='_eyegazeall.csv'):
        
        """

        """
        self.index=index
        self.mdir = mdir
        self.stub=stub
        self.verbose=True
        self.outdir = 'dataorig'
        self.datadir = 'dataorig'
    
        # check if output directory exists if not create
        output = os.path.join(mdir, self.outdir)
        if not os.path.isdir(output):
            os.makedirs(output,exist_ok=True)

        # get sorted list of files from data directory
        self.files = glob.glob(os.path.join(self.mdir, self.datadir, f"*{self.stub}"))
        self.files.sort()
        
        if list:
            i = 0
            for file in self.files:
                print(f"{i}: {file}")
            exit()
        
        self.work()

    def work(self):

        # create the lists for extracting each condition
        extractlist = self.create_eg_cond_lists()

        for file in self.files[self.index[0]: self.index[1]]:

            # get the basename without the .csv
            basename = os.path.basename(file).split('.csv')[0]

            # read in the data file into a df
            self.df = pd.read_csv(file)

            for c in ['A','B','C','D','E']:
                # new output data file name
                newdatafile = os.path.join(  self.mdir, 
                                            self.outdir, 
                                            f"{basename}_run-c{c}.csv")
                # create copy of df
                tmpdf = self.df.copy()
                # select the rows using an index list
                tmpdf = self.df.iloc[extractlist[c]]

                # save df to newdatafile
                tmpdf.to_csv(newdatafile, index=False)

                if self.verbose:
                    print(newdatafile)

                pass

    def create_eg_cond_lists(self):
        """
        Create the eyegaze condition index lists for extracting timepoints for
        a condition.

        Returns a dictionary of lists for each condition A-E
        """                 

        rindex = {}
        rindex['A'] = list(range(21,39)) + list(range(122,141)) + \
                        list(range(224,243))
        rindex['B'] = list(range(54,73)) + list(range(156,175)) + \
                        list(range(258,277))
        rindex['C'] = list(range(88,107)) + list(range(190,209)) + \
                        list(range(292,310))
        rindex['D'] = list(range(8,20)) + list(range(39,54)) + \
                        list(range(73,88)) + list(range(107,122)) + \
                        list(range(141,156)) + list(range(175,190)) + \
                        list(range(209,224)) + list(range(243,258)) + \
                        list(range(277,292))
        rindex['E'] = list(range(8,310))

        full_list = {}
        for c in ['A','B','C','D','E']:
            offset = 310
            templist = [element + offset for element in rindex[c]]
            full_list[c] = rindex[c] + templist

        return full_list
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""    
    Parse the 5 conditions (ABCDE) from the eyegaze task fmri dataset.  Assumes that
    the input csv file has 621 rows including header.  The input csv file can have a 
    stub to assist in file selection (e.g. _eyegazeall.csv)

    """)

    parser.add_argument("--start", type = int,
                        help="beginning file list index , default 0",
                        default = 0)
    parser.add_argument("--end", type = str,
                        help="end file list index, default None",
                        default=None)
    parser.add_argument("--mdir", type = str,
                     help="main directory, default is the dataorig",
                     default='dataorig') 
    parser.add_argument("--list", help="list the files to be processed",
                        action = "store_true")
    parser.add_argument("--stub",  type = str,
                        help = "file stub to assist in file selection, default - eyegazeall.csv",
                        default = 'eyegazeall.csv')
    
    args = parser.parse_args()
    
    # setup default values
    if args.end != None:
        args.end = int(args.end)
        
    test = True
    if test:
        # test
        g=Parse4cond(index=[args.start, args.end], mdir = '.', list=args.list,
                    stub=args.stub)
    else:
        g=Parse4cond(index=[args.start, args.end], mdir = args.mdir, list=args.list,
                    stub=args.stub)
