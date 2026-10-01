#!/usr/bin/env python3
from spacy.lang.en import English
nlp = English(pipeline=[], max_length=5000000)

import argparse
from lxml import etree
from collections import Counter
import html


def do_xml_parse(fp, tag):
    """ 
    Iteratively parses XML files
    """
    fp.seek(0)

    for (event, elem) in etree.iterparse(fp, tag=tag):
        yield elem
        elem.clear()

def get_examples(args, attribute, value):
    counter = Counter()

    # go through each example after parsing
    for elem in do_xml_parse(args, ("example",)):
        if elem.attrib[attribute] == value:
            doc = nlp(html.unescape(elem.text))
            unigrams = get_unigrams(doc)
            for unigram in unigrams:
                counter[unigram] += 1

    return counter

    
def get_unigrams(doc, do_lower=True): 
    unigrams = []
    for token in doc:
        if do_lower:
            unigrams.append(token.text.lower())
        else:
           unigrams.append(token.text)  
    
    return unigrams
        

def get_bigrams(doc, do_lower=True):
    unigram_1 = get_unigrams(doc)
    unigram_1.pop(len(unigram_1)-1)
    unigram_2 = get_unigrams(doc)
    unigram_2.pop(0)

    bigrams = list( zip(unigram_1, unigram_2) )
    return bigrams


def get_trigrams(doc, do_lower=True):
    unigram_1 = get_unigrams(doc)   # pop the last two elem
    unigram_1.pop(len(unigram_1)-1)
    unigram_1.pop(len(unigram_1)-1)

    unigram_2 = get_unigrams(doc)   # pop the front and back elem
    unigram_2.pop(len(unigram_2)-1)
    unigram_2.pop(0)

    unigram_3 = get_unigrams(doc)   # pop first two elems
    unigram_3.pop(0)
    unigram_3.pop(0)

    bigrams = list( zip(unigram_1, unigram_2, unigram_3) )
    return bigrams

def compare(train, test, unique=False):
    test_count = 0
    for item, count in test.items():
        if item not in train:
            if unique:
                test_count += 1
            else:
                test_count += count
    
    test_total = 0
    if unique:
        test_total = len(test.items())
    else:
        test_total = test.total()

    return (test_count, test_total)
        

def do_experiment(args, attribute, train_value, test_value): 
    """Print a pandoc-compatible table of experiment results"""
    train = get_examples(args, attribute, train_value) 
    test = get_examples(args, attribute, test_value)

    table_header = "Results for {}, using {} as train and {} as test:"
    print(table_header.format(attribute, train_value, test_value))

    print("| Order | Type/Token | Total | Zeros | % Zeros | ")
    print("| ----  | ---------- | ----- | ----- | ------- | ")
    table_row = "| Bigram | {typetoken} | {total} | {zeros} | {pct:.1%} | "

    for do_types in (True, False):
        typetoken = "Type" if do_types else "Token" 
        num_zeros, N = compare(train, test, do_types)
        print(table_row.format(typetoken=typetoken, 
              total=N, zeros=num_zeros, pct=num_zeros/N))
    print()

def main(args):
    # the path: /courses/cs159/data/patronize/patronize_sample.xml

    counter = get_examples(args.examples, 'condescension', 'true')
    print("the: " + str(counter['the']))
    print("opportunity: " + str(counter['opportunity']))
    print("zero: " + str(counter['zero']))

    # Testing compare()
    compare(Counter(['a','b','c']), Counter(['c','d','d']), unique=True)
    compare(Counter(['a','b','c']), Counter(['c','d','d']), unique=False)

    # print("Appear in condenscending (true) examples, don't appear in neutral (false) examples.")
    # do_experiment(args.examples, 'condescension', 'false', 'true')

    # print("Appear in neutral (false) examples, don't appear in condenscending (true) examples.")
    # do_experiment(args.examples, 'condescension', 'true', 'false')

    print("Appear in b examples, don't appear in a examples.")
    do_experiment(args.examples, 'randomchunk', 'a', 'b')

    print("Appear in a examples, don't appear in b examples.")
    do_experiment(args.examples, 'randomchunk', 'b', 'a')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # 'rb' means "read as bytes", which means that it doesn't assume
    # the data is UTF-8 text when it's read in.
    parser.add_argument("--examples", "-a",
                        type=argparse.FileType('rb'),
                        help="Content of examples")

    args = parser.parse_args()
    main(args)
