import pymongo
import json
import sys
import config
import ssl

def p2_snow(env):

    server= config.server
    database=config.mongodb['dbname']
    client = pymongo.MongoClient(server, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
    lst1 = []
    mydb1 = client[database]
    mycol1 = mydb1["snow_data"]

    # for record in mycol1.find():
    #     config_env=record['cmdb_ci']['display_value'].split("-")[-1].lower().lstrip()
    #     if(env.startswith(config_env)):
    #         lst1.append(record)
    for record in mycol1.find({ "environment": env}):
        lst1.append(record)

    total_env_count=len(lst1)
    total_mttc=0
    total_mttd=0
    total_mttr=0
    total_count_mttc=0
    total_count_mttd=0
    total_count_mttr=0
    dict_acc = {}
    dict_pcc={}
    dict_severity={}
    for item in lst1:
        if item['u_accountable_party']['display_value'] in dict_acc:
            dict_acc[item['u_accountable_party']['display_value']] += 1
        else:
            dict_acc[item['u_accountable_party']['display_value']] = 1



        if item['severity']['display_value'] in dict_severity:
            dict_severity[item['severity']['display_value']] += 1
        else:

            dict_severity[item['severity']['display_value']] = 1


        # config_env=item['cmdb_ci']['display_value'].split("-")[-1].lower().lstrip()
        # if(env.startswith(config_env)):
        #     total_env_count+=1
        # if config_env in dict_env:
        #     dict_env[config_env]+=1
        # else:
        #     dict_env[config_env]=1


        if len(item['u_mttc']['value']):
            mttc = item['u_mttc']['value'].split(" ")
            mttc1=mttc[1].split(":")
            total_mttc+=int(mttc1[0])*3600+int(mttc1[1])*60+int(mttc1[2])
            total_count_mttc+=1
        if len(item['u_mttd']['value']):
            mttd = item['u_mttd']['value'].split(" ")
            mttd1=mttd[1].split(":")
            total_mttd+=int(mttd1[0])*3600+int(mttd1[1])*60+int(mttd1[2])
            total_count_mttd+=1
        if len(item['u_mttr']['value']):
            mttr = item['u_mttr']['value'].split(" ")
            mttr1=mttr[1].split(":")
            total_mttr+=int(mttr1[0])*3600+int(mttr1[1])*60+int(mttr1[2])
            total_count_mttr+=1



        if(item['u_proximate_cause_category']['display_value'] in dict_pcc):
            dict_pcc[item['u_proximate_cause_category']['display_value']] +=1
        else:
            dict_pcc[item['u_proximate_cause_category']['display_value']] =1




    if(total_count_mttc == 0):
        avg_mttc=0
    else:
        avg_mttc=total_mttc//total_count_mttc

    if(total_count_mttd == 0):
        avg_mttd=0
    else:
        avg_mttd=total_mttd//total_count_mttd

    if(total_count_mttr == 0):
        avg_mttr=0
    else:
        avg_mttr=total_mttr//total_count_mttr



    env1="total "+env+" environment"
    mydict1 ={
        "Accountable parties": dict_acc,
        "Proximate_causes": dict_pcc,
        "Severity": dict_severity,
        env1:total_env_count,
        "average_time_to_communicate(secs):": avg_mttc,
        "average_time_to_detect(secs):": avg_mttd,
        "average_time_to_resolve(secs):": avg_mttr,


    }

    #print(mydict1)
    return mydict1

#env="prod"
#env="stage"
#p2_snow(env)

