import Recommendation as rmd
import pandas as pd


def validate(job_title, df_job_post, df_course, course_num=5):
    '''
    check the accuracy of first 5 recommended courses if the job title of the poster is in the suggested user for the courses
    '''
    related = 0
    irrelated = 0
    df_course2 = df_course[pd.notnull(df_course.checked_job)]
    for job_post in df_job_post.iterrows():
        df_recommed_course = rmd.recommendation(
            job_post, df_course2, course_num)
        df_recommed_course['relevancy'] = df_recommed_course.checked_job.apply(
            lambda x: True if job_title in x else False)
        a = df_recommed_course.relevancy.sum()
        related += a
        irrelated += course_num - a
    accuracy = related / (related + irrelated)
    return accuracy
