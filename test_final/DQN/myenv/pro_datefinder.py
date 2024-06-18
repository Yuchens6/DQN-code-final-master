import numpy as np 
import json
import pandas as pd 
import os
import shutil

serviceName_dict={"test_compose-post-service":0,
                  "test_media-service":0,
                  "test_post-storage-service":0,
                  "test_social-graph-service":0,
                  "test_text-service":0,
                  "test_unique-id-service":0,
                  "test_url-shorten-service":0,
                  "test_user-mention-service":0,
                  "test_user-timeline-service":0,
                  "test_nginx-web-server":0,
                  "test_home-timeline-redis":0,
                  "test_media-frontend":0,
                  "test_post-storage-mongodb":0,
                  "test_social-graph-mongodb":0,
                  "test_social-graph-redis":0,
                  "test_url-shorten-mongodb":0,
                  "test_user-mongodb":0,
                  "test_user-timeline-mongodb":0,
                  "test_user-timeline-redis":0,
             }

serviceName_dict1={"compose-post-service":0,
                  "media-service":0,
                  "post-storage-service":0,
                  "social-graph-service":0,
                  "text-service":0,
                  "unique-id-service":0,
                  "url-shorten-service":0,
                  "user-mention-service":0,
                  "user-timeline-service":0,
                  "nginx-web-server":0,
                  "home-timeline-redis":0,
                  "media-frontend":0,
                  "post-storage-mongodb":0,
                  "social-graph-mongodb":0,
                  "social-graph-redis":0,
                  "url-shorten-mongodb":0,
                  "user-mongodb":0,
                  "user-timeline-mongodb":0,
                  "user-timeline-redis":0,
             }

values=[]

