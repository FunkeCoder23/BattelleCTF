[TOC]

# The Legend of the Headless Horseman

> A mysterious figure has been terrorizing the village of Sleepy Hollow. He rides a massive horse, swings a mighty scythe and has been collecting heads from any who draw near. A group of locals, Ichabod Crane, Katrina Van Tassel, and Abraham "Brom Bones" Van Brunt have been working to discover the secret behind this mysterious menace, but just as they were on the verge of putting the pieces together, the Headless Horseman struck! All that are left of the heroes are some unidentifiable bodies with no heads!

> Can you help put our heroes back together, and figure out what secrets they uncovered? You'll first need to bargain with the horseman... bring some pumpkins with you.. a LOT of pumpkins.


## First Thoughts

We follow the usual steps, running `file` on everything in the zip.

```sh
distributed_files/body_bag:          directory
distributed_files/headless_horseman: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c27bbcbb5c6cca6f828ac55c4a67aef8ba293156, for GNU/Linux 3.2.0, not stripped
distributed_files/README.txt:        ASCII text

## body_bag/
distributed_files/body_bag/bloated_body:     data
distributed_files/body_bag/decomposing_body: Apple DiskCopy 4.2 image \226\007, 78317568 bytes, 0x80130000 tag size, GCR CLV ssdd (400k), 0x0 format
distributed_files/body_bag/rotting_body:     data
```

We have a cute little README with the following:

```text
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% The Legend of the Headless Horseman %%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

A mysterious figure has been terrorizing the village of Sleepy Hollow.

He rides a massive horse, swings a mighty scythe and has been collecting heads from any who draw near.

A group of locals, Ichabod Crane, Katrina Van Tassel, and Abraham "Brom Bones" Van Brunt have been working to discover the secret behind this mysterious menace, but just as they were on the verge of putting the pieces together, the Headless Horseman Struck!

All that are left of the heros are some unidentifiable bodies with no heads!

Can you help put our heros back together, and figure out what secrets they uncovered? You'll first need to bargin with the horseman... bring some pumpkins with you.. a LOT of pumpkins.%  
```

