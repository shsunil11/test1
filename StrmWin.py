# First run the nc -lk command as follows from one terminal
# nc -lk localhost 7777
# Then submit this application as follows from another terminal
# spark-submit --master local[2] StrmWin.py 10

import sys

from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext

conf = SparkConf().setAppName("Streaming Sliding Window")

sc = SparkContext(conf = conf)
sc.setLogLevel("WARN")

#sys.argv[1] is the first command line parameter which is the batchInterval
batchInterval = int(sys.argv[1])

ssc = StreamingContext(sc, batchInterval)

lines = ssc.socketTextStream("localhost", 7777)

ssc.checkpoint("/user/cloudera/streamcp")
users = lines.flatMap(lambda x: x.split(" "))

userPairs = users.map(lambda x: (x,1))

userPairs.pprint()

# Window Duration = 4 times batchInterval  and Slide Duration = 2 times batchInterval
winCount = userPairs.reduceByKeyAndWindow(lambda x,y:x+y, lambda x,y:x-y, 4*batchInterval, 2*batchInterval)

# This function prints the 20 elements from the input rdd
def winSorted(rdd):
   print "Printing Window foreach Sorted RDD"
   for lines in rdd.take(20):
      print lines[1] + ", " + str(lines[0])

# Sort by descending order of the value (value = count in this case)
winTrans = winCount.map(lambda (x,y) : (y,x)).transform(lambda rdd: rdd.sortByKey(False))

#For each rdd print the 20 elements
winTrans.foreachRDD(winSorted)

ssc.start()

ssc.awaitTermination()
