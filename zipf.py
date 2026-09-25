#!/usr/bin/env python3
from spacy.lang.en import English
nlp = English(pipeline=[], max_length=5000000)

import math
import os.path
from collections import Counter
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot


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
    for elem, count in counts.most_common():  # wait i dont know for sure
        count_freq.append(count)
    print("count_freq: " + str(count_freq))
    
    rel_freq = []
    for f in count_freq:
        rel_freq.append(f / counts.total())

    counts_size = len(counts.items())
    rank = list(range(1, counts_size+1))


    print("rank: " + str(rank))
    print("rel_freq: " + str(rel_freq))
        
    # Create log plot of R(w) vs. K(w)
    pyplot.loglog(rank, rel_freq)
    pyplot.xlabel("log(rank)")
    pyplot.ylabel("log(freq)")
    pyplot.suptitle(label)

    pyplot.savefig('zipf_{}.png'.format(label))
    pyplot.close()
    


def read_all(directory, extension=None):
    new_counter = Counter()

    for root, dirs, files in os.walk(directory):
        print("dirs" + str(dirs))
        for dir in dirs:
            for file in files:
                if extension is None:
                    file_counter = read_one(file)
                if os.path.splitext(dir + file)[1] == extension:
                    file_counter = read_one(file)

                new_counter += file_counter
    return new_counter
    

def read_one(fname):
    # Read the file
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
    print(counts)
    do_zipf_plot(counts, os.path.basename(directory))

def plot_one(fname):
    counts = read_one(fname)
    title = os.path.splitext(os.path.basename(fname))[0]

    do_zipf_plot(counts, label=title)

def main():
    plot_one('/courses/cs159/data/gutenberg/carroll-alice.txt')
    plot_all('/courses/cs159/data/gutenberg')


if __name__ == "__main__":
    main()
