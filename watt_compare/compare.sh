#!/bin/bash

rm -f data/*
date +%s > ./data/start.log
nvidia-smi --query-gpu=timestamp,power.draw --format=csv -lms 100 -f data/nvidia.csv &
STARPU_NCUDA=0 likwid-perfctr -c 0,1 -g PWR_PKG_ENERGY:PWR0,PWR_DRAM_ENERGY:PWR3 -t 1s -o ./data/out "./chameleon_dtesting -H -o gemm -n 25000 -g 0"
#likwid-perfctr -f -c 0,1 -g ENERGY -t 100ms -o ./data/out "sleep 20"
date +%s > ./data/end.log

pkill "nvidia-smi"
