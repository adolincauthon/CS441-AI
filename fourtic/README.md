## Fourtic - Adam Hiatt

### Overview

This was a pretty straightforward program. I implemented a minimax solver using a 2d array in order to solve instances of the problem. The algorithm and scoring was simple. I did run into an issue where I was getting the opposite value for instances where it was `O`'s turn to play. I realized then that the value in the github repo was the negamax value for the instances. To solve this I just negated the result if it was `O`'s turn rather than reimplement the whole algorithm with negamax.

### How to run

No build process run the program with your version of python based on the usage below:

```
usage: fourtic.py [-h] file

Solves instances of fourtic.

positional arguments:
  file        File containing the bug rush puzzle

options:
  -h, --help  show this help message and exit
```
