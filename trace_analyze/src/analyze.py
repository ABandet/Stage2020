import pandas as pd

DATA_PATH = 'profile.h5'


if __name__ == "__main__":
    print("Begin trace analyze")

    t = pd.read_hdf('profile.h5')
    gemm_data = t[t['name'] == 'dgemm']
    gemm_data = gemm_data[gemm_data['worker'] == 'w0']
    trsm_data = t[t['name'] == 'dtrsm']
    trsm_data = trsm_data[trsm_data['worker'] == 'w0']
    syrk_data = t[t['name'] == 'dsyrk']
    syrk_data = syrk_data[syrk_data['worker'] == 'w0']

    # GEMM
    try:
        gemm_begin = gemm_data.head(1).iloc[0]['begin']
        gemm_end = gemm_data.tail(1).iloc[0]['end']
        total_gemm_time =  gemm_end - gemm_begin

        dead_time = 0
        max_end = gemm_data.iloc[0]['end']
        for i in range(1, len(gemm_data)):
            begin = gemm_data.iloc[i]['begin']
            end = gemm_data.iloc[i]['end']
            # si la tache precedente est terminee
            if begin > max_end :
                dead_time += begin - max_end
                max_end = end

        total_gemm_time -= dead_time
    
        print("Total gemm time on GPU was {}.".format(total_gemm_time))

    except:
        print("No gemm data found")
        
    # TRSM
    try:
        trsm_begin = trsm_data.head(1).iloc[0]['begin']
        trsm_end = trsm_data.tail(1).iloc[0]['end']
        total_trsm_time =  trsm_end - trsm_begin

        dead_time = 0
        max_end = trsm_data.iloc[0]['end']
        for i in range(1, len(trsm_data)):
            begin = trsm_data.iloc[i]['begin']
            end = trsm_data.iloc[i]['end']
            # si la tache precedente est terminee
            if begin > max_end :
                dead_time += begin - max_end
                max_end = end

        total_trsm_time -= dead_time
    
        print("Total trsm time on GPU was {}.".format(total_trsm_time))
    except:
        print("No trsm data found")
        
    # SYRK
    try:
        syrk_begin = syrk_data.head(1).iloc[0]['begin']
        syrk_end = syrk_data.tail(1).iloc[0]['end']
        total_syrk_time =  syrk_end - syrk_begin

        dead_time = 0
        max_end = syrk_data.iloc[0]['end']
        for i in range(1, len(syrk_data)):
            begin = syrk_data.iloc[i]['begin']
            end = syrk_data.iloc[i]['end']
            # si la tache precedente est terminee
            if begin > max_end :
                dead_time += begin - max_end
                max_end = end

        total_syrk_time -= dead_time
    
        print("Total syrk time on GPU was {}.".format(total_syrk_time))
    except:
        print("No Syrk data found")

