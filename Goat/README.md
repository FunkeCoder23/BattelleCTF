## Feed the Magical Goat

### Intro
Once upon a time, there was a little reverse engineer who found a special bell. When the bell was struck, they say a magical billy goat appeared looking for food. Everyone knows billy goats will eat anything, but this is all the little reverse engineer had lying around.

| .Inorganic  | .Magical objects        | .Organic    | .Sources of infinite energy  |
| ----------- | ----------------------- | ----------- | ---------------------------- |
| Bottle: `P` | Newt: `n`               | Grass:  `,` | Bunny with a drum: `B`       |
| Broom: `h`  | Old Wise Owl: `W`       | Leaf: `u`   | Capillary bowl: `c`          |
| Can: `@`    | Potion: `p`             | Plant: `;`  | Dipping bird: `r`            |
| Rug: `_`    | Wizard's Staff:  ` \| ` | Seed: `.`   | Perpetual motion device: `H` |

Figure out how to feed and please the billy goat using the 16 items listed here. You only have one of each

## Steps

So the clue hidden in here is `angr`, not quite a mispelling but a hint to a ["platform-agnostic binary analysis framework. "](https://github.com/angr/angr)

### Ghidra

Before learning angr, let's see if we can take a look at the binary to figure out how it works.

In `main` we see that the program is expecting a file called `chow.down`, containing the 16 items mentioned in the intro.

There are four checks:
1. `fill_rumen`
2. `fill_reticulum`
3. `fill_omasum`
4. `fill_abomasum`

#### Fill Rumen

`fill_rumen` is relatively straight forward, we can see four `if` statements for each of the input array, following these we see that the beginning of the input should be `,;.u`

#### Fill Reticulum

`fill_reticulum` is done the same way, giving us the input of `P@h_`


#### Fill Omasum

Again, with `fill_omasum`, giving `|pnw`

#### Fill Abomasum

Our first slight 'hiccup' in `fill_abomasum`, the first input is 'obfuscated' with a bitwise `&`. However, the left hand side of the expression is all `1s` except for the MSB, and the right hand side side is just `H`. Since we haven't used `H` yet, we can clearly see that that's the expected value.

With the rest, we see `HBcr`

#### Give Offering

`give_offering` takes `"chow.down"` hard-coded as an input, and opens the file. If no file is found, it deletes the executable. It then reads 16 bytes/characters from the file, however if you feed Billy an `@` you will get a clue. Let's try, just to see.

##### Hint

```text
You ring the chow bell...
OH NO, here comes Billygoat!!
Have you even seen a goat with bo staff skills? Trick question, no one alive has!
Billygoat eats your offering...

The Ancient Goat Master appears before you and blesses you with a hint.
(unless you're viewing strings, then this is a lie.)

Goats have multiple stomachs.
Magical billygoats are no exception.
The Rumen processes organic matter.
The Reticulum processes inorganic matter.
The Omasum processes magical objects.
The Abomasum processes sources of infinite energy.
At least, that's what we believe.

You should cover your web cam! >.<
```

#### Solution Attempt 1

`,;.uP@h_|pnwHBcr`

```text
You ring the chow bell...
OH NO, here comes Billygoat!!
Have you even seen a goat with bo staff skills? Trick question, no one alive has!
Billygoat eats your offering...
Billygoat looks pleased. He bows to you. Congratulations, you are now the goat master!

flag{l1vn_th4t_goat_l1f3}

```

*Note: It took me a few attempts, make sure your commas are in fact commas, and capitalization is correct

`flag{l1vn_th4t_goat_l1f3}`

### Angr

Let's try that again in Angr, just to learn a new framework

#TODO