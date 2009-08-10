#! /usr/bin/python

# Diceware is a system for generating strong passphrases with a wordlist and dice for randomness. DiceGen makes this process totally electronic and automatic.
# While not in the true style of Diceware (less paranoid, and no dice), DiceGen still does a good job of generating strong and memorable passphrases.
# Be sure to read http://world.std.com/~reinhold/diceware.html for some fascinating info about the Diceware system, and check out the FAQ for caveots concerning electronic generation of passphrases.

import optparse
from os import path
import random
import re
import sys

def main():
    optParser = optparse.OptionParser(usage="%prog [-n] [-w]", version="%prog 1.2")
    optParser.add_option(
            "-n", 
            "--number", 
            dest="number", 
            type="int", 
            default=1, 
            help="number of passphrases to generate [default: %default]", 
            metavar="NUM")
    optParser.add_option(
            "-w", 
            "--words", 
            dest="words", 
            type="int", 
            default=5, 
            help="number of words to use in passphrase [default: %default]", 
            metavar="NUM")
    optParser.add_option(
            "--no-spaces",
            dest="addSpaces",
            action="store_false",
            default=True,
            help="do not add spaces between words")
    BASEDIR = path.dirname(path.realpath(__file__))
    optParser.add_option(
            "--word-list-file", 
            dest="wordList", 
            default=path.join(BASEDIR, 'diceware.wordlist.asc'),
            help="location of a complete Diceware wordlist [default: %default]", 
            metavar="FILE")
    optParser.add_option(
            "--word-list-format",
            dest="wordListFormat",
            default="diceware",
            help="how the wordlist is formatted [possible values: diceware, simple] [default: %default]",
            metavar="FORMAT")
    (options, args) = optParser.parse_args()

    # Open the word list
    try:
        wordListFile = open(options.wordList, 'r')
    except IOError:
        sys.stderr.write('Error: Wordlist "%s" cannot be opened.\n' %(options.wordList))
        return 1

    # Build the appropriate regular expression
    if options.wordListFormat == 'diceware' or 'Diceware':
        expression = re.compile(r"^\d{5}\t(?P<word>\S+)$")
    elif options.wordListFormat == 'simple':
        expression = re.compile(r"^(?P<word>\S+)$")
    else:
        try:
            raise ValueError
        except:
            sys.stderr.write('Error: "%s" is not a supported word list format.\n' %(options.wordListFormat))
            return 1

    # Create list of valid words using the regular expression from above
    wordList = []
    for line in wordListFile:
        matchObject = expression.match(line)
        if matchObject:
            word = matchObject.group('word')
            wordList.append(word)
    wordListFile.close()

    # Check for a non-empty wordlist
    if len(wordList) is 0:
        try:
            raise ValueError
        except ValueError:
            sys.stderr.write('Error: The word list does not contain any valid words. Please ensure that the word list is properly formatted and that the correct word list format is specified with the "--word-list-format" option.\n')
            return 1

    # Build and print the passphrases
    separator = ''
    if options.addSpaces:
        separator = ' '
    for i in xrange(options.number):
        passphrase = ''
        passphrase = separator.join([random.choice(wordList) for k in xrange(options.words)])
        print passphrase

main()
