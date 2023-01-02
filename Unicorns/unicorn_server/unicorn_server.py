#!/usr/bin/env python

from __future__ import print_function
from unicorn import * # Install unicorn from source https://github.com/unicorn-engine/unicorn
from unicorn.unicorn_const import *
from unicorn.x86_const import *
from unicorn.arm_const import *
from unicorn.mips_const import *
from pwn import * # pip install pwntools
import socketserver
from hashlib import md5
import binascii
import random

MEM_SIZE = 0x001000

unicorn_types = [
    (UC_ARCH_X86, UC_MODE_32, UC_X86_REG_ECX),
    (UC_ARCH_X86, UC_MODE_64, UC_X86_REG_RDX),
    (UC_ARCH_ARM, UC_MODE_ARM, UC_ARM_REG_R2),
    (UC_ARCH_ARM, UC_MODE_THUMB, UC_ARM_REG_R4),
    (UC_ARCH_MIPS, UC_MODE_MIPS32, UC_MIPS_REG_3),
    (UC_ARCH_MIPS, UC_MODE_MIPS64, UC_MIPS_REG_6),
]

class UnicornsHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        try:
            t = remote.fromsocket(self.request)
            t.sendline('What is a group of unicorn called?')
            if (md5.new(t.recvline()).digest() != binascii.unhexlify('fdb2efc47ec9498b576cad5f707e433e')):
                t.sendline('Wrong!')
                t.close()
                return
            t.sendline('How many unicorns do you have?')
            num = int(t.recvline())
            
            shared = '\x00'*MEM_SIZE
            code_addr = random.randint(1,255) * 0x1000
            data_addr = random.randint(1,255) * 0x100000
            
            for x in range(num):
                t.sendline('Running unicorn %d'%x)
                foundunicorn = unicorn_types[x%len(unicorn_types)]
                mu = Uc(foundunicorn[0], foundunicorn[1])
                mu.mem_map(code_addr, MEM_SIZE)
                mu.mem_write(code_addr, t.recvn(MEM_SIZE))
                mu.mem_map(data_addr, MEM_SIZE)
                mu.mem_write(data_addr, shared)
                mu.reg_write(foundunicorn[2], data_addr)
                try:
                    mu.emu_start(code_addr, code_addr+MEM_SIZE, timeout=10, count=4)
                except:
                    t.sendline('Encountered an error running unicorn %d. Exiting.'%x)
                    t.close()
                    return
                shared = str(mu.mem_read(data_addr, MEM_SIZE))
                
            foundunicorn = unicorn_types[num%len(unicorn_types)]
            mu = Uc(foundunicorn[0], foundunicorn[1])
            mu.mem_map(code_addr, MEM_SIZE)
            mu.mem_write(code_addr, shared)
            mu.mem_map(data_addr, MEM_SIZE)
            mu.mem_write(data_addr, flag)
            mu.reg_write(foundunicorn[2], data_addr)
            try:
                if foundunicorn[1] == UC_MODE_THUMB: 
                    mu.emu_start(code_addr | 1, code_addr+MEM_SIZE, timeout=10, count=4)
                else:
                    mu.emu_start(code_addr, code_addr+MEM_SIZE, timeout=10, count=4)
            except:
                t.sendline('Encountered an error running final unicorn. Exiting.')
                t.close()
                return
            shared = str(mu.mem_read(data_addr, MEM_SIZE))
            if (shared.rstrip('\x00')[::-1] == flag):
                t.sendline("flag:{%s}"%flag)
            else:
                t.sendline('The last unicorn did not return the right flag.')
        except:
            print('Unexpected exception caught. Closing this socket.')
        finally:
            t.close()

if __name__ == "__main__":
    flag = open('flag','r').read().rstrip('\n')
    server = socketserver.TCPServer(('0.0.0.0', 4567), UnicornsHandler, bind_and_activate=False)
    server.allow_reuse_address=True
    server.server_bind()
    server.server_activate()
    server.serve_forever()

