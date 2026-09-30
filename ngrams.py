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
        print("Elem Attribute " + str(elem.attrib[attribute]))
        if elem.attrib[attribute] == value:
            doc = nlp(html.unescape(elem.text))
            print("Elem Text" + str(elem.text))
            print(doc)
            unigrams = get_unigrams(doc)
            print("Unigrams: " + str(unigrams))
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
    bigrams = []

    i = 0
    while i+1 < len(doc):
        token = doc[i]
        next_token = doc[i+1]
        if do_lower:
            curr_bigram = (token.text.lower(), next_token.text.lower())
            bigrams.append(curr_bigram)
        else:
            curr_bigram = (token.text, next_token.text)
            bigrams.append(curr_bigram)
        i += 1
    
    return bigrams

def get_trigrams(doc, do_lower=True):
    trigrams = []

    i = 0
    while i+2 < len(doc):
        token = doc[i]
        second_tok = doc[i+1]
        third_tok = doc[i+2]
        if do_lower:
            curr_trigram = (token.text.lower(), second_tok.text.lower(), third_tok.text.lower())
            trigrams.append(curr_trigram)
        else:
            curr_trigram = (token.text, second_tok.text, third_tok.txt)
            trigrams.append(curr_trigram)
        i += 1
    
    return trigrams

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
    # the path: /courses/cs159/data/patronize/patronize_sample.xml

    counter = get_examples(args.examples, 'condescension', 'true')
    # print(counter.most_common(20))
    print("the: " + counter['the'])
    print("opportunity: " + counter['opportunity'])
    print("zero: " + counter['zero'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # 'rb' means "read as bytes", which means that it doesn't assume
    # the data is UTF-8 text when it's read in.
    parser.add_argument("--examples", "-a",
                        type=argparse.FileType('rb'),
                        help="Content of examples")

    args = parser.parse_args()
    main(args)
