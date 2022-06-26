#! /usr/bin/env python

import pandas as pd
import numpy as np
"""
Code to generate lists for each of conditions abcd to extract out
time courses from csv files with 620 rows.

"""

def create_eg_cond_lists():
    """
    Create the eyegaze condition index lists for extracting timepoints for
    a condition.

    Returns a dictionary of lists for each condition A-D
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

    full_list = {}
    for c in ['A','B','C','D']:
        offset = 320
        templist = [element + offset for element in rindex[c]]
        full_list[c] = rindex[c] + templist

    return full_list


file = 'NEW Conditions A, B and C - v4.csv'

cond = pd.read_csv(file)

# name of column containing the conditions A-D,Z (discard Z)
condcol = cond.columns[2]
# get single column
co = cond.loc[:,condcol]

# get indexes meeting conditions A-D
"""
In [719]: select_indices = list(np.where(df["BoolCol"] == True)[0])
In [720]: df.iloc[select_indices]
"""
listx = cond[cond.iloc[:,2] == 'A']

rowindexes = {}
for conds in ['A','B','C','D']:
    rowindexes[conds] = list(np.where(cond[condcol] == conds)[0])



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

# do sanity check
for c in ['A','B','C','D']:
    if rowindexes[c] == rindex[c]:
        print(f"OK: condition {c} matches")
    else:
        print(f"Error: condition {c} lists don't match")


# extend each index by 320
# new_list = [element + 1 for element in a_list]
full_list = {}
for c in ['A','B','C','D']:
    offset = 320
    templist = [element + offset for element in rindex[c]]
    full_list[c] = rindex[c] + templist
    

new_list = create_eg_cond_lists()

if full_list == new_list:
    print(f"OK: Lists match")
else:
    print(f"Error: lists don't match")
pass
