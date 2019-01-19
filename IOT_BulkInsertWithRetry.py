import pymongo, json
import sys, time, datetime

# ================
# DB IOT
# COLL DeviceData, Capped = 2102400 2TB
# ================
connStr= sys.argv[1]
dbName= sys.argv[2]     # IOT
collName= sys.argv[3]   # DeviceData

client= pymongo.MongoClient(connStr, retryWrites=True)
db= client[dbName]
coll= db[collName]

print("CONNECTED")

bulk= []
while 1:
   try:
       post= sys.stdin.readline()
   except KeyboardInterrupt:
       break
   if not post:
       break

   post= post.replace("$date","date")
   j= json.loads(post)
   bulk.append(pymongo.InsertOne(j))

for retry in [3, 5, 7, 13, 17]: #exponential back-off & retry
    try:
        result= coll.bulk_write(bulk)
        print(result.bulk_api_result)
        break

    except Exception as e: #pymongo.errors.BulkWriteError
        print("EXCEPTION: ", e)
        print("Sleeping for ", retry, " seconds and then retrying...")
        time.sleep(retry)

client.close()
