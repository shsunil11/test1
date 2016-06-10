package com.mycom.kafkatest.generator;

import java.util.*;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.io.*;

import org.apache.hadoop.conf.*;
import org.apache.hadoop.fs.*;

public class HDFSKProd {

    public static void main(String[] args) {

        String topic = args[1];
        int batchSize = Integer.parseInt(args[2]);
        long sleepIntervalMillis = Long.parseLong(args[3]);
        int maxTrans = Integer.parseInt(args[4]);
        
        FSDataInputStream  eventStream = null;

        Properties kafkaProps = new Properties();
        KafkaProducer producer;
        
        kafkaProps.put("bootstrap.servers", "brokerHost:9092");
        kafkaProps.put("metadata.broker.list", "brokerHost:9092");

        // This is mandatory, even though we don't send keys
        kafkaProps.put("key.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");
        kafkaProps.put("value.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");
        kafkaProps.put("acks", "0");

        // how many times to retry when produce request fails?
        kafkaProps.put("retries", "3");
        kafkaProps.put("linger.ms", 2);
        kafkaProps.put("batch.size", 1000);
        kafkaProps.put("queue.time", 2);

        producer = new KafkaProducer(kafkaProps);
       
        if (eventStream == null) {
          try {
              Configuration conf = new Configuration();
              ("fs.hdfs.impl.disable.cache",true);
              Path pt = new Path(args[0]);
              
              FileSystem hdfs  = FileSystem.get(conf);
              
              eventStream = hdfs.open(pt);
              
          }
          catch (IOException e){
                e.printStackTrace();;
          }
        }

        int i = 0;
        try {
           byte buffer[] = new byte[800];

           while (eventStream.read(i*800,buffer,0,800) > 0) {
               i++;
              
               ProducerRecord record = new ProducerRecord(topic, buffer );
               producer.send(record);
               
               if (i > maxTrans) {
            	   System.out.println("Exiting at i= " + i);
            	   break;
               }
               if (i % batchSize == 0) {
            	   System.out.println("Sleeping at i= " + i);
            	   try {
            		   Thread.sleep(sleepIntervalMillis);
            	   } catch(InterruptedException e) {
            		   e.printStackTrace();
            	   }
               }

           }

           eventStream.close();

           producer.close();
           } catch (IOException e) {
                   e.printStackTrace();
           }
    }


}
