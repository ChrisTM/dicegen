#! /bin/env python

"""
Command-line tool for generating strong and memorable passphrases in the style
(but not the spirit) of Diceware.

Diceware is a non-electronic system for generating strong passphrases by using
dice and a numbered wordlist. This tool removes the dice from Diceware, missing
the point entirely, but adding a bunch of convienence.

Read more about Diceware at http://world.std.com/~reinhold/diceware.html
"""

import argparse
import os
from random import SystemRandom
import re
import sys

random = SystemRandom()  # Use a higher-quality RNG


def make_passphrase(words, num_words):
    return ' '.join(random.choice(words) for k in range(num_words))


def read_wordlist(filename, format='diceware'):
    """
    Return a list of the words in the wordlist `filename`.
    """
    file_ = open(filename, 'r')

    if format == 'diceware':
        expression = re.compile(r"^\d{5}\t(?P<word>\S+)$")
    elif format == 'simple':
        expression = re.compile(r"^(?P<word>\S+)$")
    else:
        raise ValueError('"{}"is not a supported word list format.'.format(format))

    words = []
    for line in file_:
        match = expression.match(line)
        if match:
            word = match.group('word')
            words.append(word)

    file_.close()
    return words


def make_parser():
    parser = argparse.ArgumentParser(
        description="Generate a Diceware-style passphrase.",
    )

    parser.add_argument(
        "-n", "--number",
        dest="num_passphrases",
        type=int,
        default=1,
        help="number of passphrases to generate [default: %(default)s]",
        metavar="NUM"
    )

    parser.add_argument(
        "-w", "--words",
        dest="num_words",
        type=int,
        default=5,
        help="number of words to use in each passphrase [default: %(default)s]",
        metavar="NUM"
    )

    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    word_list = os.path.join(BASEDIR, 'diceware.wordlist.asc')

    parser.add_argument(
        "--word-list",
        default=word_list,
        help="location of a wordlist [default: %(default)s]",
        metavar="FILE"
    )

    parser.add_argument(
        "--word-list-format",
        default="diceware",
        help="format of wordlist [possible values: diceware, simple] [default: %(default)s]",
        metavar="FORMAT"
    )

    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()

    words = read_wordlist(args.word_list, args.word_list_format)

    if len(words) == 0:
        sys.stderr.write('Error: The word list does not contain any valid words. Please ensure that the word list is properly formatted and that the correct word list format is specified with the "--word-list-format" option.\n')
        sys.exit(1)

    for i in range(args.num_passphrases):
        passphrase = make_passphrase(words, args.num_words)
        print passphrase


if __name__ == '__main__':
    main()
