### Day 2: Dive!

Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like
`forward 1`, `down 2`, or `up 3`:

  - `forward X` increases the horizontal position by `X` units.

  - `down X` **increases** the depth by `X` units.

  - `up X` **decreases** the depth by `X` units.

Note that since you're on a submarine, `down` and `up` affect your
**depth**, and so they have the opposite result of what you might
expect.

The submarine seems to already have a planned course (your puzzle
input). You should probably figure out where it's going. For example:

    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2

Your horizontal position and depth both start at `0`. The steps above
would then modify them as follows:

  - `forward 5` adds `5` to your horizontal position, a total of `5`.

  - `down 5` adds `5` to your depth, resulting in a value of `5`.

  - `forward 8` adds `8` to your horizontal position, a total of `13`.

  - `up 3` decreases your depth by `3`, resulting in a value of `2`.

  - `down 8` adds `8` to your depth, resulting in a value of `10`.

  - `forward 2` adds `2` to your horizontal position, a total of `15`.

After following these instructions, you would have a horizontal
position of `15` and a depth of `10`. (Multiplying these together
produces `**150**`.)

Calculate the horizontal position and depth you would have after
following the planned course. **What do you get if you multiply your
final horizontal position by your final depth?**

Your puzzle answer was `1692075`.

### Part Two

Based on your calculations, the planned course doesn't seem to make
any sense. You find the submarine manual and discover that the process
is actually slightly more complicated.

In addition to horizontal position and depth, you'll also need to
track a third value, **aim**, which also starts at `0`. The commands
also mean something entirely different than you first thought:

  - `down X` **increases** your aim by `X` units.

  - `up X` **decreases** your aim by `X` units.

  - `forward X` does two things:<ul>   <li>It increases your horizontal
    position by `X` units.

  - It increases your depth by your aim **multiplied by** `X`.

Again note that since you're on a submarine, `down` and `up` do the
opposite of what you might expect: "down" means aiming in the positive
direction.

Now, the above example does something different:

  - `forward 5` adds `5` to your horizontal position, a total of `5`.
    Because your aim is `0`, your depth does not change.

  - `down 5` adds `5` to your aim, resulting in a value of `5`.

  - `forward 8` adds `8` to your horizontal position, a total of `13`.
    Because your aim is `5`, your depth increases by `8*5=40`.

  - `up 3` decreases your aim by `3`, resulting in a value of `2`.

  - `down 8` adds `8` to your aim, resulting in a value of `10`.

  - `forward 2` adds `2` to your horizontal position, a total of `15`.
    Because your aim is `10`, your depth increases by `2*10=20` to a total
    of `60`.

After following these new instructions, you would have a horizontal
position of `15` and a depth of `60`. (Multiplying these produces
`**900**`.)

Using this new interpretation of the commands, calculate the
horizontal position and depth you would have after following the
planned course. **What do you get if you multiply your final
horizontal position by your final depth?**

Your puzzle answer was `1749524700`.

Both parts of this puzzle are complete! They provide two gold stars:
**

### Notes

#### Python

To run:

    $ ./aoc-2021-d02.py
    Part 1: 1925 pos *    879 depth =    1692075
    Part 2: 1925 pos * 908844 depth = 1749524700

#### Forth

The input to this problem is particularly amenable to Forth and as
luck would have it, I've been learning the language!  Although Forth is
postfix, the ability to consume tokens from the input stream makes it
easy to change to prefix or infix notation.  That is, it would be
more Forth-like if the input were formatted as:

    5 forward
    5 down
    8 forward
    3 up
    8 down
    2 forward

Instead of:

    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2

But, again, it's not a problem.  Even in my limited experience, I've
observed Forth is sometimes prefix (see for example `VARIABLE Foo`, but
perhaps that's out of necessity since for `Foo VARIABLE`, the
interpreter / compiler would not recognize the word `Foo`.)

Essentially, the Forth solution defines a Domain Specific Language (DSL)
that exactly matches the problem input.  No command parsing or
conditionals are required!  (Quickly and easily creating custom DSLs is
one of the selling points of Forth.)

To run:

    $ ./aoc-2021-d02.fs
    Part 1: 1925 pos * 879 depth = 1692075
    redefined forward  redefined down  redefined up
    Part 2: 1925 pos * 908844 depth = 1749524700
