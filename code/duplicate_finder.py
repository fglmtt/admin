import hashlib
from collections import defaultdict
import os


def is_image(path, extensions):
    """
    Check whether the path ends with one of the extensions

    path : path to a file
    extensions : list of extensions

    >>> is_image('photo.jpg', ['jpg', 'jpeg'])
    True
    >>> is_image('PHOTO.JPG', ['jpg', 'jpeg'])
    True
    >>> is_image('notes.txt', ['jpg', 'jpeg'])
    False
    """
    for extension in extensions:
        if path.lower().endswith(extension):
            return True
    return False


def md5_digest(filename):
    data = open(filename, "rb").read()
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    digest = md5_hash.hexdigest()
    return digest


def add_path(path, d):
    """
    Compute the digest of path and update a defaultdict of lists as follows
    - the key is the digest of the image
    - the value is a list of paths to files with the same digest

    path : path to a file
    d : defaultdict of lists

    >>> add_path('data/photos/feb-2023/photo1.jpg', defaultdict(list))
    defaultdict(<class 'list'>, {'dace5bcdd614b5a23e465b1edc406bc3': ['data/photos/feb-2023/photo1.jpg']})
    """
    digest = md5_digest(path)
    d[digest].append(path)
    return d


def walk_images(dirname, d):
    """
    Walk the directory tree and return a defaultdict of lists where
    - the key is the digest of the image
    - the value is a list of paths to the images with the same digest

    path : path to a directory
    d : defaultdict of lists
    """
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)

        if os.path.isfile(path) and is_image(path, ["jpg", "jpeg"]):
            add_path(path, d)
        elif os.path.isdir(path):
            walk_images(path, d)

def main():
    d = defaultdict(list)
    walk_images(".", d)
    for digest, paths in d.items():
        if len(paths) > 1:
            for path in paths:
                print(path)

if __name__ == "__main__":
    import doctest

    doctest.testmod()

    main()
