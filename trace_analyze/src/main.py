#!/usr/bin/env python3

import sys;
import numpy as np
import pandas as pd;
import h5py

if len(sys.argv) != 2:
    print ("please provide a paje file to analyze")
    exit(0)

input_file=open(sys.argv[1], "r");

def find_element_in_list(list, word):
    for i in range(len(list)):
        if list[i] == word:
            return i
    return -1

def get_next_line():
    while 1:
        line=input_file.readline();
        if(len(line) == 0):
            return None
        if len(line) > 1:
            line_split=line.split();
            return line_split;

completed_tasks={};
started_tasks={};
started_gpu_tasks={};
tasks_begin=[]
tasks_end=[]
tasks_workers=[]
workers_id=[]
tasks_name=[]
tasks_id=[]
list_tasks=[]
nodes=[]
df = pd.DataFrame();


nodes.append("dahu-8")

def update_stats(worker):

    task_name=started_tasks[worker]["task"];
    
    start_date=float(started_tasks[worker]["start_date"]);
    stop_date=float(started_tasks[worker]["stop_date"]);
    duration = stop_date-start_date;
    tasks_name.append(task_name);
    tasks_begin.append(start_date);
    tasks_end.append(stop_date);
    tasks_workers.append(worker);
    workers_id.append(int(worker.split("w")[1]));
    if(find_element_in_list(list_tasks, task_name) == -1):
        list_tasks.append(task_name)
        tasks_id.append(len(list_tasks))
    else:
        tasks_id.append(find_element_in_list(list_tasks, task_name) + 1)

def update_gpu_stats(worker):

    task_name=started_gpu_tasks[worker]["task"];
    
    start_date=float(started_gpu_tasks[worker]["start_date"]);
    stop_date=float(started_gpu_tasks[worker]["stop_date"]);
    duration = stop_date-start_date;
    tasks_name.append(task_name);
    tasks_begin.append(start_date);
    tasks_end.append(stop_date);
    tasks_workers.append(worker);
    workers_id.append(int(worker.split("w")[1]));
    if(find_element_in_list(list_tasks, task_name) == -1):
        list_tasks.append(task_name)
        tasks_id.append(len(list_tasks))
    else:
        tasks_id.append(find_element_in_list(list_tasks, task_name) + 1)
        
    # stat=completed_tasks.get(task_name);
    # if(stat == None):
    #     completed_tasks[task_name]={"name":task_name,
    #                                 "ntasks":0,
    #                                 "total_duration":0,
    #                                 "min":-1,
    #                                 "max":-1};
    #     stat = completed_tasks[task_name];
    # stat["ntasks"] += 1;
    # stat["total_duration"] += duration;
    # if(stat["min"]<0 or stat["min"] > duration):
    #     stat["min"] = duration;

    # if(stat["max"]<0 or stat["max"] < duration):
    #     stat["max"] = duration;

def print_stats():
    # print("#task\tntasks\ttotal_duration\tmin_duration\tmax_duration\tavg_duration");
    # for key, value in completed_tasks.items():
    #     task=value;
    #     avg=task["total_duration"]/task["ntasks"];
    #     print(task["name"]+"\t"+str(task["ntasks"])+"\t"+str(task["total_duration"])+"\t"+
    #           str(task["min"])+"\t"+str(task["max"])+"\t"+str(avg));
    df['name'] = tasks_name;
    df['id'] = tasks_id;
    df['begin'] = tasks_begin;
    df['end'] = tasks_end;
    df['worker'] = tasks_workers;
    df['worker_id'] = workers_id;
#    dff['node'] = nodes


    df.to_csv('profile.csv')
    df.to_hdf('profile.h5', key='df', mode='w')
        
while 1:
    line_split=get_next_line();
    if line_split==None :
        break
    if (len(line_split)>0):
        if line_split[0]=="20":
            timestamp=line_split[1];
            worker=line_split[2];
            task=line_split[4];
            if(worker == "w0"):
                if(started_gpu_tasks.get(worker)!=None and float(started_gpu_tasks[worker]["start_date"]) > 0):
                    sys.stderr.write("Error at "+timestamp+": worker "+worker+" did not finish its previous job (started at"+started_gpu_tasks[worker]["start_date"]+")\n");
                    
                started_gpu_tasks[worker]={}
                started_gpu_tasks[worker]["start_date"]=timestamp;
                started_gpu_tasks[worker]["task"]=task;

            else:
                if(started_tasks.get(worker)!=None and float(started_tasks[worker]["start_date"]) > 0):
                    sys.stderr.write("Error at "+timestamp+": worker "+worker+" did not finish its previous job (started at"+started_tasks[worker]["start_date"]+")\n");
            
                started_tasks[worker]={}
                started_tasks[worker]["start_date"]=timestamp;
                started_tasks[worker]["task"]=task;
                
                #        print(timestamp+": worker "+worker+" starts task "+task);
        if line_split[0]=="10" and line_split[4] == "\"Po\"" :
            timestamp=line_split[1];
            worker=line_split[2];

            if(started_tasks.get(worker)!=None and float(started_tasks[worker]["start_date"]) < 0):
                sys.stderr.write("Error at "+timestamp+": worker "+worker+" finished a job that never started!\n");

            duration=float(timestamp)-float(started_tasks[worker]["start_date"]);
                #        print(timestamp+": worker "+worker+" ends his task("+started_tasks[worker]["task"]+") that started at "+started_tasks[worker]["start_date"]+" -> duration: "+str(duration));

            started_tasks[worker]["stop_date"]=timestamp;
            update_stats(worker);

            started_tasks[worker]["start_date"]=-1;

        else:
            if line_split[0]=="10" and line_split[4] == "\"I\"" :
                timestamp=line_split[1];
                worker=line_split[2];
                if((worker == "w0") and (len(started_gpu_tasks) > 0)):
                    if(started_gpu_tasks.get(worker)!=None and float(started_gpu_tasks[worker]["start_date"]) < 0):
                        sys.stderr.write("Error at "+timestamp+": worker "+worker+" finished a job that never started!\n");
                        
                    duration=float(timestamp)-float(started_gpu_tasks[worker]["start_date"]);
                #        print(timestamp+": worker "+worker+" ends his task("+started_tasks[worker]["task"]+") that started at "+started_tasks[worker]["start_date"]+" -> duration: "+str(duration));
                
                    started_gpu_tasks[worker]["stop_date"]=timestamp;
                    update_gpu_stats(worker);
                
                    started_gpu_tasks[worker]["start_date"]=-1;

print_stats()

