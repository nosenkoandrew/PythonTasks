from collections import Counter
from functools import lru_cache
import argparse


@lru_cache
def non_repeating_elems(txt):
    if not isinstance(txt, str):
        raise TypeError(f'Passed variable should be text, got {type(txt)}')

    res = sum(value for value in Counter(txt).values() if value == 1)
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', help='String with a text that you need', type=str, default='')
    parser.add_argument('--file', help='File with a text that you need', type=argparse.FileType('r'))
    args = parser.parse_args()
    text = args.text

    if args.file:
        text = open(args.file, 'r').read()

    print(non_repeating_elems(text))


if __name__ == '__main__':
    main()