def PrometheusData():
    global values
    current_dir=os.getcwd()
    
    pro_data_name="myenv/data"
    
    file_name="myenv/test_prometheus_data.json"
    
    file_path=os.path.join(current_dir,file_name)
    
    pro_data_path=os.path.join(current_dir,pro_data_name)
    
    if os.path.exists(pro_data_path):
        shutil.rmtree(pro_data_path)
        os.mkdir(pro_data_path)
    else:
        os.mkdir(pro_data_path)
        
    with open(file_path,'r',encoding='utf-8') as pro_json:
        data=json.load(pro_json)
        
        ##获取cpu数据：容器在每个CPU内核上的累积占用时间 (单位：秒)
        for table_num in range(len(data['container_cpu'])):
            if 'container_label_com_docker_stack_namespace' in data['container_cpu'][table_num]['metric']:
                if data['container_cpu'][table_num]['metric']['container_label_com_docker_stack_namespace']=="test":
                    ##container_label_com_docker_stack_namespace为docker stack name
                    for key in serviceName_dict:
                        if key==data['container_cpu'][table_num]['metric']['container_label_com_docker_swarm_service_name']:
                            if float(data['container_cpu'][table_num]['value'][1])>=float(serviceName_dict[key]):
                                serviceName_dict[key]=data['container_cpu'][table_num]['value'][1]
        a=0
        for key in serviceName_dict.keys():
            value = serviceName_dict[key]
            values.append(value)
        for key in serviceName_dict1.keys():
                serviceName_dict1[key]=values[a]
                a+=1
        a=0
        values=[]
        
        cpu_data=json.dumps(serviceName_dict1)
        cpu_data_path=os.path.join(pro_data_path,"cpu.json")
        with open(cpu_data_path,"w") as f:
            f.write(cpu_data)
        f.close()
        for key in serviceName_dict:
            serviceName_dict[key]=0
        
        ##获取mem数据：容器当前的内存使用量（单位：字节）
        for table_num in range(len(data['container_memory'])):
            if 'container_label_com_docker_stack_namespace' in data['container_memory'][table_num]['metric']:
                if data['container_memory'][table_num]['metric']['container_label_com_docker_stack_namespace']=="test":
                    
                    for key in serviceName_dict:
                        if key==data['container_memory'][table_num]['metric']['container_label_com_docker_swarm_service_name']:
                            if float(data['container_memory'][table_num]['value'][1])>=float(serviceName_dict[key]):
                                serviceName_dict[key]=data['container_memory'][table_num]['value'][1]
        
        a=0
        for key in serviceName_dict.keys():
            value = serviceName_dict[key]
            values.append(value)
        for key in serviceName_dict1.keys():
                serviceName_dict1[key]=values[a]
                a+=1
        a=0
        values=[]
        
        for key in serviceName_dict1.keys():
            serviceName_dict1[key]=int(serviceName_dict1[key])/1000000
            ##改单位为MB
        mem_data=json.dumps(serviceName_dict1)
        mem_data_path=os.path.join(pro_data_path,"mem.json")
        with open(mem_data_path,"w") as f:
            f.write(mem_data)
        f.close()
        for key in serviceName_dict:
            serviceName_dict[key]=0
        
        ####获取mem数据：容器的最大内存使用量（单位：字节）
        ##for table_num in range(len(data['container_max_memory'])):
        ##    if 'container_label_com_docker_stack_namespace' in data['container_max_memory'][table_num]['metric']:
        ##        if data['container_max_memory'][table_num]['metric']['container_label_com_docker_stack_namespace']=="test":
        ##            print(data['container_max_memory'][table_num]['value'])
        
        ##获取容器网络累积接收数据总量（单位：字节）
        for table_num in range(len(data['container_network_receive'])):
            if 'container_label_com_docker_stack_namespace' in data['container_network_receive'][table_num]['metric']:
                if data['container_network_receive'][table_num]['metric']['container_label_com_docker_stack_namespace']=="test":
                    
                    for key in serviceName_dict:
                        if key==data['container_network_receive'][table_num]['metric']['container_label_com_docker_swarm_service_name']:
                            if float(data['container_network_receive'][table_num]['value'][1])>=float(serviceName_dict[key]):
                                serviceName_dict[key]=data['container_network_receive'][table_num]['value'][1]
                                
        a=0
        for key in serviceName_dict.keys():
            value = serviceName_dict[key]
            values.append(value)
        for key in serviceName_dict1.keys():
                serviceName_dict1[key]=values[a]
                a+=1
        a=0
        values=[]
        
        net_receive_data=json.dumps(serviceName_dict1)
        net_receive_data_path=os.path.join(pro_data_path,"net_receive.json")
        with open(net_receive_data_path,"w") as f:
            f.write(net_receive_data)
        f.close()
        for key in serviceName_dict:
            serviceName_dict[key]=0
            
        ##获取容器网络累积传输数据总量（单位：字节）
        for table_num in range(len(data['container_network_transmit'])):
            if 'container_label_com_docker_stack_namespace' in data['container_network_transmit'][table_num]['metric']:
                if data['container_network_transmit'][table_num]['metric']['container_label_com_docker_stack_namespace']=="test":
                    
                    for key in serviceName_dict:
                        if key==data['container_network_transmit'][table_num]['metric']['container_label_com_docker_swarm_service_name']:
                            if float(data['container_network_transmit'][table_num]['value'][1])>=float(serviceName_dict[key]):
                                serviceName_dict[key]=data['container_network_transmit'][table_num]['value'][1]
                                
        a=0
        for key in serviceName_dict.keys():
            value = serviceName_dict[key]
            values.append(value)
        for key in serviceName_dict1.keys():
                serviceName_dict1[key]=values[a]
                a+=1
        a=0
        values=[]
        
        net_transmit_data=json.dumps(serviceName_dict1)
        net_transmit_data_path=os.path.join(pro_data_path,"net_transmit.json")
        with open(net_transmit_data_path,"w") as f:
            f.write(net_transmit_data)
        f.close()
        for key in serviceName_dict:
            serviceName_dict[key]=0
        
        for table_num in range(len(data['container_cpu'])):
            if 'container_label_com_docker_stack_namespace' in data['container_cpu'][table_num]['metric']:
                if data['container_cpu'][table_num]['metric']['container_label_com_docker_stack_namespace']=="test":
                    for key in serviceName_dict:
                        if key==data['container_cpu'][table_num]['metric']['container_label_com_docker_swarm_service_name']:
                            serviceName_dict[key]=int(data['container_cpu'][table_num]['metric']["job"].split("_")[1])
        
        a=0
        for key in serviceName_dict.keys():
            value = serviceName_dict[key]
            values.append(value)
        for key in serviceName_dict1.keys():
                serviceName_dict1[key]=values[a]
                a+=1
        a=0
        values=[]
        
        node_data=json.dumps(serviceName_dict1)
        node_data_path=os.path.join(pro_data_path,"node_data.json")
        with open(node_data_path,"w") as f:
            f.write(node_data)
        f.close()
        for key in serviceName_dict:
            serviceName_dict[key]=0
            
    pro_json.close()

PrometheusData()