import json
from prometheus_api_client import PrometheusConnect

def GetPrometheusData():
    # Prometheus API URL
    prometheus_url = "http://172.19.206.70:9090"
    
    # Prometheus API 用户名和密码
    prometheus_user = "zx"
    prometheus_password = "zx123"
    
    # 创建 Prometheus 连接
    prom = PrometheusConnect(
        url=prometheus_url,
        headers={"Authorization": f"Basic {prometheus_user}:{prometheus_password}"}
    )
    
    # 查询每个 Docker 容器当前的 CPU 利用率
    query_container_cpu = 'container_cpu_usage_seconds_total'
    container_cpu_result = prom.custom_query(query_container_cpu)
    
    # 查询每个 Docker 容器最大内存使用量
    query_container_max_memory = 'container_memory_max_usage_bytes'
    container_max_memory_result = prom.custom_query(query_container_max_memory)
    
    
    # 查询每个 Docker 容器当前的内存使用量
    query_container_memory = 'container_memory_usage_bytes'
    container_memory_result = prom.custom_query(query_container_memory)
    
    # 查询每个 Docker 容器当前的网络流量
    query_container_network_receive = 'container_network_receive_bytes_total'
    container_network_receive_result = prom.custom_query(query_container_network_receive)
    
    query_container_network_transmit = 'container_network_transmit_bytes_total'
    container_network_transmit_result = prom.custom_query(query_container_network_transmit)
    
    #后期加的两个指标
    # 查询 container_cpu_load_average_10s 指标数据
    query_cpu_load = 'container_cpu_load_average_10s'
    cpu_load_result = prom.custom_query(query_cpu_load)
    
    # 查询 container_memory_max_usage_bytes 指标数据
    query_memory_usage = 'container_memory_max_usage_bytes'
    memory_usage_result = prom.custom_query(query_memory_usage)
    
    # 查询每个 Docker 容器当前的磁盘 I/O
    # query_container_disk_reads = 'container_disk_reads_bytes_total'
    # container_disk_reads_result = prom.custom_query(query_container_disk_reads)
    
    # query_container_disk_writes = 'container_disk_writes_bytes_total'
    # container_disk_writes_result = prom.custom_query(query_container_disk_writes)
    
    # 查询 Swarm 每个主机节点的 CPU 利用率
    query_node_cpu = 'node_cpu_seconds_total'
    node_cpu_result = prom.custom_query(query_node_cpu)
    
    # 查询 Swarm 每个主机节点的节点内存使用量
    query_node_memory = 'node_memory_MemTotal_bytes'
    node_memory_result = prom.custom_query(query_node_memory)
    
    # 查询 Swarm 每个主机节点的节点磁盘使用量
    # query_node_disk = 'node_filesystem_size_bytes'
    # node_disk_result = prom.custom_query(query_node_disk)
    
    # 构建结果字典
    result_data = {
        "container_cpu": container_cpu_result,
        "container_memory": container_memory_result,
        "container_max_memory": container_max_memory_result,
        "container_network_receive": container_network_receive_result,
        "container_network_transmit": container_network_transmit_result,
        "container_cpu_load_average_10s": cpu_load_result,
        "container_memory_max_usage_bytes": memory_usage_result,
        # "container_disk_reads": container_disk_reads_result,
        # "container_disk_writes": container_disk_writes_result,
        "node_cpu": node_cpu_result,
        "node_memory": node_memory_result,
        # "node_disk": node_disk_result,
    }
    
    # 将结果保存到 JSON 文件
    with open('prometheus_data.json', 'w') as json_file:
        json.dump(result_data, json_file, indent=2)
    
    print("Data saved to prometheus_data.json")
    