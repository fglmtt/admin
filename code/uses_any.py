def uses_any(word, letters):
    """
        Checks if a word uses any of a list of letters

    >>> uses_any('banana', 'aeiou')
    True
    >>> uses_any('apple', 'xyz')
    False
    """
    for letter in word.lower():
        if letter in letters.lower():
            return True
    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
