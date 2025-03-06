def uses_all(word, required):
    """
    Check whether a word uses all the required letters

        word : word to be checked
        required: string of the required letter

    >>> uses_all('banana', 'ban')
    True
    >>> uses_all('apple', 'api')
    False
    """
    for letter in required.lower():
        if letter not in word.lower():
            return False
    return True


def uses_only(word, available):
    """
    Checks whether a word uses only the available letters

        word : word to be checked
        available : string of the available letters

    >>> uses_only('banana', 'ban')
    True
    >>> uses_only('apple', 'apl')
    False
    """
    for letter in word.lower():
        if letter not in available.lower():
            return False
    return True


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
    if len(word) < 4:
        return False

    if not uses_all(word, required):
        return False

    return uses_only(word, available)


def score_word(word, available):
    """
    Compute the score for an acceptable word

        word : word to be scored
        available : string of the available letters

    >>> score_word('card', 'ACDLORT')
    1
    >>> score_word('color', 'ACDLORT')
    5
    >>> score_word('cartload', 'ACDLORT')
    15
    """
    n = len(word)
    if n == 4:
        return 1

    if uses_all(word, available):
        return n + 7
    else:
        return n


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    available = "ACDLORT"
    required = "R"

    total = 0
    for line in open("data/words.txt"):
        word = line.strip()
        if check_word(word, available, required):
            score = score_word(word, available)
            total = total + score
            print(word, score)

    print("Total score", total)
