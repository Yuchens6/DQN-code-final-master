### 一、多节点部署

##### 1、初始化集群

```
docker swarm init --advertise-addr 10.68.31.174
```

添加节点：

```
docker swarm join-token worker
docker swarm join-token manager
使用上面的命令生成的秘钥在节点机子上面运行
```

[swarm的调度](https://bingohuang.gitbooks.io/docker_practice/content/swarm/scheduling.html)

三种调度策略：

- `spread`：如果节点配置相同，选择一个正在运行的容器数量最少的那个节点，即尽量平摊容器到各个节点；
- `binpack`：跟 `spread` 相反，尽可能的把所有的容器放在一台节点上面运行，即尽量少用节点，避免容器碎片化。
- `random`：直接随机分配，不考虑集群中节点的状态，方便进行测试使用。

##### 2、生成容器

```
docker stack deploy --compose-file=docker-compose-swarm.yml Test
```

```
docker stack deploy --compose-file=docker-compose-swarm.yml --placement-pref "engine.labels.zone==east" test
```

```
docker stack deploy --compose-file=docker-compose-swarm.yml --placement-pref "random" test
```

```
docker stack deploy --compose-file=docker-compose-swarm.yml --placement-pref "spread" test
```

##### 3、**加载数据集**

```
python3 scripts/init_social_graph.py --graph=socfb-Reed98
```

```
python3 scripts/init_social_graph.py --graph=<socfb-Reed98, ego-twitter, or soc-twitter-follows-mun>
```

##### 4、测试

首次需要

```
cd ../wrk2
make
所有节点都需要执行make
```

- ①撰写帖子：

  ```
  ../wrk2/wrk -D exp -t 1 -c 1 -d 30 -L -s ./wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 2
  ```

  压测：

  ```
  ../wrk2/wrk -D exp -t 2 -c 4 -d 300 -L -s ./wrk2/scripts/social-network/compose-post.lua http://localhost:8080/wrk2-api/post/compose -R 50
  ```

- ② 阅读主页时间线：

  ```
  ../wrk2/wrk -D exp -t 2 -c 4 -d 30 -L -s ./wrk2/scripts/social-network/read-home-timeline.lua http://localhost:8080/wrk2-api/home-timeline/read -R 50
  ```

- ③ 读取用户时间线：

  ```
  ../wrk2/wrk -D exp -t 4 -c 8 -d 30 -L -s ./wrk2/scripts/social-network/read-user-timeline.lua http://localhost:8080/wrk2-api/user-timeline/read -R 50
  ```

1. `-D exp`: 使用指数分布的连接间隔。这意味着连接将以指数方式增加，而不是固定的时间间隔。
2. `-t 8`: 使用8个线程。
3. `-c 500`: 每个线程使用500个并发连接。
4. `-d 30`: 运行测试的持续时间为30秒。
5. `-L`: 启用请求级别的日志记录。
6. `-s ./wrk2/scripts/social-network/compose-post.lua`: 指定Lua脚本来定义测试场景，其中`./wrk2/scripts/social-network/compose-post.lua`是用于模拟社交网络中发布帖子的场景的脚本。
7. `http://localhost:8080/wrk2-api/post/compose`: 被测试的目标URL是`http://localhost:8080/wrk2-api/post/compose`，即发布帖子的API端点。
8. `-R 5`: 设置每秒钟发出的请求数为5。

### 二、单节点部署

[docker-compose安装]([Docker之compose使用【附实用案例】（不建议收藏）_compose 案例-CSDN博客](https://yyang.blog.csdn.net/article/details/119211496))

后台运行

```
docker-compose up -d
```

停止所有服务

```
docker-compose stop
```

删除所有服务

```
docker-compose down
```

### 三、常使用命令

移除swarm集群节点

```
docker swarm leave --force 
```

容器迁移：

```
docker service update --constraint-add "node.hostname==node_1" my_service
 --constraint-add参数指定了容器运行的节点，node.hostname==node_1表示容器将要运行在节点名称为node_1的节点上，my_service为要迁移的服务
```

查看运行的容器

```
docker ps
docker ps -a  所有容器
```

查看服务

```
docker service ls
```

查看节点

```
docker node ls
```

worker节点升级为manger

```
docker node promote name
```

manger降级为worker

```
docker node demote name
```

### 四、docker swarm 节点的Drain和启用

- 将节点设置为DRAIN并不会从该节点删除独立容器（docker run/ docker up/ docker Engine API创建的容器）。节点的状态只影响service

###### 1、运行`docker node update --availability drain <NODE-ID>`以drain分配有任务的节点：

```
docker node update --availability drain 
```

###### 2、检查节点以检查其可用性：

```
docker node inspect --pretty <name>
```

###### 3、运行`docker node update --availability active <NODE-ID>`以使耗尽的节点返回活动状态：

```
docker node update --availability active
```

### 五、对node操作

###### 1、显示节点标签：

```
docker node ls --filter "label=zone=east"
如果上述不行可以查看JSON格式
docker node inspect <node-id>
```

###### 2、为节点添加标签：

```
docker node update --label-add zone=east <node-id>
```

###### 3、constraint的add/rm

- `--constraint-add`选项用于添加节点约束条件，以限制服务可以部署到哪些节点上。例如，您可以使用`--constraint-add`指定服务只能在具有特定标签的节点上运行：

  ```
  docker service create --name myservice --constraint-add 'node.labels.environment == production' myimage
  ```

  这将使服务`myservice`只能在标签为`environment=production`的节点上运行

- `--constraint-rm`选项用于移除节点约束条件，允许服务在更广泛的节点上运行。例如，您可以使用`--constraint-rm`来移除特定约束条件：

  ```dockerfile
  docker service update --constraint-rm 'node.labels.environment == production' myservice
  ```

  这将允许服务`myservice`在除了标签为`environment=production`的节点之外的节点上运行。

###### 4、在yaml文件中添加约束

```yaml
services:
  my_service:
    image: my_image
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.labels.type == worker
          - node.role == worker
          - node.hostname == myhostname
          - node.resources.cpu.cores >= 2
```

在这个示例中，约束条件包括：

- `node.labels.type == worker`：要求服务只能运行在具有 "type=worker" 标签的节点上。
- `node.role == worker`：要求服务只能运行在 worker 节点上。
- `node.hostname == myhostname`：要求服务只能运行在指定主机名为 "myhostname" 的节点上。
- `node.resources.cpu.cores >= 2`：要求服务运行的节点至少具有 2 个 CPU 核心。

#### 六、查看集群中的网络状态

1. ###### 列出所有Docker网络

   ```
   docker network ls
   ```

2. 查看特定网络的详细信息，：

   ```
   docker network inspect <network_name>
   ```

3. ###### 查看特定节点上的overlay网络状态

   ```
   docker node inspect <node_id>
   ```

4. ###### 查看端口运行情况

   ```
   查看所有端口：
   nmap -p- IP地址
   查看指定端口
   nmap -p port IP
   ```

   
