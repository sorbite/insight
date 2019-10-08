import string
import re
import pandas as pd
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from PreprocessDataset import extract_skillset, clean_text


def merge_course_content(df):
    df.course_title = df.course_title.apply(lambda x: x.lower() + ', ')
    df.checked_skill = df.checked_skill.apply(lambda x: str(x) + ', ')
    df.checked_job = df.checked_job.apply(lambda x: str(x) + ', ')
    df.course_description = df.course_description.apply(
        lambda x: extract_skillset(x))
    df['content'] = df.course_title + df.course_description + \
        df.checked_skill
    df.content = df.content.apply(lambda x:
                                  str(''.join(list(filter(lambda ch: ch not in "[]'", x))).split(', ')))
    return df


def merge_job_content(df):
    df.checked_title = df.checked_title.apply(lambda x: x.lower() + ', ')
    df['checked_description_2'] = df.checked_description_checked.apply(
        lambda x: extract_skillset(x))
    df['content'] = df.checked_description_2.apply(lambda x:
                                  str(''.join(list(filter(lambda ch: ch not in "[]'", x))).split(', ')))
    return df


def cosine_sim(job_content, course_content):
    tfidf_vect = TfidfVectorizer(analyzer=clean_text, ngram_range=(1, 4))
    tfidf = tfidf_vect.fit_transform([job_content, course_content])
    return ((tfidf * tfidf.T).A)[0, 1]


def recommendation(df, df_course, course_num=5):
    df_job = merge_job_content(df)
    job_content = df_job.job_content
    df_course['score'] = df_course.content.apply(
        lambda x: cosine_sim(job_content, x))
    df_sorted = df_course.sort_values(
        'score', ascending=False, inplace=False).reset_index(drop=True)
    df_results = df_sorted.drop(['content', 'score'], axis=1)
    return df_results[:course_num]
