import sys


xored=[]
with open('encrypted.txt','rb') as f:
    while True:
        b = f.read(1)
        if not b:
            break
        c = int.from_bytes(b, sys.byteorder) ^ 42
        xored.append(c)

with open('xor.txt','wb') as f:
    f.write(bytes(xored))
    