#!/usr/bin/env python3
"""
Mine .

Usage:
    mine_issue_comments.py [options] OWNER REPO

Options:    
    -n NAME
        Save filename as NAME  
    --verbose
        Output verbose debugging information.
"""



from docopt import docopt
import pandas as pd
import json 
import pickle
from pydriller import Repository
from github import Github
from github import Auth


auth = Auth.Token("xxxxxUSExxYOURxxTOKENxxx")
g = Github(auth=auth)




BASE_DIR  = '../'




def get_all_issues(owner, repo_name):
    
    prefix_loc ='../data/mined/iscs_'  

    repo = g.get_repo(owner+'/'+repo_name)    
    issues = repo.get_issues_comments()


    izs = []
    ctr = 1
    for issue in issues:
        
        try:
            iz=issue.raw_data
            iz['user']= {k:iz['user'][k] for  k in ['login', 'id', 'node_id', 'type', 'site_admin']}                        
            
            iz['issue_num'] = iz['issue_url'].split('/')[-1]
            del iz['issue_url']
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
    get_all_issues(owner, repo_name)
    

if __name__ == '__main__':
    opts = docopt(__doc__)   
    main(opts)