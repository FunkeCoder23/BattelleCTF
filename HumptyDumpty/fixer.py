STACK_SIZE=40000

stacks=[]

with open("og.png","rb") as pic:
    for i in range(10):
        stacks.append( pic.read(STACK_SIZE) )
        garbage = pic.read(40)
        # print(f"{garbage}")
fixed = []

fixed.append(stacks[6])
fixed.append(stacks[0])
fixed.append(stacks[5])
fixed.append(stacks[2])
fixed.append(stacks[9])
fixed.append(stacks[8])
fixed.append(stacks[1])
fixed.append(stacks[4])
fixed.append(stacks[7])
fixed.append(stacks[3])
for stack in fixed:
    print(stack[0:20])

with open("fixed.png","ab") as out:
    for fix in fixed:
        out.write(fix)