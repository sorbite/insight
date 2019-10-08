import numpy as np
import pandas as pd
import re


def check_double_entry(df):
    '''
    Check double entries in the course_job column
    '''
    df['checked_job'] = df.course_job.apply(lambda x: list(
        ''.join(list(filter(lambda ch: ch not in "[]'", x))).split(', ')))
    df.checked_job = df.checked_job.apply(lambda x: list(set(x)))
    return df


def clean_course_skill(df):
    df['checked_skill'] = df.course_skill.apply(lambda x: list(
        ''.join(list(filter(lambda ch: ch not in "[]'", x))).split(', ')))
    return df


def empty_to_null(df):
    df.checked_skill = df.checked_skill.apply(
        lambda x: np.nan if x == [''] else x)
    df.checked_job = df.checked_job.apply(
        lambda x: np.nan if x == [''] else x)
    return df
