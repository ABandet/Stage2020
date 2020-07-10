#!/bin/bash


MODEL_DIR=$HOME/for_model
IN_FILE=$PWD/data/in.log
KERNELS=('potrf_batch' "syrk_batch" 'gemm_batch' 'trsm_batch')
CHAMELEON_EXEC=$HOME/chameleon/build/testing/chameleon_dtesting

SCALE=6

MIN_NB=300
MAX_NB=1000

for KERNEL in ${KERNELS[@]}
do
    KERNEL_NAME=$(echo $KERNEL | awk 'BEGIN{FS="_batch"} { print $1 }')
    for NB in `seq $MIN_NB 25 $MAX_NB`
    do
        for NT in `seq 40 2 40`
        do
            echo Starting execution for NT=$NT and NB=$NB with kernel $KERNEL
            $CHAMELEON_EXEC -H -o $KERNEL -n $NB -i 1 -b $(( $NT * $NT * ($NT-1) / 2  )) --nowarmup > $IN_FILE
            if [ $? -eq 0 ]
            then
                cpu_pwr_s0=$(cat $IN_FILE | grep rapl:::PACKAGE_ENERGY:PACKAGE%d | head -n 1 | gawk '{ print $2 }'  )
                ram_pwr_s0=$(cat $IN_FILE | grep rapl:::DRAM_ENERGY:PACKAGE%d | head -n 1 | gawk '{ print $2 }'  )
	        total_pwr_s0=$(echo "scale=$SCALE; $cpu_pwr_s0 + $ram_pwr_s0" | bc)
	        echo "scale=$SCALE; $total_pwr_s0 / (($NT * $NT * ($NT-1)) / 2)" | bc | tee $MODEL_DIR/$KERNEL_NAME-s0-$NB

                cpu_pwr_s1=$(cat $IN_FILE | grep rapl:::PACKAGE_ENERGY:PACKAGE%d | tail -n 1 | gawk '{ print $2 }'  )
                ram_pwr_s1=$(cat $IN_FILE | grep rapl:::DRAM_ENERGY:PACKAGE%d | tail -n 1 | gawk '{ print $2 }'  )
                total_pwr_s1=$(echo "scale=$SCALE; $cpu_pwr_s1 + $ram_pwr_s1" | bc)
                echo "scale=$SCALE; $total_pwr_s1 / (($NT * $NT * ($NT-1)) / 2)" | bc | tee $MODEL_DIR/$KERNEL_NAME-s1-$NB  
            else
	        break 1
            fi
        done
    done
done
	      

