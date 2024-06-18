
import numpy as np 
import json
import pandas as pd
import openpyxl
from pathlib import Path
import os
import shutil

serviceName_list=['user-timeline-service','home-timeline-service']


def JaegerData():
    write_str='{'
    
    current_dir=os.getcwd()
    excl_file_name="myenv/trace_excl"
    excl_file_path=os.path.join(current_dir,excl_file_name)
    data_file_name="myenv/jaeger_data"
    data_file_path=os.path.join(current_dir,data_file_name)
    home_json_file_name="myenv/home_jaeger_traces.json"
    home_json_file_path=os.path.join(current_dir,home_json_file_name)
    user_json_file_name="myenv/user_jaeger_traces.json"
    user_json_file_path=os.path.join(current_dir,user_json_file_name)

    duration_file_name="myenv/duration.json"
    duration_file_path=os.path.join(current_dir,duration_file_name)
    
    if os.path.exists(excl_file_path):
        shutil.rmtree(excl_file_path)
        os.mkdir(excl_file_path)
    else:
        os.mkdir(excl_file_path)
    if os.path.exists(data_file_path):
        shutil.rmtree(data_file_path)
        os.mkdir(data_file_path)
    else:
        os.mkdir(data_file_path)
    ##os.mkdir(excl_file_path)
    ##os.mkdir(data_file_path)

    if os.path.exists(duration_file_path):
        os.remove(duration_file_path)

    with open (home_json_file_path,'r',encoding='utf-8') as traces_json:
        data=json.load(traces_json)
        readhome = 0
        for trace_num in range(len(data['data'])):


            length=len(data['data'][trace_num]['spans'])
        #
        #     child_ID_data=[None]*length
        #     excl_data=[None]*length
        #     keys=[None]*length
        #     values=[[0]* 5 for i in range(length)]
        #
            for i in range(length):
                if data['data'][trace_num]['spans'][i]['operationName'] == "read_home_timeline_client":
                    readhome += data['data'][trace_num]['spans'][i]['duration']


        #
        #         keys[i]=data['data'][trace_num]['spans'][i]['spanID']
        #         values[i][0]=data['data'][trace_num]['spans'][i]['spanID']
        #         values[i][1]=data['data'][trace_num]['spans'][i]['operationName']
        #         values[i][2]=data['data'][trace_num]['spans'][i]['duration']
        #         values[i][3]=data['data'][trace_num]['spans'][i]['hasChildren']
        #
        #         if data['data'][trace_num]['spans'][i]['hasChildren'] == True:
        #             child_ID_data[i]=data['data'][trace_num]['spans'][i]['childSpanIds']
        #
        #
        #     span_id=keys
        #     span_dict=dict(zip(keys,values))
        #
        #     for  i in range(length):
        #         excl_data[i]=span_dict[span_id[i]]
        #         self_time=span_dict[data['data'][trace_num]['spans'][i]['spanID']][2]
        #         if data['data'][trace_num]['spans'][i]['hasChildren'] == False:
        #             span_dict[data['data'][trace_num]['spans'][i]['spanID']][4]=span_dict[data['data'][trace_num]['spans'][i]['spanID']][2]
        #         else:
        #             for j in range(len(child_ID_data[i])):
        #                 duration2=self_time
        #                 duration1=duration2-span_dict[child_ID_data[i][j]][2]
        #                 self_time=duration1
        #             self_time=abs(self_time)
        #             span_dict[data['data'][trace_num]['spans'][i]['spanID']][4]=self_time
        #
        #     # #print(excl_data)
        #     trace_id=data['data'][trace_num]['traceID']
        #     #
        #     # #pd.DataFrame(excl_data, columns=["span_ID","operationName","duration","hasChildren","self_time"]).to_excel("C:/Users/31778/Desktop/self_time.xlsx",index=False)
        #     # xlsx="self_time.xlsx"
        #     # path=os.path.join(excl_file_path,xlsx)
        #     # in_file=Path(path)
        #     # ##in_file=Path('C:/Users/31778/Desktop/trace_excl/self_time.xlsx')
        #     # insert='_'+trace_id
        #     #
        #     # out_file=in_file.parent/(in_file.stem+insert+in_file.suffix)
        #     # pd.DataFrame(excl_data, columns=["span_ID","operationName","duration","hasChildren","self_time"]).to_excel(out_file,index=False)
        #
        # ##print(span_dict[keys[1]])
        #
        #     for  i in range(length):
        #         for k in range(len(serviceName_list)):
        #             if span_dict[keys[i]][1]==serviceName_list[k]:
        #                 write_str=write_str+'"'+serviceName_list[k]+'"'+':'+str(span_dict[keys[i]][4])+','
        #                 break
        #     write_str=write_str[:-1]+'}'
        #
        #     data_txt="data.json"
        #     path=os.path.join(data_file_name,data_txt)
        #     in_file=Path(path)
        #     ##in_file=Path('C:/Users/31778/Desktop/data/data.txt')
        #     insert='_'+trace_id
        #     out_file=in_file.parent/(in_file.stem+insert+in_file.suffix)
        #     with open(out_file, "w") as f:
        #         f.write(write_str)
        #     write_str='{'
        #     f.close()
        avgReadHome = readhome/10
        write_str = write_str + '"home-timeline-service"' + ':' + str(avgReadHome) + ','

    traces_json.close()

    with open (user_json_file_path,'r',encoding='utf-8') as traces_json:
        data=json.load(traces_json)
        readuser = 0
        for trace_num in range(len(data['data'])):


            length=len(data['data'][trace_num]['spans'])
        #
        #     child_ID_data=[None]*length
        #     excl_data=[None]*length
        #     keys=[None]*length
        #     values=[[0]* 5 for i in range(length)]
        #
            for i in range(length):
                if data['data'][trace_num]['spans'][i]['operationName'] == "read_user_timeline_server":
                    readuser += data['data'][trace_num]['spans'][i]['duration']


        avgReaduser = readuser/10

        write_str = write_str + '"user-timeline-service"' + ':' + str(avgReaduser) + '}'
        with open(duration_file_path,'w') as f:
            f.write(write_str)
        f.close()

    traces_json.close()

JaegerData()