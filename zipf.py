#!/usr/bin/env python3
from spacy.lang.en import English
nlp = English(pipeline=[], max_length=5000000)

import math
import os.path
from collections import Counter
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import random


def H_approx(n):
    """
    Returns an approximate value of n-th harmonic number.
    http://en.wikipedia.org/wiki/Harmonic_number
    """
    # Euler-Mascheroni constant
    gamma = 0.57721566490153286060651209008240243104215933593992
    return gamma + math.log(n) + 0.5/n - 1./(12*n**2) + 1./(120*n**4)


def do_zipf_plot(counts, label=""):
    fig = pyplot.figure()

    # obtain C(w), R(w), and K(w)
    count_freq = []
    expected_rel_freq = []

    types = len(counts.items())
    tokens = counts.total()
    harmonic = H_approx(types)
    scaling = tokens / harmonic
    
    i = 0
    rank = list(range(1, types+1))
    for elem, count in counts.most_common():
        count_freq.append(count)
        expected_rel_freq.append((scaling / rank[i]) / tokens)
        i += 1
    
    rel_freq = []
    for f in count_freq:
        rel_freq.append(f / tokens)
        
    # Create log plot of R(w) vs. K(w)
    pyplot.loglog(rank, rel_freq, label="Empirical")
    pyplot.loglog(rank, expected_rel_freq, label="Theoretical")
    pyplot.xlabel("log(rank)")
    pyplot.ylabel("log(freq)")
    pyplot.suptitle("Zipf's Law for " + label)
    pyplot.legend(loc="lower left")

    pyplot.savefig('zipf_{}.png'.format(label))
    pyplot.close()
    

def read_all(directory, extension=None):
    new_counter = Counter()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if extension is None:
                file_counter = read_one(root + "/" + file)
            if os.path.splitext(root + file)[1] == extension:
                file_counter = read_one(root + "/" + file)

            new_counter += file_counter
    return new_counter
    
    

def read_one(fname, rdm=False):
    # Write file with random characters    
    if rdm:
        with open(fname, 'w', encoding='latin1') as fp: 
            rdm_chars = []
            for i in range(10**5):
                rdm_char = random.choice("abcdefghijklmnopqrstuvwxyz ")
                rdm_chars.append(rdm_char)
            text = "".join(rdm_chars)
            fp.write(text)

    # Read file
    text = ""
    with open(fname, 'r', encoding='latin1') as fp: 
        text = fp.read()
    
    # Put tokens in counter
    doc = nlp(text)
    counter = Counter()
    for token in doc:
        counter[token.text.lower()] += 1
    
    return counter


def plot_all(directory):
    counts = read_all(directory, ".txt")
    do_zipf_plot(counts, os.path.basename(directory))
    print("Number of Tokens (Gutenberg): " + str(counts.total()))

def plot_one(fname, random=False):
    if random:
        counts = read_one(fname, random)
    counts = read_one(fname)
    title = os.path.splitext(os.path.basename(fname))[0]

    do_zipf_plot(counts, label=title)

def main():
    plot_one('/courses/cs159/data/gutenberg/carroll-alice.txt')
    # plot_one('/courses/cs159/data/gutenberg/bryant-stories.txt')
    # plot_one('/courses/cs159/data/gutenberg/edgeworth-parents.txt')
    # plot_one('/courses/cs159/data/gutenberg/chesterton-ball.txt')
    # plot_one('/courses/cs159/data/gutenberg/blake-poems.txt')
    # plot_one('/courses/cs159/data/gutenberg/austen-sense.txt')
    plot_all('/courses/cs159/data/gutenberg')

    plot_one('random.txt', True)


if __name__ == "__main__":
    main()
