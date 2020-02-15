"""This script is used to access the data fetched using the JIRA API and perform required manipulations on it.
The script calculates:
dict_resolve_time : dictionary mapping issue type to average resolution time
list_id_closed: lists of closed issues
list_issueType : list of issue types
dict_issueType: count of every issue type
Other data can be fetched and calculated according to need
"""

from collections import Counter
import json
import datetime
import config
import pymongo
import json


def p2_jira(status):
    my_db = config.client[config.mongodb['dbname']]
    my_col = my_db['jira_data_' + status]
    issues = my_col.find({})
    issue_type = {}
    list_issueType = []
    list_status = []
    list_open = []
    list_id_closed = []
    list_id_closed_RT = []
    dict_resolve_time = {}
    new_dict_resolve_time = {}

    for i in issues:
        # print(i)
        created = i['created']
        created = created.split(".")
        created_date = datetime.datetime.strptime(created[0], '%Y-%m-%dT%H:%M:%S')
        resolutionDate = i['resolutiondate']
        status = i['status']
        IT = i['issuetype']
        if resolutionDate != None:

            resolutionDate = resolutionDate.split(".")
            resolved_date = datetime.datetime.strptime(resolutionDate[0], '%Y-%m-%dT%H:%M:%S')
            resolution_time = resolved_date - created_date  # time to resolve closed jira issue
            if IT not in dict_resolve_time.keys():
                dict_resolve_time[IT] = resolution_time
            else:
                value = dict_resolve_time.get(IT)
                dict_resolve_time[IT] = resolution_time + value
            list_id_closed.append(i['_id'])  # list of closed issues
            list_id_closed_RT.append(resolution_time)  # list of resolution times

        list_status.append(status)  # list of status
        list_issueType.append(IT)  # list of issue types
    count_issue_type = Counter(list_issueType)  # count of every issue type
    count_issue_status = Counter(list_status)  # count of every isssue status
    dict_issueType = dict((i, list_issueType.count(i)) for i in list_issueType)
    for key in dict_resolve_time:
        dict_resolve_time[key] = str(dict_resolve_time.get(key) / dict_issueType[
            key])  # dictionary containing the average resolution time per issue type
    dict_status = {}
    for k in count_issue_status.items():
        dict_status.update({k[0]: k[1]})
    data = {
        "status": dict_status,
        "issueType": dict_issueType,
        "resolve_time": dict_resolve_time
    }
    # print(data)
    return data


# data={
#     'closed':p2_jira('closed'),
#     'open':p2_jira('open'),
# }
# with open("data.json", "w") as f:
#     json.dump(data, f, indent=4)