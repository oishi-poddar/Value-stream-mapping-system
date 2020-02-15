# Required:install package pygithub
# https://pypi.org/project/PyGithub
# https://pygithub.readthedocs.io

from github import Github
import pymongo
import sys
from datetime import timedelta
import datetime
import re
import config


def p1_git(status, my_col):
    print(status)
    count = 0
    today = datetime.datetime.now()
    d = today - timedelta(days=n_days)
    pulls = None
    if my_col.count_documents({}) > 0:
        d = my_col.find().sort('closed_at', -1)[0]['closed_at']
    if my_col.count_documents({}) == 0:
        pulls = repo.get_pulls(state=status, base='master', sort='created', direction='desc')
    else:
        pulls = repo.get_pulls(state=status, base='master', sort='updated', direction='desc')

    if status == 'open':
        my_col.delete_many({})

    for pr in pulls:
        label_continuouslocalization = False
        if (today - pr.created_at) > timedelta(days=n_days): break
        if status == 'closed' and pr.closed_at <= d: break
        jira_id = None
        duration_to_merge = None
        duration_to_close = None
        # Finding the match to the pattern in the given string
        if pattern.findall(pr.title):
            jira_id = pattern.findall(pr.title)[0]
        elif pattern.findall(pr.head.label):
            jira_id = pattern.findall(pr.head.label)[0]
        elif pattern.findall(pr.body):
            jira_id = pattern.findall(pr.body)[0]
        elif pr.labels:
            if pr.labels[0].name == 'ContinuousLocalization':
                label_continuouslocalization = True

        if pr.closed_at is not None:
            duration_to_close = "{0:.2f}".format((pr.closed_at - pr.created_at).total_seconds())  # in seconds
        if pr.merged_at is not None:
            duration_to_merge = "{0:.2f}".format((pr.merged_at - pr.created_at).total_seconds())  # in seconds
        data = {
            '_id': pr.number,
            'title': pr.title,
            'state': pr.state,
            'jira_id': jira_id,
            'created_at': pr.created_at,
            'closed_at': pr.closed_at,
            'merged_at': pr.merged_at,
            'label_ContinuousLocalization': label_continuouslocalization,
            'duration_to_close': duration_to_close,
            'duration_to_merge': duration_to_merge,
            'review_comment_count': pr.review_comments,
        }
        if status == 'open':
            data['Open_since'] = "{0:.2f}".format((today - pr.created_at).total_seconds())
        print(pr.number)
        count += 1
        my_col.insert_one(data)
    print('Data Inserted', status, '  ', count)


# input argument format= 0:script_name, 1:input_token, 2:Repo_Name, 3:status, 4:pattern to get Jira ID, 5:number_of_days
login_token = sys.argv[1]  # 'login_token'
repo_name = sys.argv[2]  # "A360/Galileo-Web"
jira_id_format = sys.argv[3]  # pattern to get the Jira ID
n_days = 720  # Number of days to get the list

# defining variables
pattern = re.compile(jira_id_format + "-\d+")  # pattern to get the Jira id
# Database Connection
# server = "mongodb://" + config.mongodb['hostname'] + ":" + str(config.mongodb['port']) + "/"

my_client = pymongo.MongoClient(config.server)
my_db = my_client[config.mongodb['db']]
my_col_closed = my_db['git_data_closed']
my_col_open = my_db['git_data_open']

g = Github(base_url="https://git.autodesk.com/api/v3", login_or_token=login_token)
repo = g.get_repo(repo_name)
print("Repo name = " + repo.name)
p1_git('open', my_col_open)
p1_git('closed', my_col_closed)
