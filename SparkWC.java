package com.aaa.SparkProj.WC;

import java.util.Arrays;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.*;
import org.apache.spark.api.java.function.*;
import scala.Tuple2;

public class JavaWC {
	
	public static void main(String[] args) {
		SparkConf conf = new SparkConf().setAppName("WC App");
		JavaSparkContext sc = new JavaSparkContext(conf);
		
		JavaRDD<String> lines = sc.textFile(args[0]);
		
		JavaRDD<String> words = lines.flatMap(
		   new FlatMapFunction<String,String>() {
			   public Iterable<String> call(String x) {
				   return Arrays.asList(x.split(" "));
			   }
		   }
	    );

		JavaPairRDD<String,Integer> pairs = words.mapToPair(
	       new PairFunction<String, String, Integer>() {
	    	   public Tuple2<String, Integer> call(String x) {
	    		   return new Tuple2(x, 1);
	    	   }
	       }
		);
		
		JavaPairRDD<String,Integer> counts = pairs.reduceByKey(
			       new Function2<Integer, Integer, Integer>() {
			    	   public Integer call(Integer x, Integer y) {
			    		   return x + y;
			    	   }
			       }
		);
		
		for (Tuple2<String, Integer> t : counts.collect()) {
			System.out.println(t._1 + "," + t._2);
		}
		
        sc.stop();
		
	}

}
