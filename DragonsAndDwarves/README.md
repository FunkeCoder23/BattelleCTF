# Dragons and Dwarves

> A wise dragon decided that dwarves were too easily stealing his treasure while he slept. To thwart these villains he has placed his prized possessions inside a magic portal that transmutes the valuables into worthless junk unless one knew the magic pass phrase. The dragon is so confident of his new scheme that he taunts dwarves daring them to try to steal his treasure.

> The clever dwarves figured out that there were two obstacles the dragon used to prevent access to his treasure. The first one was easily determined because every time the dwarves tried to throw the worthless junk into the magic portal it spit them back out with a flash of a lightning bolt. The dwarves, being masters of ores, gems, and precious things figured out how to fix the junk. Once the magic portal accepted the junk they then realized there was a fundamental flaw in the ancient magic portal the dragon used and leveraged knowledge and wisdom of their great oracle Goggle to crack the pass phrase and recover the treasure.

> We humans want our share of the dragon's loot, but since relations between dwarves and humans is poor, they are unwilling to share any additional information. You must figure out how the dwarves were able to make use of the magic portal and to find the tool they used to access and replace the dragon's valuables with real junk.

> We obtained a copy of the dragon's message to the dwarves and have included it in the provided bundle.

> Prove that you stole the dragon's valuables by swapping them with some junk of your own. When done correctly, the dragon will wake up to inspect his valuables using his magic pass phrase (aka password) and find in its place junk (or a taunting message of your own).

## First Thoughts

In this challenge, we have a text file `Dwarf_Message` containing:

```text
To my next Dwarf victim:

I knew you would be back and my hunch regarding your greed was correct.  As you look around you here all you’ll find is junk. My magic portal is protected by a secret password you’ll never discover and my metallurgical skills are unmatched even by you Dwarves!

You might as well give up now before I catch whiff of you and wake up for a Dwarf-kabob.

Sincerely yours,
Bronze Dragon

```

and a `junk` file, which appears to be a zip archive - password protected.

## Junk

Dumping the hex from `junk` we can see a few file names 

