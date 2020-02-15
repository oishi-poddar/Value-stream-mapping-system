import requests
import pymongo
import json
import errno,sys
import json
import config
import ssl



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
        url = 'https://autodeskcloudops.service-now.com/api/now/table/incident'
        user = sys.argv[1]
        pwd = sys.argv[2]

        #sys_created_onONLast 2 years@javascript:gs.beginningOfLast2Years()@javascript:gs.endOfLast2Years()^GOTOcmdb_ci.nameLIKEA360
        #cmdb_ci=011f2fa16f73d100afea07321c3ee4d8 :configuration item(A360)   (^cmdb_ci=011f2fa16f73d100afea07321c3ee4d8)

        # Set proper headers
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        PARAMS = {'sysparm_query':'sys_created_onONLast 2 years@javascript:gs.beginningOfLast2Years()@javascript:gs.endOfLast2Years()^GOTOcmdb_ci.nameLIKEA360',
                'sysparm_limit' :'20000', 'sysparm_display_value':'all',
                'sysparm_fields':'number,cmdb_ci,close_notes,description, severity,u_mttd,u_mttr,'
                                'u_mttc,u_proximate_cause_category,caused_by,u_accountable_party'}

        response = requests.get(url, auth=(user,pwd), headers=headers, params=PARAMS)

        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            sys.exit(errno.EACCES)

        # Decode the JSON response into a dictionary and use the data
        data = response.json()     #data dictionary
        #data1 = json.dumps(data)   #converting to json string


        num1=0
        lst=[]
        if mycol.count_documents({}) > 0:
            str_num1 = mycol.find().sort('number',-1)[0]['number']['value']
            num1=int(''.join(list(filter(str.isdigit, str_num1))))

        for n in data['result']:
            dd=n['number']['value']
            config_env=n['cmdb_ci']['display_value'].split("-")[-1].lower().lstrip()
            num=int(''.join(list(filter(str.isdigit, dd))))
            n['environment']=config_env

            if num <= num1:
                break
            mycol.insert_one(n)

        print("total documents:",mycol.count_documents({}))



server= config.server
database=config.mongodb['dbname']
client = pymongo.MongoClient(server, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
mydb = client[database]
mycol = mydb["snow_data"]
p1_snow(mycol)
