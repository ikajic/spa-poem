from nengo import spa
from epa_sentences import epa_sentences
import os
import numpy as np
import pickle


def get_all_words():
    """
    Load 3D-EPA values for the whole dictionary.
    """
    data_path = os.path.join(
        os.path.dirname(__file__), os.pardir, 'data', 'epa_dimensions.pkl')

    with open(data_path, 'r') as f:
        epa_all = pickle.load(f)

    return epa_all.keys()


def create_spa_vocabulary(experiment, randomize=True, D=128):
    """
    Read the experiment specific data from a dictionary `experiment` and create
    a dictionary with a SPA vocabulary for every ensemble.
    If randomize is True random vectors instead of orthogonal ones will be
    created.
    """
    networks = experiment.vocab.keys()
    vocab = {}

    for network in networks:
        try:
            words = experiment.vocab[network]
        except KeyError:
            raise Exception(("Vocabulary for network %s undefined in the " +
                            "experiment %s.") % (network, experiment['name']))

        # orthogonal vectors E, P and A for the affect network
        rand = True
        if 'affect' in network:
            rand = False
        vocab[network] = spa.Vocabulary(D, randomize=rand)

        for word in words:
            vocab[network].parse(word)

        vocab[network].add('EMPTY', np.zeros(D))

    return vocab


def get_epa_expression(words):
    """
    Generate a string expression of a form:
    x*E+y*P+z*A
    for every word in `words`, where (x, y, z) are 3D coordinates
    extracted from a pickled database of EPA values.
    """

    data_path = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                             'epa_dimensions.pkl')
    with open(data_path, 'rb+') as f:
        epa_all = pickle.load(f)

    epa_subset = {word_epa: epa for word_epa, epa in
                  epa_all.items() if word_epa in words}

    # EPA values are in the interval [-4, 4], normalise to [-1, 1] for SPA
    norm_fact = 4.
    keys = []

    for word in words:
        e, p, a = 0, 0, 0
        try:
            epa_values = epa_subset[word]/norm_fact
            e, p, a = epa_values[0], epa_values[1], epa_values[2]
        except KeyError:
            if word not in epa_sentences:
                print('%s does not have EPA value in EPA space' % word)

        if word in epa_sentences:
            e, p, a = epa_sentences[word]
        expr = ("%.2f*E+%.2f*P+%.2f*A" % (e, p, a)).replace("+-", "-")
        keys.append(expr)

    return keys


def add_vocabularies(vocab, name1, name2):
    """
    New vocabulary containing semantic pointers from vocab1 and vocab2.
    name1:      name of the first vocabulary
    name2:      name of the second vocabulary
    """

    vocab1, vocab2 = vocab[name1], vocab[name2]
    d1, d2 = vocab1.dimensions, vocab2.dimensions
    assert d1 == d2

    new_vocab = spa.Vocabulary(d1)

    # TODO
    # first add items from vocab1
    for key1 in vocab1.keys:
        vec1 = vocab1[key1].v
        sp1 = name1.capitalize() + '_' + key1
        new_vocab.add(sp1, vec1)

    # and then from vocab2
    for key2 in vocab2.keys:
        vec2 = vocab2[key2].v
        sp2 = name2.capitalize() + '_' + key2
        new_vocab.add(sp2, vec2)

    return new_vocab


def keys_from_input(keys, factor=None):
    new_keys = []
    prefix = ''

    if factor is not None:
        prefix = str(factor) + '*'

    for key in keys:
        word = key
        if '_' in key and any(w in key for w in ('Sensory', 'Episodic',
                                                 'Interoception', 'Language',
                                                 'Conceptualization')):
                word = key.split('_', 1)[1]
        word = prefix + word
        new_keys.append(word)
    return new_keys
