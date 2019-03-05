import nengo
import simulations as sim
import utils
import numpy as np

from nengo import spa

Memory = spa.AssociativeMemory

def create_model(D=512, incl_interoception=False, query=False):
    vocabulary = sim.Experiment()

    # Create semantic pointers in each network
    spa_voc = utils.create_spa_vocabulary(vocabulary, randomize=True, D=D)
    
    # Episodic and affect integrate two vocabularies
    input_episodic = utils.add_vocabularies(spa_voc, 'sensory', 'conceptualization')
    input_affect = utils.add_vocabularies(spa_voc, 'episodic', 'interoception')

    with spa.SPA('POEM') as model:
        # Sensory
        model._sensory = spa.State(D, vocab=spa_voc['sensory'])
                            
        # Episodic
        episodic_output_keys = utils.keys_from_input(input_episodic.keys)
        
        zoo_idx = input_episodic.keys.index('Conceptualization_ZOO')
        episodic_output_keys[zoo_idx] = '2*ZOO-2*GLASS-2*SNAKE'

        model._episodic = Memory(input_vocab=input_episodic,
                                output_vocab=spa_voc['episodic'],
                                input_keys=input_episodic.keys,
                                output_keys=episodic_output_keys,
                                wta_output=True,
                                wta_inhibit_scale=0.1,
                                threshold_output=True)

        ep_output_vectors = np.array([spa_voc['episodic'].parse(key).v for key in\
            episodic_output_keys], ndmin=2)

        if query:
            model.query = spa.State(D, vocab=spa_voc['sensory'])
            model.bind = spa.Bind(D, invert_b=True)
            nengo.Connection(model.bind.output, model._episodic.input,
                             transform=3)
            nengo.Connection(model._sensory.input, model.bind.A)
            nengo.Connection(model.query.input, model.bind.B)
        else:
            nengo.Connection(model._sensory.output, model._episodic.input,
                             transform=3)  # 3 because inputs set by cloud are
                                           # not normalized

        # Language
        model._language = Memory(input_vocab=spa_voc['episodic'],
                                output_vocab=spa_voc['language'])

        nengo.Connection(model._episodic.am.elem_output, model._language.input,
                         transform=ep_output_vectors.T)
                         
        # Conceptualization
        model._conceptualization = Memory(input_vocab=spa_voc['language'],
                               output_vocab=spa_voc['conceptualization'],
                               wta_output=True,
                               wta_synapse=.05,
                               threshold_output=True,
                               wta_inhibit_scale=.3)
                               
        trans_mat = vocabulary.custom_transform(spa_voc['language'], D=D)
        nengo.Connection(model._language.output, model._conceptualization.input,
                         transform=trans_mat.T, synapse=0.01)
        nengo.Connection(model._conceptualization.output, model._episodic.input,
                         synapse=0.3)
        
        # Interoception
        if incl_interoception:
            model._interoception = spa.State(D, vocab=spa_voc['interoception'])

        # Affect: EPA expressions at the output
        input_words = utils.keys_from_input(input_affect.keys)
        epa_expressions_words = utils.get_epa_expression(input_words)

        model._affect = Memory(input_vocab=input_affect,
                              output_vocab=spa_voc['affect'],
                              input_keys=input_affect.keys,
                              output_keys=epa_expressions_words,
                              wta_output=False,
                              threshold=0.4)
        if incl_interoception:
            nengo.Connection(model._interoception.output, model._affect.input,
                             transform=1.)
        
        print(input_affect.keys)                         
        
        # Emotion detection network (comment if not needed)
        model.active = nengo.Ensemble(n_neurons=200, dimensions=3)
        model.emotion_present = nengo.Ensemble(n_neurons=50, dimensions=1)
        nengo.Connection(model._affect.output[[0, 1, 2]], model.active)
        nengo.Connection(model.active, model.emotion_present, function=lambda x: np.sum(x**2))
        
        
        nengo.Connection(model._episodic.output, model._affect.input)
        # Executive: EPA expressions at the input
        emotion_tags = spa_voc['executive'].keys
        epa_expressions = utils.get_epa_expression(emotion_tags)
        
        model._executive = Memory(input_vocab=spa_voc['affect'],
                                 output_vocab=spa_voc['executive'],
                                 input_keys=epa_expressions,
                                 output_keys=emotion_tags,
                                 threshold=0.8)

        nengo.Connection(model._affect.output, model._executive.input,
                         transform=3)
                         
    return model, spa_voc

model, _ = create_model(D=512,
                        incl_interoception=False,
                        query=False)  ## Set true only for Sim 5 and 6

