[TOC]

# Thanksgiving Bandits
> Last year, the notorious Thanksgiving Bandits struck for the third time. They stole over 1,000 potatoes that were meant to be mashed for the annual Thanksgiving Day feast. Two years ago, they burgled 400 pounds of cranberries, and they took 104 pumpkin pies the year before that. No one knows how they pull off such masterful heists or what they do with their score, but everyone agrees that they must be stopped at all costs.

> Your department has been tasked with intercepting and deciphering their communications to determine when and where they will strike next. You've discovered that they are hiding CANs with secret messages in them inside bags of stuffing, but no one can make any sense of what they say. There are only a few days until the big celebration, and people are becoming worried!

> At this point, it's all up to you to determine what the Thanksgiving Bandits are communicating so the authorities can act. Will you save Thanksgiving, or will you allow the bandits to ruin it for the fourth year in a row? People are counting on you.


## First thoughts

The only file included is the `ImStuffed.bin`. They're not making this easy. The helpful clue hidden in the Intro is that they are hiding `CANs`. I believe they're referring to CAN bus messages, but let's take a look at the googs and see.

After pulling up the CAN spec, I started decoding the binary by hand just to see if it lined up. The first thing I'm noticing is many consecutive `1`'s, while the CAN spec uses bit stuffing (opposite bit for long runs of consecutive bits) in order to keep synchronization

## Binary File Viewer

There's a super handy extension for VSCode that I found, [Binary File Viewer](https://marketplace.visualstudio.com/items?itemName=maziac.binary-file-viewer). With it, you can write your own binary parser and it'll display the parsed values in a nice organized table.... unfortunately the support for big-endian is minimal, at best, and the values I'm getting out of it don't match up with the hand-decoding that I performed. 

Let's try a python decoder.


## Python Decoder

Alright, python decoder is in the works. After messing around with it a bit, I'm much more confident in my CAN assumption, everything seems to be lining up - except the bit stuffing which is yet to be implemented.

The data appears to be from a CAN-LO line, meaning it starts with a `0 Start of Frame` and ends with a series of ten or more `1s` (End of Frame is seven `1`s without bitstuffing, and Inter-Frame Spacing is a three or more `1`s without bitstuffing). This explains the large series of `1`s I was seeing in the binary earlier.

Alright, so after getting bit stuffing implemented, we're starting to see things line up nicely!

I'm printing each message as it gets decoded, with small pause, just to ensure that data looks good.

It looks like the data is repeated twice, once with the ACK high (sending) and one low (receiving), so we'll need to split our data for the final product. 

I'm also seeing some IFS that aren't quite the 3 bits, but because the rest of it's okay, I'm ignoring it.

Another terrible coding practice is just handling the OOB exception and using that as our EOF marker, which then calls `write` to file.

Now for the full speed test (in python, so takes a minute).

Bingo!

We can see in our output file binary (or using the `file` command) that it's a png image, changing the extension and opening it up gives us our nice little CAN of (Bit) Stuffing!