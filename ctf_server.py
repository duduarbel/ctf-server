#!/usr/bin/env python3

from multiprocessing import Process
import socket
from threading import Thread
import time
import docker
import logging

number_of_conns = 0

def log_exception():
    class bcolors:
        RED = '\033[91m{'
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
   
    print(bcolors.RED)
    logging.exception("message")
    print(bcolors.ENDC)

def user_thread_op(socket_to_client, socket_to_docker, kill_youself, server_ready):
    try:
        while True:
            if server_ready[0]=='yes':
                data = socket_to_client.recv(1024)
                #print(f'received from client {data}')
                if not data or kill_youself[0]=='yes':
                    break
                socket_to_docker.sendall(data)
            else:
                time.sleep(0.01)
    except Exception as e: 
        log_exception()
    
def _get_ip():
    res = 'IP'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        res =  s.getsockname()[0]
        s.close()
    except:
        print('failed to receive ip')
        log_exception()

    return res

def get_docker_ip(id):
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    container_ip = client.inspect_container(id)['NetworkSettings']['Networks']['bridge']['IPAddress']
    return container_ip

def run_in_docker(socket_to_client, addr, docker_image_name):
    try:
        global number_of_conns
        docker_name = f'{docker_image_name}_{addr[0]}_{number_of_conns}'
        with socket_to_client:
            print(f"Connected by {addr[0]}")

            client = docker.from_env()

            container = client.containers.run(  image=docker_image_name, 
                                                detach=True,
                                                name=docker_name,
                                                #network_disabled=True,
                                                #network_mode='host',
                                                remove=True,
                                                tty=True
                                                )
            container_ip = get_docker_ip(container.id)
            print(f'create container {docker_name} (ip={container_ip})')

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_to_docker:
                kill_youself = ['no']
                server_ready = ['no']
                user_thread = Thread(target=user_thread_op, args=(socket_to_client, socket_to_docker, kill_youself, server_ready))
                user_thread.start()
        
                for i in range(500):
                    try:
                        socket_to_docker.connect((container_ip, 22334))
                        break
                    except ConnectionRefusedError:
                        time.sleep(0.01)
                        if i==400:
                            print(f'connection to {docker_name} (ip={container_ip}) CAN NOT be established')
                            return

                print(f'connection to {docker_name} (ip={container_ip}) has been established')
                
                server_ready[0] = 'yes'
                while True:
                    data = socket_to_docker.recv(1024)
                    #print(f'data from docker: {data}')
                    if not data or data==b'Stop ctf)(*&':
                        break
                    socket_to_client.sendall(data)
            
                socket_to_client.shutdown(socket.SHUT_RDWR)

            kill_youself[0] = 'yes'

    except KeyboardInterrupt:
        pass
    except Exception as e: 
        log_exception()
    finally:
        print(f'Kill container {docker_name}')
        container.kill()
        print(f'container {docker_name} - dead!')

    print(f"Connection to {addr[0]} has been lost")
    
def start(port, docker_image_name):
    global number_of_conns
    processes = []

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', int(port)))
            s.listen()
            while True:
                conn, addr = s.accept()
            
                number_of_conns += 1     
                proc = Process(target=run_in_docker, args=(conn, addr, docker_image_name,))
                proc.start()
                processes.append(proc)
    except KeyboardInterrupt:
        pass
    # for proc in processes:
    #     proc.join()


def get_condif():
    cfg_data = []
    with open('ctf_server.cfg', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.rstrip()
            if line=='' or line[0] == '#':
                continue
            cfg = " ".join(line.split()).split(' ')
            if len(cfg) != 2:
                print("in cfg file - each line should be: docker_name {space} ip ")
                return None
            cfg_data.append(cfg)
    return cfg_data

if __name__ == '__main__':
    
    #start(1237,'ctf_connection_failed')

    cfg_data = get_condif()
    procs = []

    try:
        if cfg_data is not None:
            for cfg in cfg_data:

                print(f'for {cfg[0]}: nc {_get_ip()} {cfg[1]}')
                proc = Process(target=start, args=(int(cfg[1]), cfg[0]))
                proc.start()
                procs.append(proc)

            for t in procs:
                t.join()

    except KeyboardInterrupt:
        pass

    # if len(argv) < 2:
    #     print('USAGE: cft_server.py port docker_name', file=stderr)
    #     exit(1)
    # start(argv[1], argv[2])
