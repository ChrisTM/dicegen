#! /bin/env python

"""
Command-line tool for generating strong and memorable passphrases in the style
(but not the spirit) of Diceware.

Diceware is a non-electronic system for generating strong passphrases by using
dice and a numbered wordlist. This tool removes the dice from Diceware, missing
the point entirely, but adding a bunch of convienence.

Read more about Diceware at http://world.std.com/~reinhold/diceware.html
"""

import optparse
import os
import random
import re
import sys


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
    parser = optparse.OptionParser(usage="%prog [-n] [-w]", version="%prog 1.2")

    parser.add_option(
        "-n",
        "--number",
        dest="number",
        type="int",
        default=1,
        help="number of passphrases to generate [default: %default]",
        metavar="NUM"
    )

    parser.add_option(
        "-w",
        "--words",
        dest="words",
        type="int",
        default=5,
        help="number of words to use in passphrase [default: %default]",
        metavar="NUM")

    BASEDIR = os.path.dirname(os.path.realpath(__file__))

    parser.add_option(
        "--word-list-file",
        dest="wordList",
        default=os.path.join(BASEDIR, 'diceware.wordlist.asc'),
        help="location of a complete Diceware wordlist [default: %default]",
        metavar="FILE")

    parser.add_option(
        "--word-list-format",
        dest="wordListFormat",
        default="diceware",
        help="how the wordlist is formatted [possible values: diceware, simple] [default: %default]",
        metavar="FORMAT")

    return parser


def main():
    parser = make_parser()
    options, args = parser.parse_args()

    words = read_wordlist(options.wordList, options.wordListFormat)

    if len(words) == 0:
        sys.stderr.write('Error: The word list does not contain any valid words. Please ensure that the word list is properly formatted and that the correct word list format is specified with the "--word-list-format" option.\n')
        sys.exit(1)

    for i in range(options.number):
        passphrase = make_passphrase(words, options.words)
        print passphrase


if __name__ == '__main__':
    main()
