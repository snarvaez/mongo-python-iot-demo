import pymongo, json
import sys, time, datetime
import logging

# ================
# DB IOT
# Listen COLL DeviceData
# Write COLL DeviceDataPermanent
# ================
connStr= sys.argv[1]
dbName= sys.argv[2]             # IOT
collListenName= sys.argv[3]     # DeviceData
collWriteName= sys.argv[4]      # DeviceDataPermanent

client= pymongo.MongoClient(connStr, retryWrites=True)
db= client[dbName]
collListen= db[collListenName]
collWrite= db[collWriteName]

print("CONNECTED")

try:
    with collListen.watch(
        # Watch inserts with only one element in payload.processingHistory
        # Insert into permanent collection
        [{'$match': {'$and': [
            {'operationType': 'insert'},
            {'$expr' : {'$eq' : [ {'$size': '$fullDocument.payload.processingHistory'}, 1]}}
        ]}}]
    ) as stream:

        for insert_change in stream:

            print("INSERTING INTO PERMANENT COLLECTION")
            print(insert_change)

            collWrite.update({'_id':insert_change['_id']}, insert_change, upsert=True)

except Exception as e:
    print("EXCEPTION: ", e)

client.close()
