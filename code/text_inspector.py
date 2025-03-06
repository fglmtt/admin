import doctest


def clean_book(source_filename, destination_filename):
    """
    Remove everything except the book itself. Return the number of lines of the cleaned book

    source_filename : where to find the book to be cleaned
    destination_filename : where to store the cleaned book

    >>> clean_book("data/stevenson.txt", "data/stevenson_clean.txt")
    2530
    """
    start = "*** START OF THIS PROJECT GUTENBERG EBOOK THE STRANGE CASE OF DR. ***"
    end = "*** END OF THIS PROJECT GUTENBERG EBOOK THE STRANGE CASE OF DR. ***"

    source = open(source_filename)
    destination = open(destination_filename, "w")

    for line in source:
        if start in line:
            break

    for line in source:
        if end in line:
            break
        destination.write(line)

    source.close()
    destination.close()

    return len(open(destination_filename).readlines())


def count_unique_words(filename):
    """
    Count the number of unique words in a file

    filename : path to a file

    >>> count_unique_words("data/stevenson_clean.txt")
    6039
    """
    unique_words = {}
    for line in open(filename):
        seq = line.split()
        for word in seq:
            unique_words[word] = 1
    return len(unique_words)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
