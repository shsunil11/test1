from pyspark.sql import Row

sc.setLogLevel("WARN")

lines = sc.textFile("/user/cloudera/ssql/ssql_data.txt")

cols = lines.map(lambda x: x.split(","))

rows = cols.map(lambda x: Row(name=x[0], age=int(x[1])))

peopleTable = rows.toDF()

peopleTable.rdd.saveAsTextFile("/user/xx62883/ssql/peopleTableTxt")

peopleTable.registerTempTable("people")

oldp = sqlCtx.sql("select name, age from people where age > 40")

sqlCtx.registerFunction("makeLower", lambda x: x.lower())
sqlCtx.sql("select makeLower(name) as nm , age from people").show()

oldp.select(oldp.name, (oldp.age+10).alias('age10')).show(5)

oldp5 = oldp.select( "name","age").withColumn("age5", oldp['age']+5)
oldp5.write.saveAsTable("bdahd01d_dledl_hbase_poc.oldp1")

# Preferred - Using DataFrame.write
# sqlContext.setConf("spark.sql.parquet.compression.codec","snappy")  for snappy. Default is gzip
# sqlContext.refreshTable("my_table")  refreshes Metadata in Spark from Hive
ooldp.write.save("/user/xx62883/ssql/newPrq", format = "parquet", mode='overwrite')
oldp.write.saveAsTable("bdahd01d_dledl_hbase_poc.oldp55", format = "parquet", mode='overwrite')

oldpTrans = oldp.map(lambda x: x.name + " is old with age " + str(x.age))
oldpTrans.take(10)

#oldpName is DataFrame
oldpName = oldp.select("name")

oldp.write.format("parquet").save("/user/cloudera/ssql/row.prq")


prqIn = sqlCtx.read.parquet("/user/cloudera/ssql/row.prq")

#prqIn is DataFrame       DataFrame[name: string, age: bigint]

prqIn.write.json("/user/cloudera/ssql/ssql_json")

# RDD of String (String contains valid JSON Data) can also be passed to read.json
jsonIn = sqlCtx.read.json("/user/cloudera/ssql/ssql_json")

# Use read.option("mergeSchema","true") to merge Parquet Schemas of input files
#  OR set spark.sql.parquet.mergeSchema to true

# Partition columns are inferred by read parquet

# Saves with dynamic Partitioning
# pdf.write.partitionBy("age").format("parquet").mode(SaveMode.Overwrite).save("/user/xx62883/ssql/newPrqPart")

############################################################################################
# JDBC
# JdbcRDD deprecated.
# Create a DataFrame using sqlContext.read.format('jdbc').options(url='jdbcurl',dbtable='db.table or query').load()
# Other options are driver, (partitionColumn, lowerBound,upperBound,numPartitions)  and fetchSize
############################################################################################
