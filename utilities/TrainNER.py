import json
import random
import logging
from spacy.gold import GoldParse
from spacy.scorer import Scorer
import spacy
import pandas as pd


def convert_to_spacy(jsonfile):
    '''
    Creates NER training data in Spacy format
    '''
    try:
        tranin_data = []
        lines = []
        with open(jsonfile, 'r') as f:
            lines = f.readlines()

        for line in lines:
            data = json.loads(line)
            text = data['content']
            entities = []
            for annotation in data['annotation']:
                # only a single point in text annotation.
                point = annotation['points'][0]
                labels = annotation['label']
                # handle both list of labels or a single label.
                if not isinstance(labels, list):
                    labels = [labels]

                for label in labels:
                    # dataturks indices are both inclusive [start, end] but spacy is not [start, end)
                    entities.append((point['start'], point['end'] + 1, label))

            tranin_data.append((text, {"entities": entities}))

        return tranin_data
    except Exception as e:
        logging.exception("Unable to process \n" + "error = " + str(e))
        return None



def train_NER_spacy(blank_model=True, load_model='model', jsonfile='traindata.json',
                create_model_name='skill', model_output=True, n_iter=10):
    '''
    Train Spacy NER using traindata.json
    '''
    tranin_data = convert_to_spacy(jsonfile)
    if blank_model == False:
        nlp = spacy.load(load_model)  # load pretrained spaCy model
    else:
        nlp = spacy.blank('en')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)  # last
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for content, annotations in tranin_data:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])
    if blank_model == True:
        optimizer = nlp.begin_training()
    else:
        optimizer = nlp.entity.create_optimizer()
        
    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

    with nlp.disable_pipes(*other_pipes):  # only train NER
        for itn in range(n_iter):
            print("Statring iteration " + str(itn))
            random.shuffle(tranin_data)
            losses = {}
           
            for content, annotations in tranin_data:
                nlp.update(
                    [content],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    if model_output == True:
        nlp.meta["name"] = create_model_name
        nlp.to_disk('/home/xinda/insight/model')