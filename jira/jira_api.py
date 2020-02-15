"""
This script is used to fetch the JIRA data using the API and uses the python package 'jira-python'.
Documentation: https://jira.readthedocs.io/en/master/index.html
Expected command line arguments:[file name to be run, username, password, project_key]
Issues returns the data in json format where the first parameter is the JQL query string which is amendable according to need and currently fetched issues for the past two year
and the fields resolution,updated,description,project,created,status,issuetype,summary,resolutiondate,comment.
"""

from jira import JIRA
import sys
import pymongo
import config


def insert_data(d, my_col):
    print(d['id'], d['fields']['created'], d['fields']['resolutiondate'], end=',')
    json_data = {
        "key": d["key"],
        "_id": d["id"],
        "status": d['fields']['status']['name'],
        "summary": d['fields']['summary'],
        "description": d['fields']['description'],
        "created": d['fields']['created'],
        "updated": d['fields']['updated'],
        "issuetype": d['fields']['issuetype']['name'],
        "resolutiondate": d['fields']['resolutiondate'],
        "project": d['fields']['project']['name'],
        "comment": d['fields']['comment']['total'],
    }
    print(d['key'])
    my_col.insert_one(json_data)


def p1_jira(status, my_col):
    print(status)
    i = 0
    total = 1
    count = 0
    fields = "resolution,updated,description,project,created,status,issuetype,summary,resolutiondate,comment"
    if status == 'not closed':
        my_col.delete_many({})
    while True:
        if total < i: break
        if status == 'closed':
            issues = jira.search_issues(
                "project=" + project_key + " AND status in (Closed,Delivered,Finished) AND created >= -720d ORDER BY created DESC ",
                startAt=i, maxResults=1000, json_result=True, fields=fields)
        else:
            issues = jira.search_issues(
                "project=" + project_key + " AND status not in (Closed,Delivered,Finished) AND created >= -720d ORDER BY created DESC ",
                startAt=i, maxResults=1000, json_result=True, fields=fields)
        total = issues['total']
        print(i, total)
        i += 1000
        all_id = list(my_col.distinct('_id'))
        for d in issues['issues']:
            if (d['id'] not in all_id):
                insert_data(d, my_col)
                count += 1
        # if count == 0: break
    print('Data Inserted ', status, '  ', count)


program_name = sys.argv[0]
arguments = sys.argv[1:]
if len(sys.argv) == 2 and sys.argv[1] == '--help':
    print(__doc__)
elif len(sys.argv) < 4:
    print("Error in input arguments!")
    print(__doc__)
else:
    username = sys.argv[1]  # taking input arguments
    pwd = sys.argv[2]
    project_key = sys.argv[3]
    jira = JIRA(basic_auth=(username, pwd), options={'server': 'https://jira.autodesk.com'})
    my_client = pymongo.MongoClient(config.server)
    my_db = my_client[config.mongodb['db']]
    jira_data_closed = my_db['jira_data_closed']
    jira_data_open = my_db['jira_data_open']

    p1_jira("closed", jira_data_closed)
    p1_jira("not closed", jira_data_open)
