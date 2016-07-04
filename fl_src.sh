#!/bin/bash
i=0
while true
do
   if [ -f /tmp/ctl.txt ]
   then
      i=$((i+1))
      echo "This is Line ${i} " >> /tmp/flm/f1.log
      rem=$(($i % 100))
      if [ ${rem} -eq 0 ]
      then
         echo " 100 Records reached"
         sleep 3
      fi
   else
      exit 0
   fi
done
