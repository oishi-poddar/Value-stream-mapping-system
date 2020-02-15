"""
Using the package 'python-jenkins'
https://python-jenkins.readthedocs.io/en/latest/examples.html
To get data from the Pipeline View plugin in Jenkins, using it's REST API
https://github.com/jenkinsci/pipeline-stage-view-plugin/tree/master/rest-api#get-jobjob-namewfapiruns
Expected input arguments are: [filename to be run, username, password, master node,job name]

"""
import requests
import jenkins
import sys
import pymongo
import config



def p1_jenkins(collection,username,pwd,master_node,JobName,job_url):

    server = jenkins.Jenkins("https://"+master_node+".jenkins.autodesk.com", username=username, password=pwd)
    print(server)
    job=server.get_job_info(JobName, fetch_all_builds=True) #information of all builds of the particular job specified
    list1=[]
    count=0
    d=0
    if collection.count_documents({}) > 0:
        d = collection.find().sort('id', -1)[0]['id'] #to find the latest build id
    for j in job['builds']: #to fetch the data for every stage for every build

        build_number=str(j['number'])

        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        url =job_url + build_number + "/wfapi/changesets"
        response = requests.get(url, auth=(username, pwd), headers=headers)
        data1 = response.json()
        url = job_url+ build_number + "/wfapi/describe"
        response = requests.get(url, auth=(username, pwd), headers=headers)
        data = response.json()

        try:
            data['changeset'] = data1[0]
        except IndexError:
            data['changeset'] = None
        if data['id']<=d: break #to insert only if a new build occurs
        collection.insert_one(data)
    print("The count of builds are:",collection.count_documents({}))
    print(count)





server=config.server
db=config.mongodb['db']
client=pymongo.MongoClient(server)
db = client[db]
collection = db['jenkins_data']

program_name = sys.argv[0]
username=sys.argv[1]
pwd=sys.argv[2]
master_node=sys.argv[3] #master-2
job_name=sys.argv[4]    #A360/Galileo-Web/master
job_url=sys.argv[5] #https://master-2.jenkins.autodesk.com/job/A360/job/Galileo-Web/job/master/
if len(sys.argv)==2 and sys.argv[1]=='--help':
    print(__doc__)
else:
    p1_jenkins(collection,username,pwd,master_node,job_name,job_url)