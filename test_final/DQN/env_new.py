# import gym
# from gym import spaces
import torch
import torch.nn as nn
import torch.optim as optim
import json
import tool
from tool import container_states
from tool import cache_states
# from tool import container_merge
import socket
import paramiko
import os
import re
import time

class CustomEnv():
    def __init__(self):
        super(CustomEnv, self).__init__()
        # 初始化环境参数和状态空间、动作空间等
        #self.observation_space = spaces.Discrete(...)####################
        
        #self.action_space = spaces.Discrete(2)
        # 其他环境参数的初始化

        ## 定义离散动作空间，取值范围为 1-9 表示所占总内存百分比
        #self.action_space = list(range(2))
        self.action_space = [1,2,3,4,5,6,7,8,9]
        # 定义状态空间为一个包含多个 ContainerState 对象的列表
        #self.state_space = [ContainerState(*container_state) for container_state in container_states]
        # 定义状态空间为【CPU.MEM,等】
        # con = tool.ContainerState("name_1","name_2",20.3)
        # [con.container1_cpu_usage,con.container2_cpu_usage,con.container1_memory_usage,con.container2_memory_usage,con.communication_delay]
        self.state_space = []

        #结果列表
        self.result_dict = {}
        self.reward = 0
    
    #发送消息
    def send_message(self):
        host = '172.19.206.70'
        port = 22
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        try:
            # 连接到目标主机
            sock.connect((host, port))
            print("连接成功")

            # 将字典序列化为 JSON 字符串
            message = json.dumps(self.result_dict)

            # 发送消息
            sock.sendall(message.encode())

        except ConnectionRefusedError:
            print("连接失败，请检查目标主机的 IP 地址和端口号是否正确。")

        finally:
            # 关闭连接
            sock.close()


    
    def reset(self):
        # 重置环境状态并返回初始观测
        # 设置环境的初始状态
        tool.load_data_function()
        # print(self.state_space)
      
        # 返回初始观测

        # 调用数据爬取文件和数据处理文件
        # 获得当前数据信息，初始化状态表##数据里得告诉我当前这两个机器是否合并了呀

    
    #返回初始状态
    def get_initial_state(self):
        self.reset()
        self.state_space = []
        for cache_name, cache_state in cache_states.items():
            # 添加容器对象的值到状态空间
            state = [
                cache_state.hit_rate,
                cache_state.memory_used,
                cache_state.byte_read
            ]
            self.state_space.append(state)
           # 将状态空间转换为张量
        # print(self.state_space)
        # initial_state = torch.tensor(self.state_space, dtype=torch.float32)
        # 提取数字并转换为浮点数
        self.state_space = [[float(num) if isinstance(num, str) and num.replace(".", "", 1).isdigit() else num for num in sublist] for sublist in self.state_space]
        l = len(self.state_space)
        initial_state = torch.tensor(self.state_space, dtype=torch.float32)

        return initial_state#返回的是容器对列表
    
    #execute_action需要dqn循环调用，给出每一对容器的action
    #
    def execute_action(self,action):
        #action01列表
        # 处理
        self.reward = 0
        if torch.is_tensor(action):
            action = action.detach().numpy()
        action = action.flatten()
        #
        for cache_name, cache_state in cache_states.items():
        #     #获取并删除action的第一个值
            self.result_dict[cache_name] = action.ptp(0)#针对某一个容器对的action结果调用的返回结果
        #
        # # self.state_space.remove(state)
        # # 都调用完成,将结果返回给机器
        # # if container_name in container_states and container_states[container_name] == list(container_states.values())[-1]:
        # #     done = False#已经遍历到字典最后一个值
        # # else:
        # #     done = True
        # # return done
        #     #发送消息
        #     # self.send_message()
        #     # time.sleep(5 * 60)
        #     print(cache_name)
        #     print(self.result_dict[cache_name])

            print("hometimeline",action[0],"usertimeline",action[1],"post",action[2],"redis",action[3])
            print("等待重新配置环境,Press Enter to continue...")
            input()
            w = Getwrk()
            print("Continuing...")
                #tool.load_data_function()
                #统计新排版后的reward值
            next_state = self.get_initial_state()
            stats = 0
            for cache_name, cache_state in cache_states.items():
                stats += cache_state.hit_rate
            print(stats)
            #根据请求条数情况调整x和b的值
            x=100000
            b = 0.7
            self.reward = (b*w + (1-b) * stats*x)

            done = True
            return next_state, self.reward, done
        
    
    def render(self):
        # 可选：显示环境的当前状态
        #没有可视化功能
        pass

# 创建自定义环境实例
#env = CustomEnv()


def execute_ssh_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode()

    return result




def userwrk2(ssh, command,limit):
    # 进入Redis容器并获取命中率

    info_output = execute_ssh_command(ssh, command)
    stats_lines = info_output.split('\n')

    result = 1
    num = 0
    for line in stats_lines:
        parts = line.split()
        if len(parts) == 4 and parts[0] != 'Test' and parts[0] != 'Value':
            value = float(parts[0])
            if value>limit:
                result = float(parts[1])
                break
    for line in stats_lines:
        parts = line.split()
        if len(parts) == 6 and parts[0] != 'Latency' and parts[0] != '#[Mean' and parts[0] != '#[Max'and parts[0] != '#[Buckets':
            num = int(parts[0])
    return result,num





def Getwrk():


    # 远程服务器信息
    hostname = '172.19.206.30'
    port = 22
    username = 'zx'
    password = 'zx123'



    # SSH 连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    # route = 'cd newbishe'
    # command = 'ls'
    #要执行的指令
    command = (f'./newbishe/bishe/wrk2/wrk -D exp -t 8 -c 800 -d 20 -L -s '
               f'./newbishe/bishe/socialNetwork/wrk2/scripts/social-network/read-home-timeline.lua '
               f'http://localhost:8080/wrk2-api/home-timeline/read -R 5')
    #时间分割线，超过这个时间的请求会被记录，单位是ms
    limit = 15000
    result,num = userwrk2(ssh,command,limit)
    #超过时请求数
    w = (1-result)*num


    # 关闭 SSH 连接
    ssh.close()
    return w

# if __name__ == '__main__':
#     result,num = Getwrk()
#     print("result",result)
#     print("num",num)



        