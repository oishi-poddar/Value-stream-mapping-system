import requests
import pymongo
import errno,sys
import config
import ssl
import json



# input format
# 0:scriptname 1:username 2:password
def p1_snow(mycol):
    program_name = sys.argv[0]
    arguments = sys.argv[1:]
    lst = []
    if len(sys.argv)==2 and sys.argv[1]=='--help':
        print(__doc__)
    elif len(sys.argv) < 2:
        print("Error in input arguments!")
        print(__doc__)
    else:
        url = 'https://autodeskcloudops.service-now.com/api/now/table/change_request'
        user = sys.argv[1]
        pwd = sys.argv[2]

        
        # Set proper headers
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        
        PARAMS = {'sysparm_query':'sys_created_onONLast 2 years@javascript:gs.beginningOfLast2Years()@javascript:gs.endOfLast2Years()^cmdb_ciLIKEA360',
                'sysparm_limit' :'15000', 'sysparm_display_value':'all',
                'sysparm_fields':'number,sys_updated_on,state,u_jira_key,conflict_status,closed_at,work_end,calendar_duration,risk_value,parent,type,category,'
                                 'sys_mod_count,delivery_plan,priority,review_date,approval,opened_at,work_start,phase,u_environment,u_approval_phase'}

        response = requests.get(url, auth=(user,pwd), headers=headers, params=PARAMS)

        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            sys.exit(errno.EACCES)

        # Decode the JSON response into a dictionary and use the data
        data = response.json()     #data dictionary
        #data1 = json.dumps(data)   #converting to json string


        # with open('cm.json', 'w') as outfile:
        #     json.dump(data, outfile, sort_keys = True, indent = 4)


        num1=0
        if mycol.count_documents({}) > 0:
            str_num1 = mycol.find().sort('number',-1)[0]['number']['value']
            num1=int(''.join(list(filter(str.isdigit, str_num1))))

        for n in data['result']:
            dd=n['number']['value']
            num=int(''.join(list(filter(str.isdigit, dd))))

            if num <= num1:
                break
            mycol.insert_one(n)
        print("total documents:",mycol.count_documents({}))

server= config.server
database=config.mongodb['dbname']
client = pymongo.MongoClient(server, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
lst1 = []
mydb1 = client[database]
mycol1 = mydb1["snow_change_mng_data"]
p1_snow(mycol1)
