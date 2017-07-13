# First run the nc -lk command as follows from one terminal
# nc -lk localhost 7777
# Then submit this application as follows from another terminal
# spark-submit --master local[2] StrmUpd.py 10

import sys

from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext

conf = SparkConf().setAppName("Streaming UpdateByKey")

sc = SparkContext(conf = conf)
sc.setLogLevel("WARN")

# sys.argv[1] is the first command line parameter which is batchInterval
batchInterval = int(sys.argv[1])

ssc = StreamingContext(sc, batchInterval)

lines = ssc.socketTextStream("localhost", 7777)

ssc.checkpoint("/user/cloudera/streamcp")
users = lines.flatMap(lambda x: x.split(" "))

userPairs = users.map(lambda x: (x,1))

userPairs.pprint()

# In the updateFunc, values is the values of a key in this batch and runningCount is the current state of the key
# The current state of the key is maintained as the running count of the key
def updateFunc(values, runningCount):
   if runningCount is None:
      runningCount = 0

   return sum(values) + runningCount
   userState = userPairs.updateStateByKey(updateFunc)

# Save each batch to HDFS (folder will be created if it does not exist
# "txt" is the suffix of the folder
userState.saveAsTextFiles("/user/cloudera/streamOut","txt")

# for each rdd print the top 20 elements in descendin order of the value (value = count in this case)
def winRDD(rdd):
   print "Printing Updated foreach RDD"
   for lines in rdd.takeOrdered(20, lambda (x,y): (-y,x)):
      print lines

userState.foreachRDD(winRDD)

ssc.start()

ssc.awaitTermination()
