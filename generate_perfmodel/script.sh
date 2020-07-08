#!/bin/bash


MODEL_DIR=$HOME/perf_model
IN_FILE=$PWD/data/in.log
KERNEL=syrk_batch
CHAMELEON_EXEC=$HOME/chameleon/build/testing/chameleon_dtesting

SCALE=6

MIN_NB=300
MAX_NB=700
NT=43

for NB in `seq $MIN_NB 50 $MAX_NB`
do
    echo Starting execution for NT=$NT and NB=$NB
    $CHAMELEON_EXEC -H -o $KERNEL -n $NB -i 1 -b $(( $NT * $NT * ($NT-1) / 2  )) --nowarmup > $IN_FILE
    if [ $? -eq 0 ]
    then
        cpu_pwr_s0=$(cat $IN_FILE | grep rapl:::PACKAGE_ENERGY:PACKAGE%d | head -n 1 | gawk '{ print $2 }'  )
        ram_pwr_s0=$(cat $IN_FILE | grep rapl:::DRAM_ENERGY:PACKAGE%d | head -n 1 | gawk '{ print $2 }'  )
	total_pwr_s0=$(echo "scale=$SCALE; $cpu_pwr_s0 + $ram_pwr_s0" | bc)
	echo "scale=$SCALE; $total_pwr_s0 / (($NT * $NT * ($NT-1)) / 2)" | bc | tee $MODEL_DIR/$KERNEL-s0-$NB-$default

	cpu_pwr_s1=$(cat $IN_FILE | grep rapl:::PACKAGE_ENERGY:PACKAGE%d | tail -n 1 | gawk '{ print $2 }'  )
        ram_pwr_s1=$(cat $IN_FILE | grep rapl:::DRAM_ENERGY:PACKAGE%d | tail -n 1 | gawk '{ print $2 }'  )
        total_pwr_s1=$(echo "scale=$SCALE; $cpu_pwr_s1 + $ram_pwr_s1" | bc)
        echo "scale=$SCALE; $total_pwr_s1 / (($NT * $NT * ($NT-1)) / 2)" | bc | tee $MODEL_DIR/$KERNEL-s1-$NB-$default
    else
	break 1
    fi
done

