txt = []
# for c in range(ord('A'), ord('z')+1):
#     txt.append(c)

# for c in range(ord('0'),ord('9')):
#     txt.append(c)

# print(len(txt))
for c in range(1,128):
    txt.append(c)


with open('data.txt', 'wb') as data:
    data.write(bytes(txt))
