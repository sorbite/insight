import numpy as np
import pandas as pd
import re

def check_job_title(df, occupation):
    df['checked_title'] = df.job_title.apply(
        lambda x: np.nan if occupation not in str(x) else x)
    df2 = df.dropna() 
    return df2

def clean_job_description(df):
    df['checked_description_checked'] = df.job_description.apply(lambda x:
                                                             ''.join(list(filter(lambda ch: ch not in "[]'", x))))
    for i in ["Find Jobs, Company Reviews, Find Salaries, Find Resumes, Employers", "About, Help Centre", r'\n', r'\,', 'Post Job, Upload your resume, Sign in']:
        df.checked_description_checked = df.checked_description_checked.apply(
            lambda x: x.replace(i, ' '))
    df.checked_description_checked = df.checked_description_checked.apply(
        lambda x: np.nan if len(x) < 10 else x)
    df = df.dropna()
    return df