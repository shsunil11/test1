# First run the nc -lk command as follows from one terminal
# nc -lk localhost 7777
# Start pyspark as follows from another
# pyspark --master local[2]
# Then Execute the following from pyspark from another terminal


from pyspark.streaming import StreamingContext

ssc = StreamingContext(sc, batchInterval)

lines = ssc.socketTextStream("localhost", 7777)

users = lines.flatMap(lambda x: x.split(" "))
userPairs = users.map(lambda x: (x,1))
counts = userPairs.reduceByKey(lambda x,y: x + y)
counts.pprint()

ssc.start()

