#!/usr/bin/env python
import os
import pymongo
import ssl

mongodb = {
    'dbhost': "tvsm-c-uw2.cluster-ct0dqhwv5tkr.us-west-2.docdb.amazonaws.com",
    'dbport': "27017",
    'username': "root",
    'password': "",
    'dbname': 'thunder',
    'dbauthSource': "admin",
}
# server1 = "mongodb://" + mongodb['dbhost'] + ":" + str(mongodb['dbport']) + "/"
# client1 = pymongo.MongoClient(server1)
server = "mongodb://" + mongodb['username'] + ":" + mongodb['password'] + "@" + mongodb['dbhost'] + ":" + mongodb[
    'dbport'] + "/?ssl=true&authSource=" + mongodb['dbauthSource']
client = pymongo.MongoClient(server, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)

