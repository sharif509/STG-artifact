#!/usr/bin/env python3
"""
Mine. 

Usage:
    mine_pr_comments.py [options] OWNER REPO

Options:    
    -n NAME
        Save filename as NAME  
    --verbose
        Output verbose debugging information.
"""

from docopt import docopt
import pandas as pd

import os
from pydriller import Repository
from github import Github
from github import Auth

auth = Auth.Token('xxxxxUSExxYOURxxTOKENxxx')
g = Github(auth=auth)

    
BASE_DIR  = '../'



def get_all_prs(owner, repo_name):

    prefix_loc = BASE_DIR+'data/mined/prcs_'    

    repo = g.get_repo(owner+'/'+repo_name)
    prs = repo.get_pulls_comments() 
    
    
    izs = []
    ctr = 1
    for pr in prs:
        
        try:
            iz=pr.raw_data
            iz['user']= {k:iz['user'][k] for  k in ['login', 'id', 'node_id', 'type', 'site_admin']}                                        
            del iz["url"]
            del iz["html_url"]

            izs.append(iz)
            
        except Exception as e:
            print(repo_name, iz['id'], 'ctr=',ctr,'encountered an error', e)
        ctr+=1

    df = pd.DataFrame(izs)    
    df.to_pickle(prefix_loc+repo_name+'.pkl')
    
    del df

#-------------------------------------------------------------------------------------
def main(opts):
    owner, repo_name = opts['OWNER'],opts['REPO']
    get_all_prs(owner, repo_name)
    


    


if __name__ == '__main__':
    opts = docopt(__doc__)
    main(opts)

