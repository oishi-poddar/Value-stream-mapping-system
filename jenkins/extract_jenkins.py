"""
This script is used to access the data fetched using the Jenkins API and perform required manipulations on it.
Expected arguments are : [filename to be run, json_file(from which data is to be fetched),filename in which data to be stored]
"""

import sys
import config


def p2_jenkins():
    no_of_builds = collection.count_documents({})
    builds = collection.find()
    count_stage = 0
    dict_stage = {}
    data_json = {}
    count_successful_builds = 0
    list_duration = []
    list_final = []
    for b in builds:
        for s in b['stages']:

            stage_name = s['name']
            if stage_name not in dict_stage.keys():
                dict_stage[stage_name] = count_stage
            if s["name"] == "Deploy" and s["status"] == "SUCCESS":
                list_duration.append(b["durationMillis"])
                count_successful_builds += 1
            if s["status"] == "FAILED":
                stage_failed = s["name"]
                count_stage = dict_stage.get(stage_failed)
                dict_stage[stage_failed] = count_stage + 1

    no_of_stages = len(dict_stage)
    sum_duration_successful_builds = sum(list_duration)
    avg_duration_successful_builds = sum_duration_successful_builds / count_successful_builds
    success_ratio = float(count_successful_builds) / float(no_of_builds)
    dict_stage.update({'id': 2})
    data_json = {
        "id": 1,
        "Total number of stages": no_of_stages,
        "no_of_builds": no_of_builds,
        "no of successful builds": count_successful_builds,
        "average duration of successful builds": avg_duration_successful_builds * 0.001,  # in seconds
        "success ratio": success_ratio * 100,
        "Number of failures": no_of_builds - count_successful_builds
    }
    return data_json

    # collection_jenkins_output1.replace_one({'id': 1},data_json,upsert=True) #to insert only if a new document id is found and to keep replacing the old document
    # collection_jenkins_output1.replace_one({'id':2},dict_stage,upsert=True)


db = config.client[config.mongodb['dbname']]
collection = db['jenkins_data']
# collection_jenkins_output1=db['data_extract_Jenkins']
