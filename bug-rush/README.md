## Bug Rush Adam Hiatt

### Overview

To solve the bug rush problem I implemented a breadth first search. For simplicity, I started by parsing the bug rush maps into a two dimensional array.
I iterated through the file and added each character where it needed to be. I then checked if the instance provide was already solved, and if not added all of
the valid next moves into an array. I continued this until I found a solution. I kept a list that was the hash of the current instances map represented as a string.

into a hash of the instance's 1d array represented as a tuple to improve performance.
TThis worked fine, but took a while to solve some of the larger instances, and took too long to finish the unsat problem. To increase performance I implemented a minqueue
using OOTB python libraries, changed the 2d array into a 1d array, and changes the hash into a hash of the instance's 1d array represented as a tuple to improve performance.
These changes brought all of the puzzles to under 5 seconds. The unsat problem did take 5.1 seconds one time but only once.

I then created a solvable instance with a much larger frontier, located in the "redo.bugs" file. It was solvable in 12 moves but took about 28 seconds. To improve this I decided to implement
astar. I used the number of moves the chevron was away from the edge as a heuristic. This increased performance of the smaller instances by about 10-15%, but had about a 40% increase in performance
for the more difficult instance - about 17 seconds runtime instead of 28.

We could further improve this by adding additional heuristics, but I probably will move on to another problem.

### How to run

No build process run the program with your version of python based on the usage below:

```
usage: bugrush [-h] [-astar ASTAR] file

Solves instances of a bug rush puzzle.

positional arguments:
  file          File containing the bug rush puzzle

options:
  -h, --help    show this help message and exit
  -astar ASTAR  Set to true to use astar
```
