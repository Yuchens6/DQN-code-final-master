import memcache
import json
import docker
import paramiko
import os
import re

def execute_ssh_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode()

def get_container_ip(ssh, container_name):
    command = "docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + f"{container_name} \n"
    return execute_ssh_command(ssh, command).strip()

def get_memcached_stats(ssh, container_ip):
    command = f"echo \"stats\" | nc -w 1 {container_ip} 11211 "
    stats_output = execute_ssh_command(ssh, command)
    stats_lines = stats_output.split('\n')
    stats = {}
    for line in stats_lines:
        parts = line.split()
        if len(parts) >= 3:
            if parts[1] == "get_hits" or parts[1] == "get_misses" or parts[1] == "bytes" or parts[1] == "bytes_read":
                key = parts[1]
                value = int(parts[2])
                stats[key] = value
    return stats


def get_redis_hit_rate(ssh, container_id_or_name):
    # 进入Redis容器并获取命中率
    command = f'docker exec {container_id_or_name} redis-cli INFO'
    info_output = execute_ssh_command(ssh, command)
    stats_lines = info_output.split('\n')
    stats = {}
    for line in stats_lines:
        parts = line.split(':')
        if len(parts) >= 2:
            if parts[0] == "keyspace_hits" or parts[0] == "keyspace_misses" or parts[0] == "used_memory_human" or parts[0] == "total_commands_processed":
                key = parts[0]
                value = int(''.join(re.findall(r'\d+', parts[1])))
                stats[key] = value
    return stats

def calculate_hit_ratio(stats):
    hits = stats.get('get_hits', 0)
    misses = stats.get('get_misses', 0)
    if hits + misses == 0:
        return 0.0
    else:
        return (hits / (hits + misses)) * 100


def calculate_redis_hit_ratio(stats):
    hits = stats.get('keyspace_hits', 0)
    misses = stats.get('keyspace_misses', 0)
    if hits + misses == 0:
        return 0.0
    else:
        return (hits / (hits + misses)) * 100

def GetMemcacehdState():

    current_dir=os.getcwd()
    json_file_name="myenv/memcached_stats.json"
    json_file_path=os.path.join(current_dir,json_file_name)

    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    # 远程服务器信息
    hostname = '172.19.206.30'
    port = 22
    username = 'zx'
    password = 'zx123'

    # 远程 Docker 容器信息
    container_name = 'socialnetwork-home-memcached-1'

    # SSH 连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    # 获取容器 IP 地址
    container_ip = get_container_ip(ssh, container_name)

    # 获取 Memcached 统计信息
    memcached_stats = get_memcached_stats(ssh, container_ip)


    # 计算命中率
    hit_ratio = calculate_hit_ratio(memcached_stats)
    bytes = memcached_stats.get('bytes')
    bytes_read = memcached_stats.get('bytes_read')

    write_str = "{"
    write_str = (write_str + '"hometimeline-memcached":{' + '"hit_ratio":'+str(hit_ratio) + ',"bytes":' + str(bytes) +
                 ',"read_bytes":' + str(bytes_read) + '},')

    container_name = 'socialnetwork-usertimeline-memcached-1'

    container_ip = get_container_ip(ssh, container_name)

    # 获取 Memcached 统计信息
    memcached_stats = get_memcached_stats(ssh, container_ip)

    # 计算命中率
    hit_ratio = calculate_hit_ratio(memcached_stats)
    bytes = memcached_stats.get('bytes')
    bytes_read = memcached_stats.get('bytes_read')

    write_str = (write_str + '"usertimeline-memcached":{' + '"hit_ratio":'+str(hit_ratio) + ',"bytes":' + str(bytes) +
                 ',"read_bytes":' + str(bytes_read) + '},')

    container_name = 'socialnetwork-memcached-1'

    container_ip = get_container_ip(ssh, container_name)

    # 获取 Memcached 统计信息
    memcached_stats = get_memcached_stats(ssh, container_ip)

    # 计算命中率
    hit_ratio = calculate_hit_ratio(memcached_stats)
    bytes = memcached_stats.get('bytes')
    bytes_read = memcached_stats.get('bytes_read')

    write_str = (write_str + '"post-memcached":{' + '"hit_ratio":' + str(hit_ratio) + ',"bytes":' + str(bytes) +
                 ',"read_bytes":' + str(bytes_read) + '},')

    container_name = 'socialnetwork-redis-1'

    # 获取 Memcached 统计信息
    memcached_stats = get_redis_hit_rate(ssh, container_name)

    # 计算命中率
    hit_ratio = calculate_redis_hit_ratio(memcached_stats)
    bytes = memcached_stats.get('used_memory_human')

    bytes_read = memcached_stats.get('total_commands_processed')

    write_str = (write_str + '"redis":{' + '"hit_ratio":' + str(hit_ratio) + ',"bytes":' + str(bytes) +
                 ',"read_bytes":' + str(bytes_read) + '}}')

    # 将命中率和内存使用量写入到 JSON 文件中
    with open(json_file_path, "w") as f:
        f.write(write_str)
    f.close()

    # 关闭 SSH 连接
    ssh.close()
#
if __name__ == "__main__":
    main()