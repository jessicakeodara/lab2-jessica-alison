#!/usr/bin/env python3

import argparse
from lxml import etree
from collections import Counter


def do_xml_parse(fp, tag):
    """ 
    Iteratively parses XML files
    """
    fp.seek(0)

    for (event, elem) in etree.iterparse(fp, tag=tag):
        yield elem
        elem.clear()

def get_examples(args, attribute, value):
    pass

def get_unigrams(doc, do_lower=True): 
    pass

def get_bigrams(doc):
    pass

def get_trigrams(doc):
    pass

def compare(train, test, unique=False):
    pass

def do_experiment(args, attribute, train_value, test_value): 
    """Print a pandoc-compatible table of experiment results"""
    train = get_examples(args, attribute, train_value) 
    test = get_examples(args, attribute, test_value)

    table_header = "Results for {}, using {} as train and {} as test:"
    print(table_header.format(attribute, train_value, test_value))

    print("| Order | Type/Token | Total | Zeros | % Zeros | ")
    print("| ----  | ---------- | ----- | ----- | ------- | ")
    table_row = "| Unigram | {typetoken} | {total} | {zeros} | {pct:.1%} | "

    for do_types in (True, False):
        typetoken = "Type" if do_types else "Token" 
        num_zeros, N = compare(train, test, do_types)
        print(table_row.format(typetoken=typetoken, 
              total=N, zeros=num_zeros, pct=num_zeros/N))
    print()

def main(args):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # 'rb' means "read as bytes", which means that it doesn't assume
    # the data is UTF-8 text when it's read in.
    parser.add_argument("--examples", "-a",
                        type=argparse.FileType('rb'),
                        help="Content of examples")

    args = parser.parse_args()

    main(args)
