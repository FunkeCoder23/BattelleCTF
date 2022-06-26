
import sys
if 0 > len(sys.argv) > 1:
        sys.exit(0)
f = open(sys.argv[1], 'rb')
s = f.read()
s = list(s)
xok = 0x2a
l = len(s)
kek = []
for x in range(0,l):
        kek.append(hex(s[x]))
for x in range(0,l):
        kek[x] = hex(int(kek[x], 16) ^ int(hex(xok), 16))


def convert_hex_to_ascii(h):
    chars_in_reverse = []
    while h != 0x0:
        chars_in_reverse.append(chr(h & 0xFF))
        h = h >> 8

    chars_in_reverse.reverse()
    return ''.join(chars_in_reverse)
gee = ""
for x in range(0,l):
        gee = gee + convert_hex_to_ascii(int(kek[x], 16))

print( gee)