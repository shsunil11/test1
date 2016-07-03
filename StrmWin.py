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

winCount = userPairs.reduceByKeyAndWindow(lambda x,y:x+y, lambda x,y:x-y, 4*batchInterval, 2*batchInterval)

def winRDD(rdd):
   print "Printing foreach RDD"
   for lines in rdd.takeOrdered(20, lambda (x,y): (-y,x)):
      print lines
      
#winCount.foreachRDD(winRDD)

def winSorted(rdd):
   print "Printing foreach Sorted RDD"
   for lines in rdd.take(20):
      print lines[1] + ", " + str(lines[0])

winTrans = winCount.map(lambda (x,y) : (y,x)).transform(lambda rdd: rdd.sortByKey(False))
winTrans.foreachRDD(winSorted)

ssc.start()

ssc.awaitTermination()x`xx
