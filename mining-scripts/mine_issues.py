#!/usr/bin/env python3
"""
Mine. 

Usage:
    mine_issues.py [options] OWNER REPO

Options:    
    -n NAME
        Save filename as NAME  
    --verbose
        Output verbose debugging information.
"""
# -r REPO
        # Location of repository to be mined



from docopt import docopt
import pandas as pd
import os
from pydriller import Repository
from github import Github
from github import Auth

auth = Auth.Token("xxxxxUSExxYOURxxTOKENxxx")
g = Github(auth=auth)

import json

BASE_DIR  = '../'



def get_all_issues(owner, repo_name):

    prefix_loc = BASE_DIR+'data/mined/iss_'
    repo = g.get_repo(owner+'/'+repo_name)
    issues = repo.get_issues(state='all')    
    izs = []
    ctr = 1
    for issue in issues:
        
        try:
            iz=issue.raw_data
            del iz["url"]
            del iz["repository_url"]
            del iz["labels_url"]
            del iz["comments_url"]
            del iz["events_url"]
            del iz["html_url"]
            del iz["timeline_url"]

            iz['user']= {k:iz['user'][k] for  k in ['login', 'id', 'node_id', 'type', 'site_admin']}
            if iz['assignee']: 
                iz['assignee']= {k:iz['assignee'][k] for  k in ['login', 'id', 'node_id', 'type', 'site_admin']}
            if iz['closed_by']: 
                iz['closed_by']= {k:iz['closed_by'][k] for  k in ['login', 'id', 'node_id', 'type', 'site_admin']}

            iz['assignees'] = [{k:u[k] for k in ['login', 'id', 'node_id', 'type', 'site_admin']} for u in iz['assignees']]
            iz['labels'] = [{k:u[k] for k in ['name']} for u in iz['labels']]
            
            
            #            

            if 'pull_request' in iz:
                iz['pr_merged_at'] = iz['pull_request']['merged_at']
            else:
                iz['pull_request']=None
                iz['pr_merged_at']=None
                # 
            izs.append(iz)
            
        except Exception as e:
            print(repo_name, iz['number'], 'ctr=',ctr,'encountered an error', e)

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
