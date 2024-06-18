import paramiko

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
            if parts[1] == "get_hits" or parts[1] == "get_misses":
                key = parts[1]
                value = int(parts[2])
                stats[key] = value
    return stats

def calculate_hit_ratio(stats):
    hits = stats.get('get_hits', 0)
    misses = stats.get('get_misses', 0)
    if hits + misses == 0:
        return 0.0
    else:
        return (hits / (hits + misses)) * 100

def main():
    # 远程服务器信息
    hostname = '192.168.8.130'
    port = 22
    username = 'lin'
    password = '0'

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
    bytes = memcached_stats.get('bytes', 0)
    bytes_read = memcached_stats.get('bytes_read', 0)
    result_data = {"hit_ratio": hit_ratio, "memory_usage": memory_usage}

    # 将命中率和内存使用量写入到 JSON 文件中
    with open('memcached_stats.json', 'w') as json_file:
        json.dump(result_data, json_file, indent=2)
    print(f"Memcached hit ratio: {hit_ratio:.2f}%")

    # 关闭 SSH 连接
    ssh.close()

if __name__ == "__main__":
    main()
