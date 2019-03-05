### Running simulations

All simulations use the same model, the only difference being the input
presented to the input modules: either `_sensory`  or `_interoception`. To
present the input, right-click onto the module (i.e. labelled gray box) and
select `Semantic pointer cloud`. This will open a small window with a label,
which is empty initially and will be populated with semantic pointer labels
once the simulation starts running. Press the play button in the right corner,
wait for the network to build (this can take some time). Once
the network is running (the play button will convert into pause) the inputs can
be presented by right-clicking onto the semantic pointer cloud, selecting `Set
value...` and typing in the name of the semantic pointer.

Currently input from one simulation will stay in the network when wanting to
start another simulation, which can cause problems. After running one
simulation, the best way to run another one is to restart the model by
refreshing (F5).

### Simulation 1 
Present input `SNAKE` to the sensory input. Emotions such as
`ANXIETY, FEAR, SHAME` and `STRESS` should appear in the executive network.

### Simulation 2 
As in Sim 1, but after a while the input is changed to
`SNAKE+GLASS`. This should slowly prompt `ZOO` in the language and episodic
networks with emotions changing to `HAPPINES, JOY, LOVE, PLEASURE` and `PRIDE`.

### Simulation 3 
For this simulation, we will need the `interoception` semantic
pointer cloud where we will present input. Interoception is presented with
a weighted combination of semantic pointers: 
```
0.25*(FELT_HEARTBEAT_GETTING_FASTER+MUSCLES_TENSING_WHOLE_BODY+FELT_BREATHING_GETTING_FASTER+SWEATED)
```

and the sensory network with `EUPHORIC`. This should result with positive
emotions in the executive network. To test the `ANGRY` condition, restart the
network (F5), wait for the build process to finish, present the same input to
interoception and `ANGRY` to the sensory semantic pointer cloud.

### Simulation 4

This simulation uses `interoception` network for input. First, present the
input `FROWNED` to see negative emotions, and then `SMILED` to see the
positive.

### Simulation 5

This simulation is computationally the most expensive because it includes
additional mechanism to parse a sentence. To enable this option, change the
last line in the text editor by replacing `query=False` with `query=True`. This
will create additional module in the network, called `query` whose semantic
pointer cloud can be used to query emotions of roles in the sentence. 

The sentence is presented to the sensory network, and following are several
examples of valid inputs for sensory and query networks:


``` 
Sensory:    MOTHER*SUBJECT+SHOUT_AT*ACTION+CHILD*OBJECT 
Query:      MOTHER or CHILD 
``` 
To query the emotions of the subject or the object, present input to the query.
For example, to query emotions of a mother who is shouting at a child, present
the input: `MOTHER*SUBJECT+SHOUT_AT*ACTION+CHILD*OBJECT` to the sensory
network (it might not appear in the cloud), and `MOTHER` to the query network.
After running simulation for a while, the `episodic` network should come up
with `SHOUT_AT_S` which can be interpreted as the subject of the action `shout
at`, and the corresponding emotions of that subject are shown in the executive
network. To query emotions of a child, present `CHILD` to the query.

### Simulation 6
In this simulation, we test the model's ability to represent mixed emotions as in a scenario where a person is eating a cake while being on a diet. The assumption is that this might prompt positive emotions (as a result of a tasty cake) and negative emotions (guilt from eating something that's not part of the diet).
As in simulation 5, we will also use the query network to probe emotional responses.
First, in the sensory network we type in `CAKE*TASTE` and in the query network we present `TASTE`. We observe positive emotions such as *contentment, happiness* and *pleasure*. Then, in the sensory network we change input to `THOUGHT*OBESITY` (or `THOUGHT*OBESITY+CAKE*TASTE`), and in query `THOUGHT`. The conceptualization network will slowly converge to represent `BINGE_EAT` and the emotional responses will change and also include emotions with negative valence.
