# poem-model
Implementation of the model presented in `The Semantic Pointer Theory of
Emotion: Integrating Physiology, Appraisal and Construction.`

## 1. Installation instructions
The model is implemented in Python 3.6 using the [Nengo](https://github.com/nengo/nengo) neural simulator. 

Python packages required to run the model and reproduce paper results are
listed in `requirements.txt`.

## 2. Running the model

After successfully installing all required packages, the model can be run from a console by typing:
```
nengo model.py
```
Nengo GUI should open as a web-interface with a an outline of the network on the left and the text editor on the right. How to run simulations is explained in `src/README.md`.

## 3. Project directory structure and file descriptions

### src/ 
Directory containing the model source code.

`model.py` The source code of our model. It reads the data from
‘simulations.py’ file and uses to simulate an experiment.

`simulations.py` Contains single `Experiment` class that stores words used in all experiments.

`utils.py` Utilities. Various functions for generating and handling of EPA
vectors that are used in the model.

### scripts/ 
Directory containing the scripts not needed to run the model per
se, but are used to generate the data the model uses. 
It is not necessary to run any scripts in these folders, as a single file
(`epa_dimensions.pkl`) is small enough (143KB) to be added to this repository.

`read_epa.py` Process the xls sheets stored in `./data`and create a file used by the model to
create mappings between words and the EPA values

### data/
Data used to build and run the model. Mostly .xls sheets with EPA values for
various concepts: Actions, EmotionLabels, Identities, Settings and more
elaborate scenarios (Fontaine). Available upon request.