We also have a binary, and 3 data (well technically, 1 is an `Apple DiskCopy`... but we'll leave that for later)

## Application

Running `headless_horseman` gives us the following output:

```sh
You see a dark figure looming in the darkness
As you approach he raises his hand to stop you
The figure holds up a bloody sack as if offering the contents to you
He holds out his other hand, as if expecting some kind of offering
you look back in your cart and scan over the pumpkins you brought.. will it be enough?
how many pumpkins did you bring with you this time? 
```

entering a non-zero number ("bring some pumpkins") results in:

```sh
The figure pulls a head off the saddle and holds it over the cart and you hear it mumble as it inspects your offering
the figure turns to you and draws his sword... time to leave! make sure to bring the right number of pumpkins next time!
```

Clearly, we're not going to bruteforce all of the possibilities, so let's take a look at the binary.

## Ghidra

## Main

In our main function, we have `print_intro` which (shockingly) prints the intro text, and an int which gets set by `offer_pumpkins` and is passed into `count_offering`,

## Offer Pumpkins

`offer_pumpkins` appears to simply read in and return our input, and contains a `stack_canary` that we saw previously in HumptyDumpty.

## Main pt2

With this information, we can see that the int is some kind of `pumpkinCount` which is read in and passed to `count_offering` 

## Count Offering

Here's where we get to the meat of the application. We can see that our `pumpkinCount` needs to be higher than 0, and then get's passed into `first_count`

## First Count

Easy, `return pumpkinCount >> 0x10 == 0xdead;`, reversing that operation gives us `0xdead << 0x10 = 3735879680`.

We can pass that as our `pumpkinCount` which outputs the previous text followed by "The figure turns to you and nods, pulling out his bag of heads, dumping them on the ground in front of you".

## Second Count

Even easier, `return pumpkinCount == 0xface;`

Combining these two give us our final 'pumpkinCount' of `0xdeadface = 3735943886` 

## Release the Heads

Entering our new `pumpkinCount` we get the final part of the message

```text
You hear a grunt of approval but the mumbling continues
The figure turns to you and nods, pulling out his bag of heads, dumping them on the ground in front of you
A quick count indicates more heads than you were expecting, he is quite the collector!
well, you seem have gotten what you came for..time to start stitching
As you pick up the first head you begin to wonder which body it might belong to, and how on earth you might go about reviving these poor souls...
maybe you can use the fabled Quick and Efficient Murder Un-Doer(QEMU for short)
```

and another data dump of `heads`
```
dessicated_head: ERROR: error reading
fetid_head:      ELF 64-bit LSB shared object, x86-64, version 1 (SYSV)
moldy_head:      ERROR: error reading
putrid_head:     ELF 64-bit LSB shared object, x86-64, version 1 (SYSV)
shrunken_head:   ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV)
swollen_head:    ELF 64-bit LSB shared object, x86-64, version 1 (SYSV)
```

and a quick attempt at importing into ghidra shows 3 of type `x86:LE:64`, one `ARM:LE:32`, one `MIPS:BE:32`, and one `X86:LE:32`... unfortunately, for some reason, none were imported into ghidra, but we can try and run the files themselves within qemu. Since, dessicated and moldy had errors reading, we can probably assume one is MIPS and the other ARM

* Note from future: Moldy head is BE, and dessicated is LE, giving us 
 * x86-64:LE  : fetid, putrid, swollen
 * ARM-32:LE  : dessicated 
 * MIPS-32:BE : moldy 


## QEMU

I've never messed with qemu before, but it's an emulator for different architectures, given a disk image. Now it's starting to make sense why we have an Apple DiskCopy body, and I'm going to assume that the other bodies are similarly disk images.

After getting qemu installed, each is showing a file format of `raw`. 

```sh
❯ qemu-img info bloated_body
image: bloated_body
file format: raw
virtual size: 598 KiB (612352 bytes)
disk size: 600 KiB
❯ qemu-img info decomposing_body
image: decomposing_body
file format: raw
virtual size: 514 KiB (526336 bytes)
disk size: 516 KiB
❯ qemu-img info rotting_body
image: rotting_body
file format: raw
virtual size: 16 KiB (16384 bytes)
disk size: 16 KiB
```

So that may be a bad lead, let's try the heads

```sh
❯ qemu-img info dessicated_head
image: dessicated_head
file format: raw
virtual size: 512 B (512 bytes)
disk size: 4 KiB
❯ qemu-img info fetid_head
image: fetid_head
file format: raw
virtual size: 512 B (512 bytes)
disk size: 4 KiB
❯ qemu-img info moldy_head
image: moldy_head
file format: raw
virtual size: 512 B (512 bytes)
disk size: 4 KiB
❯ qemu-img info putrid_head
image: putrid_head
file format: raw
virtual size: 512 B (512 bytes)
disk size: 4 KiB
❯ qemu-img info shrunken_head
image: shrunken_head
file format: raw
virtual size: 512 B (512 bytes)
disk size: 4 KiB
❯ qemu-img info swollen_head
image: swollen_head
file format: raw
virtual size: 512 B (512 bytes)
disk size: 4 KiB
```

## Another thought

Heads and bodies go together... that seems natural, each of the heads has ELF magic bits, and the rest of them seem to contain other expected binary data such as `.rodata`

I wrote a simple script to combine all permutations

```sh
#!/usr/bin/env bash
cd distributed_files
mkdir -p people
for f1 in $(ls body_bag)
do
    for f2 in $(ls head_bag)
    do
        file=$f2\_$f1
        echo making $file
        cat head_bag/$f2 > people/$file
        cat body_bag/$f1 >> people/$file
        chmod +x head_bag
    done
done
```

using another simple script:

```sh
for i in *
do
echo $i
./$i
done
```

we can quickly iterate through our new files.

AHA, we have a hit on our first one:

```
dessicated_head_decomposing_body
Katrina blinks awake, seeming a bit shocked ot be waking up again
'Oh! hello there! just before the lights went out I was working with Ichabod and Brom to get rid of that pesky horseman for good!'
'Drat! it looks like I encrypted my portion but I cant seem to remember what I used!'
'can you help me out? I was never very creative with these things, maybe try the street I grew up on? or my Home Town?'
What should Katrina use as the decryption key? 
                |$
```

Our second seems to also have some valid output

```sh
moldy_head_bloated_body
Ichabod Crane gasps as life returns to his body
He begins looking around frantically
qemu: uncaught target signal 11 (Segmentation fault) - core dumped
```

After deciding to take a smarter approach, I also ran `file`:

```text
❯ file *
dessicated_head_bloated_body:     ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, too large section header offset 546785024
dessicated_head_decomposing_body: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, BuildID[sha1]=c96a5a55d131a48d6e034236330d1925e890f360, for GNU/Linux 3.2.0, not stripped
dessicated_head_rotting_body:     ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, missing section headers
fetid_head_bloated_body:          ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), statically linked, too large section header offset 7998395292473925633
fetid_head_decomposing_body:      ERROR: , statically linked error reading (Invalid argument)
fetid_head_rotting_body:          ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), statically linked, missing section headers
moldy_head_bloated_body:          ELF 32-bit MSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), statically linked, BuildID[sha1]=fb3ef826027d1a22e0926cd609bc9453dab03662, for GNU/Linux 3.2.0, not stripped
moldy_head_decomposing_body:      ELF 32-bit MSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), statically linked, missing section headers
moldy_head_rotting_body:          ELF 32-bit MSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), statically linked, missing section headers
putrid_head_bloated_body:         ERROR: , statically linked error reading (Invalid argument)
putrid_head_decomposing_body:     ERROR: , statically linked error reading (Invalid argument)
putrid_head_rotting_body:         ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), statically linked, missing section headers
shrunken_head_bloated_body:       ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), statically linked, too large section header offset 1208006063
shrunken_head_decomposing_body:   ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), statically linked, too large section header offset 3942644575
shrunken_head_rotting_body:       ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=46ee2457ce9871242b7ad74249a3a19091cd0c52, for GNU/Linux 3.2.0, not stripped
swollen_head_bloated_body:        ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), statically linked, too large section header offset 4611713765090526268
swollen_head_decomposing_body:    ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), statically linked, too large section header offset 1270226218358194178
swollen_head_rotting_body:        ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), statically linked, missing section headers
```

with this we can see that our three valid files are:
1. dessicated_head_decomposing_body
2. moldy_head_bloated_body
3. shrunken_head_rotting_body

However, our prior test was not for nought, since it confirmed 2/3 as valid programs

and TADA we can now import them into ghidra

## Dessicated Head Decomposing Body

`Main` -> `Katrina`, easy

## Katrina

`dessicated_head_decomposing_body`

Our first real function is `Katrina`. The first thing i see is the stack_chk_fail, so I mark the stack_canary and get it out of the way. After the strings loaded in, we can easily see that the byte array is the expected encryption_key.

<Spongebob 5 hours later meme.jpg>... after entirely too long reading through the binary I decided to re-read the prompt, and noticed the clue about the Home Town. After some quick OSINT (google), we find Katrina Van Tassel is from Sleepy Hollow. Entering this into the field results in `really_loves_`. Seems like we're done with Katrina

```text
❯ ./dessicated_head_decomposing_body
Katrina blinks awake, seeming a bit shocked ot be waking up again
'Oh! hello there! just before the lights went out I was working with Ichabod and Brom to get rid of that pesky horseman for good!'
'Drat! it looks like I encrypted my portion but I cant seem to remember what I used!'
'can you help me out? I was never very creative with these things, maybe try the street I grew up on? or my Home Town?'
What should Katrina use as the decryption key? Sleepy Hollow
'You really think it's that?'
'Well i'll give that a shot, does this look right?'
really_loves_
```

## Brom

`shrunken_head_rotting_body`

It took a bit of googling to determine i needed to install `gcc-multilib` in order to get the correct linux-32.so

But once that was done, I was able to get the output of

```text
Brom shakes himself off as he stands up
'Well that was certainly an experience' he says, 'thanks for the help!'
You see him shake his head.. 'though i'm not sure you screwed me back perfectly.. something feels a bit off'
'think you have any medicine to help straighten out my thoughts?'
```

entering the incorrect medicine results in:
```text
Brom's eyes glaze over for a second and he writes down this number: 0xdeadbeef
Brom shakes himself off again
'Nope, that didn't seem to do it.. could you try again? REALLY cram it down my throat, I want to be overflowing with medicine!'
```

This one seems to be less mythology based, so I dive into the binary.

in the `brom` function there's an input, and a function that sets a `notValid` flag based on the input.
this flag gets set if the value is not equal to `0x44414544 = DAED`

The text seems to hint at an overflow exploit, but unfortunately, ghidra didn't decompile the function names properly, so we don't see if the input is succeptible. worth a shot though.

We give the expected 20 chars and append DEAD (endian-ness), and huzzah we have the output of

```text
Brom's eyes glaze over for a second and he writes down this number: 0x44414544
'WOW! I think that did the trick, it's all coming back to me now'
'here is my piece to this creepy puzzle, though I have no idea what it means..'
pumpkin_pie}
```

## Ichabod Crane

`moldy_head_bloated_body`

```text
Ichabod Crane gasps as life returns to his body
He begins looking around frantically
qemu: uncaught target signal 11 (Segmentation fault) - core dumped
[1]    122674 segmentation fault (core dumped)  qemu-mips ./IchabodCrane
```

after looking into the binary, we see that the program is looking for an environment variable `ICHABODS_HORSE`. Google seems to suggest his name is `Gunpowder` so we set that and run again.

```text
Ichabod Crane gasps as life returns to his body
He begins looking around frantically
Gunpowder
He appears to not find what he is looking for and collapses back to the ground
```

Well, at least we're not segfaulting - progress!

Of course, a few lines down in the binary is the solution, `GUNPOWDER`

```text
Ichabod Crane gasps as life returns to his body
He begins looking around frantically
GUNPOWDER
'ah, my trusty steed GUNPOWDER is here, all is well' he says, pulling something out of a saddlebag
'Here, I don't have the whole secret, but here is the piece I was able to find'
flag{the_horseman_just_
```

and with that we have our final flag! `flag{the_horseman_just_`

# Solution

`flag{the_horseman_just_really_loves_pumpkin_pie}`
