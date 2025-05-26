#!/usr/bin/env python3
"""
Mine commits.

Usage:
    mine_commits.py [options] REPO

Options:    
    -n NAME
        Save filename as NAME  
    --verbose
        Output verbose debugging information.
"""



from docopt import docopt
import pandas as pd
from pydriller import Repository



    
BASE_DIR  = '../'



def commit_to_dict(commit):
    return {
        'hash': commit.hash,
        'author': commit.author.name,
        'author_email': commit.author.email,
        'author_date': commit.author_date.isoformat(),
        'committer': commit.committer.name,
        'committer_email': commit.committer.email,
        'committer_date': commit.committer_date.isoformat(),
        'msg': commit.msg,
        'parents': commit.parents,
        'merge': commit.merge,
        'dmm_unit_size': commit.dmm_unit_size,
        'dmm_unit_complexity': commit.dmm_unit_complexity,
        'dmm_unit_interfacing': commit.dmm_unit_interfacing
    }

def get_all_commits(repo_name, save_as=''):
        
    prefix_loc = BASE_DIR+'data/mined/commits_'
    prefix_loc+=save_as+'_'
    ctr=1    
    commits = []
    
     
    repo = Repository(BASE_DIR+'data/repos/'+repo_name)    

    print(repo_name, 'begins')
    
    for c in repo.traverse_commits():
        try:
            commits.append(commit_to_dict(c))
        except Exception:
            print(repo_name, c.hash, 'encountered an error')        
        ctr+=1

    df = pd.DataFrame(commits)
    df.to_csv(prefix_loc+repo_name+'.csv')
    print(repo_name,df.size)    

    del df

    return

#-------------------------------------------------------------------------------------
def main(opts):
    repo_name = opts['REPO']
    save_as = opts['-n']    
    get_all_commits(repo_name, save_as)
    

    


if __name__ == '__main__':
    opts = docopt(__doc__)
    main(opts)