```text
00000000  50 4b 03 04 14 00 0a 00  08 00 53 80 71 53 87 3a  |PK........S.qS.:|
00000010  a7 96 81 00 00 00 82 00  00 00 12 00 1c 00 53 74  |..............St|
00000020  61 73 68 5f 42 72 6f 6e  7a 65 44 72 61 67 6f 6e  |ash_BronzeDragon|
00000030  55 54 09 00 03 ee 6d 95  61 ee 6d 95 61 75 78 0b  |UT....m.a.m.aux.|
00000040  00 01 04 00 00 00 00 04  e6 03 00 00 0f 86 ab 5b  |...............[|
00000050  6a 75 29 86 81 2b e6 1a  0b 76 ba 6d 8a 50 02 d4  |ju)..+...v.m.P..|
00000060  4e 24 9c 7a 7a 16 8a 47  62 eb f3 2c a4 33 ec 5d  |N$.zz..Gb..,.3.]|
00000070  94 da d4 45 28 b4 1b 00  08 de e8 13 ec 5d 39 e7  |...E(........]9.|
00000080  22 29 e4 73 b2 75 1b 10  32 05 24 6a 68 ad 10 58  |").s.u..2.$jh..X|
00000090  37 3f d4 3a 09 42 cb 71  57 25 f0 94 c1 e7 0a b2  |7?.:.B.qW%......|
000000a0  58 dd 53 31 3b 5f 29 25  f4 63 8f 76 33 79 d3 33  |X.S1;_)%.c.v3y.3|
000000b0  e3 57 e8 82 25 a5 83 88  cd 01 b4 16 82 ee e5 1b  |.W..%...........|
000000c0  59 6d 5e c8 06 b5 20 b0  e5 37 42 00 0f 50 4b 07  |Ym^... ..7B..PK.|
000000d0  08 87 3a a7 96 81 00 00  00 82 00 00 00 50 4b 03  |..:..........PK.|
000000e0  04 14 00 0b 00 08 00 45  8b 6f 49 05 cf 00 68 1d  |.......E.oI...h.|
000000f0  01 00 00 9d 01 00 00 0d  00 1c 00 44 77 61 72 66  |...........Dwarf|
00000100  5f 4d 65 73 73 61 67 65  55 54 09 00 03 82 8b 2b  |_MessageUT.....+|
00000110  58 cb 6d 95 61 75 78 0b  00 01 04 00 00 00 00 04  |X.m.aux.........|
00000120  e6 03 00 00 89 5d 5f 2b  02 52 b9 9f f5 02 35 c8  |.....]_+.R....5.|
00000130  43 9c e8 f1 68 c7 b0 f0  10 62 fa ed 25 8b 06 93  |C...h....b..%...|
00000140  88 de 84 4e e8 d3 a2 b0  7f df 6d eb 76 38 de c3  |...N......m.v8..|
00000150  d1 86 4a 35 fb 32 63 fd  f7 3e 0f f4 98 c8 12 88  |..J5.2c..>......|
00000160  8e 9b 55 9e 76 0a 9f ac  92 82 9f 1e 70 ed 16 51  |..U.v.......p..Q|
00000170  e9 53 40 f2 ca 62 ee 3a  6e 0b 51 5a 8a f8 e7 95  |.S@..b.:n.QZ....|
00000180  e8 ad 30 f9 df ed 0b 01  6e 75 48 cf 1a c3 93 d2  |..0.....nuH.....|
00000190  b5 04 22 56 dc 6a 32 57  a3 7e 76 d2 7e 23 77 13  |.."V.j2W.~v.~#w.|
000001a0  f9 44 57 e2 45 14 b3 03  56 b2 e7 00 62 1f b3 89  |.DW.E...V...b...|
000001b0  bf be 24 5f 68 f9 26 37  97 7a cd 78 fe 98 b9 04  |..$_h.&7.z.x....|
000001c0  bb bd 3f f4 17 10 3c 8c  d0 08 14 fb 8b 1e 5e 0e  |..?...<.......^.|
000001d0  37 fb ad b1 2b 13 58 db  a8 2d 34 04 2f aa d9 6e  |7...+.X..-4./..n|
000001e0  ba 1a ba 63 df 16 9b 8d  a4 2a 38 e8 10 1f eb 22  |...c.....*8...."|
000001f0  ec 91 1e 28 b5 ab 67 8b  5b ff a1 22 21 e5 49 81  |...(..g.[.."!.I.|
00000200  b3 64 03 53 77 8d 94 b5  2d a7 d7 fb 20 80 00 6d  |.d.Sw...-... ..m|
00000210  8c 96 56 ee 26 e2 eb 35  d9 8a 57 90 81 0f c6 a5  |..V.&..5..W.....|
00000220  11 13 d1 83 3b 9c 6d f8  98 9a 50 7b c8 4a a5 f7  |....;.m...P{.J..|
00000230  a6 4f 97 83 21 88 4d 64  ac 49 49 a5 4a 8e f7 f9  |.O..!.Md.II.J...|
00000240  1f 50 4b 07 08 05 cf 00  68 1d 01 00 00 9d 01 00  |.PK.....h.......|
00000250  00 50 4b 01 02 1e 03 14  00 0a 00 08 00 53 80 71  |.PK..........S.q|
00000260  53 87 3a a7 96 81 00 00  00 82 00 00 00 12 00 18  |S.:.............|
00000270  00 00 00 00 00 01 00 00  00 f8 81 00 00 00 00 53  |...............S|
00000280  74 61 73 68 5f 42 72 6f  6e 7a 65 44 72 61 67 6f  |tash_BronzeDrago|
00000290  6e 55 54 05 00 03 ee 6d  95 61 75 78 0b 00 01 04  |nUT....m.aux....|
000002a0  00 00 00 00 04 e6 03 00  00 50 4b 01 02 1e 03 14  |.........PK.....|
000002b0  00 0b 00 08 00 45 8b 6f  49 05 cf 00 68 1d 01 00  |.....E.oI...h...|
000002c0  00 9d 01 00 00 0d 00 18  00 00 00 00 00 01 00 00  |................|
000002d0  00 f8 81 dd 00 00 00 44  77 61 72 66 5f 4d 65 73  |.......Dwarf_Mes|
000002e0  73 61 67 65 55 54 05 00  03 82 8b 2b 58 75 78 0b  |sageUT.....+Xux.|
000002f0  00 01 04 00 00 00 00 04  e6 03 00 00 50 4b 05 06  |............PK..|
00000300  00 00 00 00 02 00 02 00  ab 00 00 00 51 02 00 00  |............Q...|
*
00000312
```

We can see it's a zip file `PK`, containing `Dwarf_Message`, and `Stash_BronzeDragon`. Interesting, as we already have a Dwarf_Message file.

## PKCrack

There's a github repo wit a potentially useful program, [PKCrack](https://github.com/keyunluo/pkcrack), it requires an encrypted zip arcive (done) and a zip containing an unencrypted copy of a file in the encrypted zip. If Dwarf_Message *is* in fact the same, this could be useful.

After running the command, we hit on a key triplet... unfortunately, Stash_BronzeDragon has an `invalid compressed data to inflate`

We did incorrectly zip our `Dwarf_Message` the first time though, using `zipinfo` we can see that junk is zipped with `defX` or maximum compression `zip -9`. After rezipping Dwarf_Message, we'll try to crack it again

# Aftermath

I think the challenge is broken... No that's not an excuse, I was able to unzip the new Dwarf_Message completely, but I keep getting a deflate error on the `Stash`. After some googling, I *did* find someone who followed the same steps, got the exact same key triplet, and was successful - in 2017. Using their stash contents:

```text
5000 gold coins
2000kg bronze
10000 silver coins
300 rubies
20 diamonds
Bronze Dragon's secret message: 32FJO!)(G209rdJ(DJ!jF3(!^%
```

They attempted to further decode the secret message, I took the easy route and tried it as a password. 

Ding.

Again, `Stash` fails to decode (Seems like an NMP), but `Dwarf_Message` again decrypts. With that confirmation, I have added my own message to the junk file and encrypted it with the same password.

Challenge Complete*