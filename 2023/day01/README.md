### Day 1: Trebuchet?!

Something is wrong with global snow production, and you've been
selected to take a look. The Elves have even given you a map; on it,
they've used stars to mark the top fifty locations that are likely to
be having problems.

You've been doing this long enough to know that to restore snow
operations, you need to check all <em class="star">fifty stars</em> by
December 25th.

Collect stars by solving puzzles.  Two puzzles will be made available
on each day in the Advent calendar; the second puzzle is unlocked when
you complete the first.  Each puzzle grants <em class="star">one
star</em>. Good luck!

You try to ask why they can't just use a [weather
machine](/2015/day/1) ("not powerful enough") and where they're even
sending you ("the sky") and why your map looks mostly blank ("you sure
ask a lot of questions") and hang on did you just say the sky ("of
course, where do you think snow comes from") when you realize that the
Elves are already loading you into a
[trebuchet](https://en.wikipedia.org/wiki/Trebuchet) ("please hold
still, we need to strap you in").

As they're making the final adjustments, they discover that their
calibration document (your puzzle input) has been **amended** by a
very young Elf who was apparently just excited to show off her art
skills. Consequently, the Elves are having trouble reading the values
on the document.

The newly-improved calibration document consists of lines of text;
each line originally contained a specific **calibration value** that
the Elves now need to recover. On each line, the calibration value can
be found by combining the **first digit** and the **last digit** (in
that order) to form a single **two-digit number**.

For example:

    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet

In this example, the calibration values of these four lines are `12`,
`38`, `15`, and `77`. Adding these together produces `**142**`.

Consider your entire calibration document. **What is the sum of all of
the calibration values?**

Your puzzle answer was `54708`.

### Part Two

Your calculation isn't quite right. It looks like some of the digits
are actually **spelled out with letters**: `one`, `two`, `three`,
`four`, `five`, `six`, `seven`, `eight`, and `nine` **also** count as
valid "digits".

Equipped with this new information, you now need to find the real
first and last digit on each line. For example:

    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen

In this example, the calibration values are `29`, `83`, `13`, `24`,
`42`, `14`, and `76`. Adding these together produces `**281**`.

**What is the sum of all of the calibration values?**

Your puzzle answer was `54087`.

Both parts of this puzzle are complete! They provide two gold stars:
**


### Notes

As usually happens early on in Advent of Code, I couldn't resist a
solution in `sed` and `awk`, just for fun.

To run:

    $ ./aoc-2023-d01.sh
    Part 1: The sum of all calibration values is 54708
    Part 2: The sum of all calibration values is 54087

For Part 1, the first sed expression `(s/[a-z]//g)` strips alphabetic
characters.  The second sed expression
`(s/([0-9])[0-9]*([0-9])/\1\2/)` keeps only the first and last digit
(if there's more than two digits).  The third sed expression
`(s/^([0-9])$/\1\1/)` repeats single digits.  Finally, `awk` sums.

For Part 2, The idea is to put the begin and end letters "back" in
case they're part of an overlap.  Any letters that remain will get
stripped by the `sed` `s/[a-z]//g` expression.  (The last three `sed`
expressions are from Part 1).

David Krogsrud points out that getting the first and last digits in
the line can be simplified by using `awk`:

    awk 'BEGIN{FS=""} {print $1 $NF}'

Great idea!
