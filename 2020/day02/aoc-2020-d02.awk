# Advent of Code 2020, Day 2 (https://adventofcode.com/2020/day/2)
# Author: Ben Bornstein

# Part 1
# Q: How many passwords are valid according to their policies?
# A: Policy 1 valid passwords: 439

# Part 2
# Q: How many passwords are valid according to their policies?
# A: Policy 2 valid passwords: 584


# Example Input Line: 3-4 j: hjvj
#                     ^ ^ ^  ^
#                     | | |  |
#                     p q c  $5
#
# FS defines the field separators to use: -, :, and ' ' (space).  The
# awk field $4 is empty because two separators are adjacent.
#
# Variables pc and qc hold the characters in $5 at positions p and q.

BEGIN { FS="\-|:| "; policy1 = 0; policy2 = 0; }
      {
        p = $1; q = $2; c = $3; pc = substr($5, p, 1); qc = substr($5, q, 1);
        if ((pc == c || qc == c) && (pc != qc)) policy2++;

        # Counts occurrences of c in $5 by replacing c with an empty
        # string.  This operation modifies $5, so policy2 is considered
        # first (above).
        count = gsub(c, "", $5);

        if (count >= p && count <= q) policy1++;
      }

END   {
        print "Policy 1 valid passwords: " policy1 ".";
        print "Policy 2 valid passwords: " policy2 ".";
      }
