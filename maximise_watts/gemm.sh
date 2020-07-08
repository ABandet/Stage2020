#!/bin/bash

OUT_FILE=$PWD/data/gemm.csv
IN_FILE=$PWD/data/in.csv

# initial file configuration
echo 'NB,NT,TIME,POWER_CPU1,POWER_RAM1,POWER_CPU2,POWER_RAM2,POWER_GPU' > $OUT_FILE

for i in `seq 900 50 1200`
do
    for j in `seq 50 1 70`
    do
        echo "Starting with NB=$i and NT=$j"
        ./chameleon_dtesting -H -o gemm_batch -n $i -i 1 -b $(( $j *($j-2)*($j-1)/6  )) --nowarmup > $IN_FILE
        if [ $? -eq 0 ]
        then
            echo -n "$i,$j," >> $OUT_FILE
            cat $IN_FILE | grep dgemm_batch | gawk  'BEGIN{ORS=""} { print $19 }' >> $OUT_FILE
            echo -n "," >> $OUT_FILE
            cat $IN_FILE | grep rapl |  gawk 'BEGIN{ORS=","} { print $2 }' >> $OUT_FILE
            cat $IN_FILE | grep nvml |  gawk 'BEGIN{ORS=","} { print $2 }'| sed s/.$// >> $OUT_FILE
            echo "" >> $OUT_FILE
        else
            break 1
        fi
    done
done
