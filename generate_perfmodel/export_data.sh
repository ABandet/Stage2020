#!/bin/bash


gemm_model_s0=$(head -n 1 $HOME/for_model/gemm-s0-$NB)
gemm_model_s1=$(head -n 1 $HOME/for_model/gemm-s1-$NB)
trsm_model_s0=$(head -n 1 $HOME/for_model/trsm-s0-$NB)
trsm_model_s1=$(head -n 1 $HOME/for_model/trsm-s1-$NB)
syrk_model_s0=$(head -n 1 $HOME/for_model/syrk-s0-$NB)
syrk_model_s1=$(head -n 1 $HOME/for_model/syrk-s1-$NB)

export STARPU_POTRF_ENERGY_S0=$potrf_model_s0
export STARPU_POTRF_ENERGY_S1=$potrf_model_s1
export STARPU_GEMM_ENERGY_S0=$gemm_model_s0
export STARPU_GEMM_ENERGY_S1=$gemm_model_s1
export STARPU_TRSM_ENERGY_S0=$trsm_model_s0
export STARPU_TRSM_ENERGY_S1=$trsm_model_s1
export STARPU_SYRK_ENERGY_S0=$syrk_model_s0
export STARPU_SYRK_ENERGY_S1=$syrk_model_s1
