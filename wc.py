from pyspark import SparkConf, SparkContext
import sys

conf = SparkConf()

sc = SparkContext(conf = conf)

lines = sc.textFile(sys.argv[1])

words = lines.flatMap(lambda line:  line.split(" ")).map(lambda word: (word,1)).reduceByKey(lambda x, y: x+y)

for line in words.take(10):
   print line
   
for wc in words.collect():
   print wc[0] + " = " + str(wc[1])


sc.stop()
