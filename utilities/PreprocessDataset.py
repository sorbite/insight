import string
import nltk
import re
import pandas as pd
import numpy as np
import random
import spacy


def clean_text(text):
    '''
    To remove punctuation, tokenize, remove stopwords, and lemmatize
    '''
    stopword = nltk.corpus.stopwords.words('english')
    text = "".join([word.lower()
                    for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    skillset = list(set(tokens))
    wl = nltk.WordNetLemmatizer()
    tokens = [wl.lemmatize(word) for word in tokens if word not in stopword]
    return skillset


def extract_skillset(content='content', model='en_core_web_lg'):
    '''
    To return the entities (skill keywords) from the job posters or course description.
    '''
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(content)
    skillset = [e.text for e in doc.ents if (
        (e.label_ == 'ORG') & (len(e.text) >= 1))]
    return skillset


def point_skill(content, skill_list):
    '''
    Point to the skills in content
    '''
    list_tmp = []
    for skill in skill_list:
        try:
            start_point = content.index(skill)
            end_point = start_point + len(skill)
        except:
            start_point = None
            end_point = None
        list_tmp.append({"label": ["skill"], "points": [
                        {"start": start_point, "end": end_point, "text": skill}]})
    return list_tmp
