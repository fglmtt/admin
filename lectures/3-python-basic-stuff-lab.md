# Python: Basic stuff - Lab

## Table of contents

- [1. Get started](#1-get-started)
	- [1.1. Hints](#11-hints)
- [2. Spelling bee](#2-spelling-bee)
	- [2.1. Assignment](#21-assignment)
	- [2.2. Hints](#22-hints)

## 1. Get started

- [ ] [Set up the development environment](1-python-basic-stuff-pt1.md#16-development-environment)
- [ ] Try out the examples provided in the previous lectures
	- [ ] [Python: Basic stuff - Pt. 1](1-python-basic-stuff-pt1.md)
	- [ ] [Python: Basic stuff - Pt. 2](2-python-basic-stuff-pt2.md)

### 1.1. Hints

The following is to run a Python program

```shell
$ python <your_program>.py
```

The following is to enable the interactive mode

```shell
$ python
```

Depending on your system, you may have to use `python` or `python3`

## 2.  Spelling bee

### 2.1. Assignment

The New York Times publishes a daily puzzle called spelling bee. This game challenges readers to spell as many words as possible using only seven letters, where one of the letters is required. The words must have at least four letters.

Suppose the letters are ACDLORT, with R as the required letter. So "color" is an acceptable word, but "told" is not, because it does not use R, and "rat" is not because it has only three letters. Letters can be repeated, so "ratatat" is acceptable.

Write a function called `check_word` that checks whether a given word is acceptable ([this](../code/data/words.txt) file contains the accepted words). Here's an outline of the function that includes [doctests](2-python-basic-stuff-pt2#16-doctests). Fill in the function and then check that all tests pass.

```python
def check_word(word, available, required):
    """
    Check whether a word is acceptable

	word : word to check
	available : string of seven available letters
	required : straing of the single required letter
    
    >>> check_word('color', 'ACDLORT', 'R')
    True
    >>> check_word('ratatat', 'ACDLORT', 'R')
    True
    >>> check_word('rat', 'ACDLORT', 'R')
    False
    >>> check_word('told', 'ACDLORT', 'R')
    False
    >>> check_word('bee', 'ACDLORT', 'R')
    False
    """
    return False
```

### 2.2. Hints

### 2.2.1. Run the 

## 3. Recommender system

todo

### 3.1. Assignment

todo

### 3.2. Hints

todo

## Bibliography

| Author                     | Title                                                                                                      | Year |
| -------------------------- | ---------------------------------------------------------------------------------------------------------- | ---- |
| Downey, A.                 | [Think Python](https://allendowney.github.io/ThinkPython/)                                                 | 2024 |
| Porter, L. and Zingaro, D. | [Learn AI-Assisted Python Programming](https://www.manning.com/books/learn-ai-assisted-python-programming) | 2023 |
