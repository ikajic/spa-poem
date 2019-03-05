import numpy as np


class Experiment(object):

    def __init__(self):
        self.emotion_tags = ['ANGER', 'ANXIETY', 'BEING_HURT',
                             'COMPASSION', 'CONTEMPT', 'CONTENTMENT',
                             'DESPAIR', 'DISAPPOINTMENT', 'DISGUST', 'FEAR',
                             'GUILT', 'HAPPINESS', 'HATE', 'INTEREST',
                             'IRRITATION', 'JEALOUSY', 'JOY', 'LOVE',
                             'PLEASURE', 'PRIDE', 'SADNESS', 'SHAME', 'STRESS',
                             ]
        vocab = set(
            ['SNAKE', 'GLASS', 'ZOO', 'SMILED', 'FROWNED',
                'FELT_HEARTBEAT_GETTING_FASTER',
                'FELT_HEARTBEAT_SLOWING_DOWN',
                'MUSCLES_TENSING_WHOLE_BODY',
                'FELT_BREATHING_GETTING_FASTER', 'SWEATED', 'ANGRY',
                'CONSEQUENCES_NEGATIVE_FOR_SOMEBODY_ELSE',
                'FELT_GOOD',
                'FELT_NERVOUS',
                'FELT_AT_EASE',
                'EUPHORIC', 'MOTHER', 'SHOUT_AT', 'CHILD', 'SUBJECT',
                'OBJECT', 'ACTION', 'CHAIR',
                'CAKE', 'BINGE_EAT', 'PIZZA', 'PLANT', 'WALL',
                'OBESITY'])

        self.vocab = {}
        self.vocab['episodic'] = list(vocab)
        self.vocab['affect'] = ['E', 'P', 'A']
        self.vocab['executive'] = self.emotion_tags
        self.vocab['sensory'] = list(vocab)
        self.vocab['language'] = list(vocab)
        self.vocab['conceptualization'] = list(vocab)
        self.vocab['interoception'] = list(vocab)

    # this is default in Nengo, identity transform
    def custom_transform(self, spa_voc, D=128):
        """
        In Nengo this transform is by default an identity function. Here, we
        implement a rule of a form 'if snake and glass, then zoo'.
        """
        trans_mat = np.zeros((D, D))

        for word_str in spa_voc.keys:
            f = 1
            word_vec = spa_voc[word_str].v
            # representing a in pre-population causes 
            # b in post-population
            a, b, = word_vec, word_vec

            if word_str == 'SNAKE' or word_str == 'GLASS':
                a, b, f = a, a-1.1*spa_voc['ZOO'].v, 2

            if word_str == 'OBESITY':
                a, b, f = a, spa_voc['BINGE_EAT'].v, 2

            if word_str == 'ZOO':
                f = 2
                trans_mat += np.outer(spa_voc['GLASS'].v +
                                      spa_voc['SNAKE'].v,
                                      2.5*word_vec -
                                      spa_voc['GLASS'].v -  # inhibit
                                      spa_voc['SNAKE'].v)   # inhibit

            trans_mat += f*np.outer(a, b)

        return trans_mat
