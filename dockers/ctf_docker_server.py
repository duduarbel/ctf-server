#!/usr/bin/env python3

import socket
import subprocess
from threading import Thread
from sys import argv
import getopt
import time
import logging

def log(msg):
    print(msg)

threads_are_dead = False

def user_thread_op(user_socket, pipe_to_ctf):
    global threads_are_dead
    try:
        while True:
            data = user_socket.recv(1024)
            if debug_msg:
                log(f'from user: {data}')
            if not data:
                break

            pipe_to_ctf.write(data)
            if add_new_line:
                pipe_to_ctf.write(b'\n')
            pipe_to_ctf.flush()
    except Exception as e:
        logging.exception("message")
    
    log('user_thread is dead')
    threads_are_dead = True

def server_thread_op(user_socket, pipe_from_ctf):
    global threads_are_dead
    line = b''
    try:
        while True:
            # data = pipe_from_ctf.readline()
            # log(f'from ctf server: \'{data}\'')
            # if not data:
            #     break
            # user_socket.sendall(data)
            data = pipe_from_ctf.read(1)
            if debug_msg:
                if data==b'\n':
                    log(f'from ctf server: {line}')
                    line=b''
                else:
                    line += data
            if not data:
                break
            user_socket.send(data)
    except Exception as e:
        logging.exception("message")

    log('server_thread is dead')
    threads_are_dead = True

def create_processes():
    names = exec_name.split(',')

    procs = []
    procs.append( subprocess.Popen( pwd+'/'+names[0], 
                                    cwd=pwd,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT))

    for name in names[1:]:
        procs.append(subprocess.Popen( name, cwd=pwd))

    return procs

def connection_op(conn, addr):
    try:
        procs = create_processes()

        time.sleep(0.2)

        server_thread = Thread(target=server_thread_op,args=(conn, procs[0].stdout))
        server_thread.start()

        time.sleep(0.2)

        user_thread = Thread(target=user_thread_op,args=(conn, procs[0].stdin))
        user_thread.start()

        for _ in range(20*60): # suiside after 20 mins
            try:
                procs[0].wait(timeout=1)
                break
            except subprocess.TimeoutExpired:
                if threads_are_dead:
                    procs[0].stdout.flush()
                    procs[0].kill()
                    procs[0].wait(timeout=0.3)
                    break

        user_thread.join(timeout=0.3)
        server_thread.join(timeout=0.3)
        log(f"Connection to {addr[0]} has been lost")

    except Exception as e: 
        logging.exception("message")

    finally:
        try:
            conn.sendall(b'Stop ctf)(*&')
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            
        except:
            log('can not send stop signal to host')
            pass

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.bind(('', port))
        s.listen()

        conn, addr = s.accept()
    
        connection_op(conn, addr)

    print(f'ctf server for {addr} is down')

def usage():
    print("usage: ctf_docker_server.py executale_name[,another] [-p port] [-n add_new_line(bool)] [-w working_dir] [-h] [-debug]")
    exit(-1)

if __name__ == '__main__':
    if len(argv) < 2:
        usage()

    # defaults:
    port = 22334
    pwd='/usr/src/ctf/'
    add_new_line = False
    debug_msg = False
      
    exec_name = argv[1]

    try:
        opts = getopt.getopt(argv[2:],"p:n:w:d")
    except getopt.GetoptError:
        usage()
   
    for opt, val in opts[0]:
        if opt == '-p':
            port = int(val)
        elif opt in ('-n'):
            add_new_line = (val == 'True' or val == 'true' or val == '1')
        elif opt in ('-w'):
            pwd = val
        elif opt in ('-d'):
            debug_msg = True
    
    start()

