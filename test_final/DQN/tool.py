#g工具类
import json
import get_and_pro_data_

container_states = {}#改用字典
cache_states = {}
# container_merge = {}#记录是否合并的数据结构
def load_data_function():
        get_and_pro_data_.get_pro_data()
        #进行初始数据读取
        # 读取 JSON 文件
        with open('myenv/duration.json') as f:
            data = json.load(f)

        with open('myenv/memcached_stats.json') as f:
            cache_data = json.load(f)

        # 遍历 jaeger JSON 数据并创建 ContainerState 对象
        for key, value in data.items():
            container_name = key.strip()
            communication_delay = int(value)
            print(communication_delay)
            container_state = ContainerState(container_name,communication_delay)
            #container_states.append(container_state)
            container_states[key] = container_state

        for i in range(len(cache_data)):
            cache_name = ""
            if i == 0:
                cache_name = "hometimeline-memcached"
            if i == 1:
                cache_name = "usertimeline-memcached"
            if i == 2:
                cache_name = "post-memcached"
            if i == 3:
                cache_name = "redis"
            hit_rate = int(cache_data[cache_name]["hit_ratio"])
            memory_size = int(cache_data[cache_name]["bytes"])
            byte_read = int(cache_data[cache_name]["read_bytes"])
            cache_state = CacheState(cache_name,hit_rate,memory_size,byte_read)

            cache_states[cache_name] = cache_state



#创建一个自定义的类，
#类里面存储两个微服务，以及微服务间对应的通信量
#
class ContainerState:
    def __init__(self, container1_name, communication_delay):
        self.container1_name = container1_name
        self.communication_delay = communication_delay



class CacheState:
    def __init__(self, cacheName,hit_rate, memory_used, byte_read):
        self.cacheName = cacheName
        self.hit_rate = hit_rate
        self.memory_used = memory_used
        self.byte_read = byte_read


class Container:
    def __init__(self, container_name, node):
        self.container_name = container_name  
        self.container_cpu_usage = 0
        self.container_memory_usage = 0
        self.container_net_receive = 0
        self.container_net_transmit = 0
        self.node = node
    
    def set_node(self, node):
        self.node = node

    def set_container_cpu_usage(self, cpu_usage):
        self.container_cpu_usage = cpu_usage

    def set_container_memory_usage(self, memory_usage):
        self.container_memory_usage = memory_usage

    def set_container_net_receive(self, net_receive):
        self.container_net_receive = net_receive

    def set_container_net_transmit(self, net_transmit):
        self.container_net_transmit = net_transmit
    
    def get_container_cpu_usage(self):
        return self.container_cpu_usage

    
if __name__ == "__main__":
    load_data_function()