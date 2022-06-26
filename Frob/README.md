[TOC]

# What the Frob

> What the.. Frob?

## First Thoughts

Included in `whatthefrob.zip`, we have `wtfrob` and `encrypted.txt`

`encrypted.txt` contains non-printable binary, which (after some experimentation) get's overwritten with our `wtfrob` program.

## Ghidra

Opening up our binary in Ghidra, we can see that the program reads from `data.txt` and writes to `encrypted.txt`.

Making a blank `data.txt` and running `wtfrob` results in

```text
My custom strfry implementation, because I didn't trust the randomess of the original..
wanna read a funny comment thread? https://sourceware.org/bugzilla/show_bug.cgi?id=4403
Did you know Memfrob is a standard function?
```

The link leads to a discussion about the pseudo-randomness of the `strfry` function, which doesn't have equal distribution - some permuations are more likely.

The second hint is that Memfrob a standard function, in the [linux manual](https://man7.org/linux/man-pages/man3/memfrob.3.html) we can see the description.

```text
DESCRIPTION

       The memfrob() function encrypts the first n bytes of the memory
       area s by exclusive-ORing each character with the number 42.  The
       effect can be reversed by using memfrob() on the encrypted memory
       area.

       Note that this function is not a proper encryption routine as the
       XOR constant is fixed, and is suitable only for hiding strings.
```

## Main

In the `main` function, we can see that the random seed is fixed, which should help with decryption quite a bit. 

The `for` loop 'appears' to be doing nothing... none of that data looks to be used afterwards, but we can test this later.

## strfry

Based on the link provided, we can see a general outline for the standard strfry function, and use that to reverse the author's custom version.

In fact, the version in the code matches exactly with Gunderson's patch proposal, which was rebuffed with the following comment:

```text
Your version is still not right, as now some strings could not appear anymore.

For example for the string "abc" the strings "abc" and "acb" could never 
appear.

The version already attached to this bug report returns all cases with a 
correct distribution.
```

## Frobbing some data

As we've seen, the rand function is seeded with a constant, so we can get the exact same permutation out of every run, and frobbing consists of a reversible `^ 42`. We should be able to reverse the permutation by passing in a series of bytes `0x00 -> 0xff`, running it through the program, and then `xor`ing again and seeing which position each is in.

The only caveat being our final output is 520 bytes long, and this only consistently finds 256 positions.

A small py script should help us with both.

... small hiccup, the encrypted data appears to be the same as the original.

Note:

... I am dumb...

The reason that my original and encrypted data appeared the same is *drumroll please* C-strings are null terminated... guess what my first byte was.

I'm now able to determine a 50% chance of where each byte position is, 

unfrobbing the included `encrypted.txt` gives a hexdump of

```brainfuck
00000000  2d 2d 2d 2b 2d 2b 2b 2e  2b 2b 2b 2b 2b 2b 2d 2d  |---+-++.++++++--|
00000010  2b 2b 2b 2b 2d 2d 2b 2b  2d 2b 2d 2d 2b 2d 2b 2b  |++++--++-+--+-++|
00000020  3c 2b 2d 2d 2b 2b 2b 2b  2b 2b 2b 2b 2b 2e 2b 2d  |<+--+++++++++.+-|
00000030  2b 2b 2d 2b 2d 2e 2b 2b  2b 2b 2b 2d 2b 2b 2b 2b  |++-+-.+++++-++++|
00000040  2b 2d 2b 2b 2b 2b 2b 2d  2d 2b 2e 2d 2b 2b 2d 2d  |+-+++++--+.-++--|
00000050  2b 2d 2b 2b 2b 2b 2d 2e  2d 2b 2b 2e 2b 2b 2b 2b  |+-++++-.-++.++++|
00000060  2b 2b 2e 2b 2b 2d 2b 2b  2b 2b 2b 2b 2b 2e 2b 2b  |++.++-+++++++.++|
00000070  2b 2d 2b 2b 2b 2e 2b 2d  3c 2b 2e 2b 2b 2b 2b 2b  |+-+++.+-<+.+++++|
00000080  2d 2b 2b 2b 2b 2d 2b 2b  2b 2e 2d 2b 2b 2b 2d 2d  |-++++-+++.-+++--|
00000090  2d 2b 2b 2d 2b 2b 2e 2b  2b 2b 2b 2b 2b 2b 2b 2d  |-++-++.++++++++-|
000000a0  2b 2b 2b 2e 2d 2d 2b 2e  2b 2d 2b 2b 2d 2b 2e 2b  |+++.--+.+-++-+.+|
000000b0  2d 2d 2b 2b 2e 2b 2d 2b  2b 2d 2b 2b 2b 2e 2b 2b  |--++.+-++-+++.++|
000000c0  2d 2d 2b 2b 2b 2b 2b 2b  2b 2d 2b 3e 2d 2d 2e 2b  |--+++++++-+>--.+|
000000d0  2b 2b 2b 2b 2d 2d 2b 2d  2d 2e 2d 2b 3e 2d 2b 2d  |++++--+--.-+>-+-|
000000e0  2b 2b 2d 2b 2b 2b 2b 2b  2b 2b 2d 2d 2b 2b 2b 2d  |++-+++++++--+++-|
000000f0  2b 2b 2d 2b 2b 2b 2b 2e  2b 2b 2b 3c 2d 2d 2b 3e  |++-++++.+++<--+>|
00000100  2d 2b 2b 2d 2b 2b 2d 2b  2d 2b 2b 2d 2b 2b 2b 2b  |-++-++-+-++-++++|
00000110  2b 2b 2b 2d 2e 2b 2b 3e  2b 2b 2d 2b 2b 2d 2b 2b  |+++-.++>++-++-++|
00000120  2b 2d 2b 2b 2b 2b 2d 2b  2b 2b 2d 2b 2b 2d 2b 3e  |+-++++-+++-++-+>|
00000130  2b 2d 2d 2b 2b 2b 2d 2b  2b 2b 2b 2d 2d 2b 2b 2b  |+--+++-++++--+++|
00000140  2b 2b 2b 2d 2b 2d 2b 2b  2d 2b 2d 2d 2d 2d 2e 2b  |+++-+-++-+----.+|
00000150  2d 2b 2d 2b 3c 2b 2e 2b  2d 2b 2b 2b 2d 2e 2b 2b  |-+-+<+.+-+++-.++|
00000160  2b 2b 2d 2b 2b 2b 2b 2b  2b 2b 2b 2b 2b 2b 2b 2b  |++-+++++++++++++|
00000170  2d 2d 2d 2b 2b 2d 2b 2b  2b 2b 2b 2b 2d 2b 2d 2b  |---++-++++++-+-+|
00000180  2e 2b 2b 2b 2e 2b 2d 2b  2b 2e 2b 2b 2b 2d 2d 2b  |.+++.+-++.+++--+|
000001a0  2d 2b 2d 2b 2d 2d 2e 2b  2b 2b 2b 2b 2b 2b 2b 2d  |-+-+--.++++++++-|
000001b0  2b 2d 2d 2b 2d 2b 2b 2b  2b 2b 2b 3c 2d 2b 2b 2b  |+--+-++++++<-+++|
000001c0  2b 2e 2b 2d 2d 2b 2b 2e  2e 3e 2b 2b 2b 2b 2b 2b  |+.+--++..>++++++|
000001d0  2b 2d 2b 2b 2b 2b 2b 2b  2b 2b 2e 2b 2b 2e 2b 2b  |+-++++++++.++.++|
000001e0  2b 2b 2d 2b 3c 2b 2b 2d  2b 2b 2b 2b 2d 2b 2b 2d  |++-+<++-++++-++-|
000001f0  2d 2b 2b 2d 2b 2d 2d 2d  2b 2b 2b 2d 2b 2b 2d 2b  |-++-+---+++-++-+|
00000200  2b 2b 2d 2b 2b 2b 2d 2b  2b                       |++-+++-++|
```

I'm... not sure what to do with that. *At best* it looks like a brainf*ck program.

I might revisit this challenge later.