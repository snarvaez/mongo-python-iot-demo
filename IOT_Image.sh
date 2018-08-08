for i in {1..1000000}
do
  mgeneratejs -n 200 IOT_Image.json | python IOT_BulkInsertWithRetry.py "mongodb://localhost:27017" IOT DeviceData
  sleep 2
done
