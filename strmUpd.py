import sys

from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext

conf = SparkConf().setAppName("Python Streaming")

sc = SparkContext(conf = conf)
sc.setLogLevel("WARN")

batchInterval = int(sys.argv[1])

ssc = StreamingContext(sc, batchInterval)

lines = ssc.socketTextStream("lbdp167a", 7777)

ssc.checkpoint("/user/xx62883/streamcp")
users = lines.flatMap(lambda x: x.split(" "))

userPairs = users.map(lambda x: (x,1))

userPairs.pprint()

def updateFunc(values, runningCount):
   if runningCount is None:
      runningCount = 0

   return sum(values) + runningCount
   userState = userPairs.updateStateByKey(updateFunc)

userState.saveAsTextFiles("/user/xx62883/streamOut","txt")

def winRDD(rdd):
   print "Printing foreach RDD"
   for lines in rdd.takeOrdered(20, lambda (x,y): (-y,x)):
      print lines

userState.foreachRDD(winRDD)

ssc.start()

ssc.awaitTermination()
