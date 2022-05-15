#! /usr/bin/env python3

import os
import semopy
import pandas as pd
import argparse
import numpy as np
import scipy.stats as stats
import json
import glob

class CausalWrap:
    
    """
    class that wraps the causal-cmd in a python wrapper
    
    """
    
    def __init__(self):
        
        # set the default arguments for causal-cmd 1.1.1
        self.causal_args = {
            'dataset': '',
            'algorithm': 'fges',
            'data-type': 'continuous',
            'delimiter': 'comma',
            'score': 'sem-bic',
            'prefix': '',
            'thread': '1',
            'skip-latest': True,
            'out': 'output'
            }
        
        self.args = {
            'rawdata': 'data' ,
            'causal-cmd': 'causal-cmd '
            }
        
        self.edges = []
        self.model = ''
        self.algo = 'fges'

        #self.set_arg({'dataset': 'sub_1001.csv'})
        #self.create_cmd()
        
        
    def set_arg(self, argval):
        """
        set the arguments 

        Parameters
        ----------
        argval : a dictionary of arg value pairs.
            .

        Returns
        -------
        None.

        """
        
        for key in argval.keys():
            # change existing arg or add an arg
            self.causal_args[key] = argval[key]

            # set the prefix based on the dataset name
            if key == 'dataset':
                prefix = os.path.basename(self.causal_args[key]).split('.csv')[0]
                self.causal_args['prefix'] = prefix
                
                
    def create_cmd(self):
        """
        create the causal-cmd using the arguments

        Returns
        -------
        0 - if OK
        1 if  problem

        """
        
        self.cmd = self.args['causal-cmd']
        
        # check to make sure that critical arguments
        # are set
        
        if (self.causal_args['dataset'] == '') or (self.causal_args['prefix'] == ''):
                # missing args
                return 1
            
        for key in self.causal_args.keys():
            
            if key == 'skip-latest':
                if self.causal_args[key] == True:
                    argstr = '--skip-latest '
            elif key == 'dataset':
                # add directory info
                argstr = '--%s %s '%(key, 
                                    os.path.join(self.causal_args['dataset']))
            else:
                argstr = "--%s %s "%(key, self.causal_args[key])
                
            self.cmd += argstr
            
        
        return 0
    
    def parse_edges(self, file='output/sub_1066.txt'):
        """
        parse the  edges from the output file
        
        get edges and parse into a list of dict
        Graph Edges:
        1. drinks --> drinking dd nl
        
        {'a': 'drinks', 'etype': '-->', 'b': 'drinking', 'extra': ['dd','nl']}

        Parameters
        ----------
        file : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        self.edges = []

        # open the file
        f = open(file, 'r')
        self.lines = f.readlines()
        
        in_edge = False  # boolean for in_edge section
        
        for line in self.lines:
            if line.startswith('Graph Attributes'):
                in_edge = False  
            # print("info: ", line)
            if in_edge:  # parse the line
                segs = line.split()
                if len(segs) > 0:
                    #print(segs)
                    edge = {}
            
                    if len(segs) >= 4:
                        edge['a'] = segs[1]
                        edge['etype'] = segs[2]
                        edge['b'] =  segs[3]
                       
                    if len(segs) > 4:
                        edge['extra'] = [segs[4], segs[5]]
                    else:
                        edge['extra'] = {'flip':False}
                    
                    
                    self.edges.append(edge)
                
            if line.startswith('Graph Edges:'):
                in_edge = True
        
    def check_edges_lr(self,filepath):
        """
        Check each of the edges using the likelihood ratio
        with robust outliers code from 
        Hyvärinen, A., & Smith, S. M. (2013). 
        Pairwise Likelihood Ratios for Estimation of 
        Non-Gaussian Structural Equation Models.
        Journal of Machine Learning Research: JMLR, 
        14(Jan), 111–152.

        """
        # read in the fmri data into a df
        df = pd.read_csv(filepath)
        
        # check each edge
        flips=0
        total=0
        for edge in self.edges:
            total += 1
            W = df[[edge['a'],edge['b']]]
            lr = self.pwlr3(W)
            # if value is negative then switch causal direction of
            # edge by swapping 'a' and 'b' in dictionary
            lrvalue = lr.loc[edge['a']][edge['b']]
            if  lrvalue < 0:
                tmp = edge['a']
                edge['a'] = edge['b']
                edge['b'] = tmp
                # set flag that edge flipped
                edge['extra'] = {'flip':True,'lr':lrvalue}
                flips += 1
            else:
                # no flip
                edge['extra'] = {'flip':False,'lr':lrvalue}
            pass
            
        # save the edge information in a json file in the output directory
        root, ext = os.path.splitext(os.path.basename(filepath))
        jsonpath = os.path.join(self.causal_args['out'],
                                root + '_edges.json')
        json.dump(self.edges, open(jsonpath,'w'), indent=4)
        return {'flips':flips, 'total':total}     
        
    def pwlr3(self, W):
        
        # assume that W is standardized
        
        # compute likelihood ratio with 
        # new skewness -based measure robust to outliers
        
        # transpose to match octave code
        X = np.transpose(W)
        #Get size parameters
        #[n,T]=size(X);
        n, T = X.shape
        
        #%If using skewness measures with skewness correction, make skewnesses positive
        #for i=1:n; X(i,:)=X(i,:)*sign(skewness(X(i,:))); end
        for i in range(n):
            X.iloc[i,:]=X.iloc[i,:]*np.sign(stats.skew(X.iloc[i,:]))
        
        #%Compute covariance matrix
        #C=cov(X');
        # https://www.pythonpool.com/numpy-cov/
        # already transposed in python above
        C = np.cov(X)

        # Compute causality measures
        # %New skewed measure, robust to outliers
        # gX=log(cosh(max(X,0)));
        # octave max is different than numpy max!
        # max(X,0) sets values in X < 0 to 0
        gX = np.log(np.cosh(np.maximum(X,0)))
                    
        #LR= C.*(-(X*gX'/T)+(gX*X'/T));
        # numpy matrix multiplication is @
        # * is element wise multiplication
        
        part1 = gX @ np.transpose(X)
        part2 = X @ np.transpose(gX)
        lr = C * (part1/T -part2/T )
                  
        return lr
    def generate_model(self):
        # generate a model for sem in lavaan format text
        self.model = ''  # string to hold the model
        
        for edge in self.edges:
    
            # create the different edges needed
            if self.algo == 'fges':
                # only do direct edge
                if edge['etype'] == '-->':
                    ops = ['~']
                else:
                    ops = []

            for op in ops:
                str = '%s %s %s\n'%(edge['b'], op, edge['a'])
                self.model += str  # append to model string
                # print(edge, str)
        return self.model
    
 
        
def fges_lr(index=[0,None], std=False, list=True):
    # get the csv files from the data directory
    c = CausalWrap()
    #c.set_arg({'knowledge': 'prior.txt'})
    
    # get sorted list of files in directory
    """
    files = os.listdir("data")    
    files = list(filter(lambda f: f.endswith('.csv'), files))
    files.sort()
    """

    files = glob.glob(os.path.join('data', "*.csv"))
    files.sort()

    if list:
        i = 0
        for file in files:
            print(f"{i}/{len(files)}: {file} ")
            i+=1
        exit()
    
    #for file in ['sub_1001.csv']:
    for file in files[index[0]: index[1]]:

        c.set_arg({'dataset': file})
        c.create_cmd()
        print(c.cmd)
        os.system(c.cmd)
        
        # read in the output file and get the edges
        outputfile = os.path.join(c.causal_args['out'], 
                                  c.causal_args['prefix'] + '.txt')
        c.parse_edges(file=outputfile)
        #print(c.edges)
        
        # check each of the edges with likelihood ratio
        stats = c.check_edges_lr(file)
        print(stats)
        # create model from edges
        c.generate_model()
        
        # output the model file
        modelfile = os.path.join(c.causal_args['out'], 
                                  c.causal_args['prefix'] + '.lav')
        #print(c.model)
        fp = open(modelfile, 'w')
        fp.write(c.model)

            
 
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description = "Runs the causal-cmd on the csv files in the \
            data directory. We use FGES for the causal discovery. \
            The likelihood ratio is the used to identify\
            the direction of causality. \
            (Hyvärinen, A., & Smith, S. M. (2013). Pairwise Likelihood Ratios for Estimation of Non-Gaussian Structural Equation Models. Journal of Machine Learning Research: JMLR, 14(Jan), 111–152)\
            \
            \
            "
    )
    parser.add_argument("--start", type = int,
                        help="beginning file list index , default 0",
                        default = 0)
    parser.add_argument("--end", type = str,
                        help="end file list index, default 1",
                        default=None)
    parser.add_argument("--list", help="list the files to be processed",
                        action = "store_true",
                        default = False)
    """
    parser.add_argument("--std", help="standardize the data, default: False",
                        action = "store_true",
                        default = False)
    """
    args = parser.parse_args()

    # setup default values
    if args.end != None:
        args.end = int(args.end)

    fges_lr( index = [args.start, args.end], 
        #std=args.std, 
        list=args.list)

    
