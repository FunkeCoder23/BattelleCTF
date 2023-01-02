[TOC]

# Humpty Dumpty's Fall

> Humpty Dumpty sat on a wall.... you know the rest. Can you figure out how the kings men and horses botched the repair on poor humpty?

## First Thoughts

I first decided to run `file` on everything.

```sh
fall-n-botch:                      ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=a91f0e61479374b48973ceb0f165373e4aaea16d, for GNU/Linux 3.2.0, not stripped
humpty-botched.png:                data
```

Alright, so we have an executable and data.

I run the executable and figure out the usage. So, being me, I run `fall-n-botch humpty-botched.png`... whoops

That overwrote the original picture :/

I re-grabbed the original png just to make sure I didn't mess with anything and call that `og.png` so I don't accidentally overwrite it again.

I decided to open up Ghidra and load in fall-n-botch. So far so good, pretty easy decomp.
Some interesting func names, `fall_and_shatter`, `attempt_fix`, `apply_glue`.

Let's start with `main`


## Main
Not too bad, this just prints the usage we saw earlier, and if run *correctly*, then will call fall and shatter. After initializing the known `int argc, char** argv` we can see that it's passing the filename into `fall_and_shatter`

## Fall and Shatter

Opening the FnS function, we see 10 `void*'s` which get 40kb malloc'd each, and a `FILE*` which reads from the filename passed earlier. The file is then split into those ten 40kb chunks before `attempt_fix` is called.

## Attempt Fix

Briefly looking at `attempt_fix` we see a `FILE*` and 10 `stack*'s`. It did take some googling to figure out why it was named `in_stack_000000#` but it turns out this just refers to things in the call stack outside of the function's frame (in this case, the pointers from FnS).

This function opens up `humpty-botched.png` (where I noticed my mistake with passing it in originally), writes some, calls `apply_glue` on the output, and repeats. 

## Apply Glue

`apply_glue` was a tricky function for me. I could see that it was writing 4 sets of random bytes, but at first I believed it was overwriting data. The other confusing part for me was the `in_FS_OFFSET + 0x28`, however after seeing that it caused a stack_check_fail, and some quick googling, I determined this was just a `stack_canary` in order to prevent stack smashing.

## Stuck

At this point, I was stuck overnight. When I got back to it I had a lot of the pieces in place, but not sure quite where to go from there. I ran `binwalk` on the png, and found there was PNG data contained in it, so I tried with `-e` to extract it but no dice. I ran `hexdump` on the `og.png` and did find the `PNG   IHDR` line while scrolling through. This gave me the idea that this was definitely some kind of misordering, which then made sense of `attempt_fix`'s stack pointers and misordered writes. 

This just left the random bits. I decided to create an empty file to pass in, just to see how the output was changed. This turned out to be extremely helpful, as I could see that my size 0 dummy file was also transformed into a 400400 byte data file, exactly the same size as the original `humpty-botched.png`. I ran `hexdiff` on my new `humpty_botched` and `og` and noticed that the 'random' bits, also happened to be the exact same, in the exact same spot (Seed your randoms, folks). With these two pieces of information, I revisited `apply_glue` and realized it was appending 40 garbage bytes in between the 40kb data bytes. Boom. Now we're ready to reverse it.

I know I'm grabbing 40kb at a time, so I set that as my STACK_SIZE (horrible naming, i'm sure, but it works).

I set up an empty array to store my 10 sets of bytes in, and read in the file, ignoring the 40 garbage bytes that follow each set.

With that ready to manipulate, I look through `attempt_fix` and match up my output stack, with the original

`08=0, 01=1, 18=2, etc.`

After running, the original image is retrieved.

```py
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
```

## Flag

![Flag](HumptyDumpty.png)

`flag{AWL-thuH-KNGz-houRsez}`