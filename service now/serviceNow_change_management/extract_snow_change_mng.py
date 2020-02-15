import pymongo
import datetime
from datetime import timedelta
import json
import sys
import config
import ssl

def p2_snow(env):
    server= config.server
    database=config.mongodb['dbname']
    myclient = pymongo.MongoClient(server, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)

    #myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    lst1 = []
    mydb1 = myclient[database]
    mycol1 = mydb1["snow_change_mng_data"]

    # for record in mycol1.find():
    #     environ = record['u_environment']['value'].lower()
    #     if(environ==env):
    #         lst1.append(record)

    for record in mycol1.find({ "u_environment.value": env}):
        lst1.append(record)


    print(len(lst1))
    dict_approval = {}
    dict_state={}
    dict_environment={}
    dict_jira_key ={}
    dict_phase ={}
    dict_type = {}
    dict_category = {}
    dict_conflict_status = {}
    dict_priority = {}
    dict_approval_phase = {}

    dict_category_duration = {}
    dict_cat_dur = {}
    total_count=0
    total_duration=0
    delta=0
    env_count=len(lst1)
    for item in lst1:
        category = item['category']['value']
        # environ = item['u_environment']['value'].lower()
        # if(environ==env):
        #     env_count+=1
        if item['approval']['value'] in dict_approval:
            dict_approval[item['approval']['value']] += 1
        else:
            dict_approval[item['approval']['value']] = 1


        if item['u_approval_phase']['value'] in dict_approval_phase:
            dict_approval_phase[item['u_approval_phase']['value']] += 1
        else:
            dict_approval_phase[item['u_approval_phase']['value']] = 1

        if item['state']['display_value'] in dict_state:
            dict_state[item['state']['display_value']] += 1
        else:

            dict_state[item['state']['display_value']] = 1


        if item['u_environment']['value'] in dict_environment:
            dict_environment[item['u_environment']['value']] += 1
        else:

            dict_environment[item['u_environment']['value']] = 1



        if item['u_jira_key']['value'] in dict_jira_key:
            dict_jira_key[item['u_jira_key']['value']] += 1
        else:
            dict_jira_key[item['u_jira_key']['value']] = 1


        if item['phase']['value'] in dict_phase:
            dict_phase[item['phase']['value']] += 1
        else:
            dict_phase[item['phase']['value']] = 1

        if item['type']['value'] in dict_type:
            dict_type[item['type']['value']] += 1
        else:
            dict_type[item['type']['value']] = 1

        if item['category']['value'] in dict_category:
            dict_category[item['category']['value']] += 1
        else:
            dict_category[item['category']['value']] = 1

        if item['conflict_status']['value'] in dict_conflict_status:
            dict_conflict_status[item['conflict_status']['value']] += 1
        else:
            dict_conflict_status[item['conflict_status']['value']] = 1

        if item['priority']['value'] in dict_priority:
            dict_priority[item['priority']['value']] += 1
        else:
            dict_priority[item['priority']['value']] = 1





        if len(item['closed_at']['value'] and item['opened_at']['value']):

            closed_at = item['closed_at']['value']
            opened_at = item['opened_at']['value']
            datetimeFormat = '%Y-%m-%d %H:%M:%S'
            diff = datetime.datetime.strptime(closed_at, datetimeFormat)- datetime.datetime.strptime(opened_at, datetimeFormat)
            days=diff.days*86400
            seconds=diff.seconds
            duration=days+seconds
            # total_duration+=duration
            # total_count+=1

        if category not in dict_category_duration.keys():
            dict_category_duration[category] = duration
        else:
            value = dict_category_duration.get(category)
            dict_category_duration[category] = duration + value



    for key in dict_category_duration:
        dict_category_duration[key] = str(dict_category_duration.get(key) / dict_category[key])

    for key in dict_category:
        dict_cat_dur[key] ={
            "count": dict_category[key],
            "avg_duration": dict_category_duration[key]
        }




    # if(total_count == 0):
    #     avg_duration=0
    # else:
    #     avg_duration=total_duration/total_count


    env1="total "+env+" environment"
    mydict1 ={
        "States": dict_state,
        "jira_key": dict_jira_key,
        "Type": dict_type,
        "Category": dict_category,
        "Conflict_status": dict_conflict_status,
        "Approval": dict_approval,
        "Priority": dict_priority,
        "Approval_phase": dict_approval_phase,
        "Phase": dict_phase,
        #"Average_duration": avg_duration,
        "Average_duration_per_category" : dict_cat_dur,
        env1:env_count,

    }



    #print(mydict1)
    return mydict1


#env="Staging"
#p2_snow(env)
