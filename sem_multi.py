#! /usr/bin/env python

import semopy 
import pandas as pd
import os
import pathlib
import argparse
import datetime
import glob

class Sem:
    
    def __init__(self, noplot=False, list=False):
        self.noplot_flag = noplot  #  set plot flag
        self.list = list
        self.outputdir = 'output'
        self.algo = 'fges'
        
    def run_sem(self, prefix):  
        modelfile = os.path.join(self.outputdir, prefix + '.lav')
        plotfile_png = os.path.join(self.outputdir, prefix + '.png')
        plotfile_pdf = os.path.join(self.outputdir, prefix + '.pdf')
        
        fp = open(modelfile, 'r')
        desc = fp.read()
        
        # check size of desc file
        if len(desc) > 0:
            # read in data
            datafile = os.path.join('data', prefix + '.csv')
            data = pd.read_csv(datafile)
            model = semopy.Model(desc)
            opt_res = model.fit(data)
            estimates = model.inspect()
            
            if not self.noplot_flag:
                g = semopy.semplot(model, plotfile_png)
                #g = semopy.semplot(model, plotfile_pdf)
                # rename the gv file from no prefix to prefix + '.gv'
                gvfile_no_suff = os.path.join(self.outputdir, prefix)
                gv_file = os.path.join(self.outputdir, prefix + '.gv')
                if os.path.isfile(gvfile_no_suff):
                    os.rename( gvfile_no_suff, gv_file)

            # write out estimates
            estimates.to_csv('output/'+ prefix +'_semopy.csv',index=False)
            estimates.to_json(path_or_buf='output/'+prefix + '_semopy.json', orient='records')
        else:
            # model not available
            print(f"*** No model available for {prefix}")
                
def main(index=[0,None], noplot=False, list=False):
    c = Sem(noplot=noplot)

    files = glob.glob(os.path.join('output', "*.lav"))
    files.sort()
    
    
    if list:
        i = 0
        for file in files:
            print(f"{i}: {file}")
            i += 1
        exit()

    #for file in ['sub_1001.csv']:
    i = 0
    for file in files[index[0]:index[1]]:
        # run semopy to calculate the parameters
        now = datetime.datetime.now()
        infostr = f"{i}/{len(files)}"
        print (infostr, 'start:', now.strftime("%Y-%m-%d %H:%M:%S"))

        prefix = pathlib.Path(file).stem
        print(prefix)
        c.run_sem(prefix)
        now = datetime.datetime.now()
        print ('finish:', now.strftime("%Y-%m-%d %H:%M:%S"))
            
        i += 1

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description = "Does the sem estimates for the lavaan model. \
            The semopy package is used."
    )
    parser.add_argument("--start", type = int,
                        help="beginning file list index , default 0",
                        default = 0)
    parser.add_argument("--end", type = str,
                        help="end file list index, default None",
                        default=None)
    parser.add_argument("--list", help="list the files to be processed",
                        action = "store_true",
                        default = False)
    parser.add_argument("--noplot", help="do not create the plot files, \
        default is to create the plot files",
        action = "store_true", default = False)
    args = parser.parse_args()

    # setup default values
    if args.end != None:
        args.end = int(args.end)

    test = False
    if test:
        main( index = [args.start, 1], 
            noplot=args.noplot, list=args.list)
    else:
        main( index = [args.start, args.end], noplot=args.noplot, list=args.list)
        
