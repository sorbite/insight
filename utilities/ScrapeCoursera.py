# Import libraries
import time
import re
from bs4 import BeautifulSoup as soup
import csv
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from urllib.error import HTTPError

# Get the url for coursera with range of pages to be crawled
# Since Coursera can only show 1000 courses, we seperated the urls depends on levels.


class CourseList:
    def __init__(self, list_name='default_course_list'):
        '''
        Get the url for coursera with range of pages to be scraped.
        Since Coursera can only show 1000 courses, we seperated the urls depends on levels.
        '''
        self.list_name = list_name
        self.beginner = [
            'https://www.coursera.org/courses?query=&indices%5Bprod_all_products%5D%5BrefinementList%5D%5Blanguage%5D%5B0%5D=English&indices%5Bprod_all_products%5D%5BrefinementList%5D%5BproductDifficultyLevel%5D%5B0%5D=Beginner&indices%5Bprod_all_products%5D%5BrefinementList%5D%5BentityTypeDescription%5D%5B0%5D=Courses&indices%5Bprod_all_products%5D%5Bpage%5D='
            + str(page) + '&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true'
            for page in range(1, 101, 1)
        ]
        self.mixed = [
            'https://www.coursera.org/courses?query=&indices%5Bprod_all_products%5D%5BrefinementList%5D%5Blanguage%5D%5B0%5D=English&indices%5Bprod_all_products%5D%5BrefinementList%5D%5BproductDifficultyLevel%5D%5B0%5D=Mixed&indices%5Bprod_all_products%5D%5BrefinementList%5D%5BentityTypeDescription%5D%5B0%5D=Courses&indices%5Bprod_all_products%5D%5Bpage%5D='
            + str(page) + '&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true'
            for page in range(1, 92, 1)
        ]
        self.intermediate = [
            'https://www.coursera.org/courses?query=&indices%5Bprod_all_products%5D%5BrefinementList%5D%5Blanguage%5D%5B0%5D=English&indices%5Bprod_all_products%5D%5BrefinementList%5D%5BproductDifficultyLevel%5D%5B0%5D=Intermediate&indices%5Bprod_all_products%5D%5BrefinementList%5D%5BentityTypeDescription%5D%5B0%5D=Courses&indices%5Bprod_all_products%5D%5Bpage%5D='
            + str(page) + '&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true'
            for page in range(1, 64, 1)
        ]
        self.advanced = [
            'https://www.coursera.org/courses?query=&indices%5Bprod_all_products%5D%5BrefinementList%5D%5Blanguage%5D%5B0%5D=English&indices%5Bprod_all_products%5D%5BrefinementList%5D%5BproductDifficultyLevel%5D%5B0%5D=Advanced&indices%5Bprod_all_products%5D%5BrefinementList%5D%5BentityTypeDescription%5D%5B0%5D=Courses&indices%5Bprod_all_products%5D%5Bpage%5D='
            + str(page) + '&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true'
            for page in range(1, 12, 1)
        ]


def get_page_content(url, course=True):
    """
    url - base url to access desired course list page
    """
    try:
        profile = webdriver.FirefoxProfile()
        # 1 - Allow all images
        # 2 - Block all images
        # 3 - Block 3rd party images
        profile.set_preference("permissions.default.image", 2)
        driver = webdriver.Firefox(
            executable_path=r'/home/xinda/insight/notebooks/geckodriver', firefox_profile=profile)
        driver.get(url)
        if course == False:
            time.sleep(2)
        else:
            try:
                wait = WebDriverWait(driver, timeout=2)
                wait.until(expected.presence_of_all_elements_located(
                    (By.CLASS_NAME, 'occupation-name')))
                time.sleep(3)
            except:
                pass
        html = driver.page_source
        page_content = soup(html, 'html.parser')
        driver.close()  # Closed the browser opened in each loop.

        return page_content

    except HTTPError as e:
        print(e)


def get_course_type(course_tag):
    """
    Check course type if it is 'Course'. Only 'Course' is interested in.
    """
    if course_tag.startswith(r"/l"):
        course_type = 'Course'
    elif course_tag.startswith(r"/s"):
        course_type = 'specializations'
    else:
        course_type = 'professional-certificates'
    return course_type


def get_course_job(course_content):
    """
    Get the occupations who are interested in this course.
    """
    course_job = []
    course_job_temp = course_content.find_all(
        'li', {'class': 'occupation-name'})
    for link in course_job_temp:
        course_job.append(link.get_text())
    return course_job


def get_course_skill(course_content):
    """
    Get the skills are expected to acquire in this course.
    """
    course_skill = []
    course_skill_temp = course_content.find_all(
        'span', {'class': 'Pill_56iw91 m-r-1s m-b-1s'})
    for link in course_skill_temp:
        course_skill.append(link.get_text())
    return course_skill


def get_course_description(course_content):
    """
    Self-explained
    """
    course_description = []
    course_description_temp = course_content.find_all(
        'div', {'class': 'content-inner'})
    for link in course_description_temp:
        course_description.append(link.get_text())
    return course_description


def retry_get_job(course_job, course_link, times=3):
    '''
    Since "the occupations who are interested in this course" are often failed to fetch from the website, I retry 3 times for each page.
    '''
    for x in range(0, times):
        if course_job == []:
            course_content = get_page_content(course_link)
            course_job = get_course_job(course_content)
        else:
            break
    return course_job

def scrap_coursera(csvfile='coursera.csv', urls='urls'):
    """
    Scrap all coursera courses.
    Save the result in csvfile.
    """
    with open(csvfile, 'w') as coursera:
        course_writer = csv.writer(coursera, delimiter=',')
        course_writer.writerow([
            'course_type', 'course_title', 'course_rating', 'course_link',
            'course_skill', 'course_job', 'course_description'
        ])  # Generate the header of csvfile.

        # loop through all the pages
        for url in urls:
            list_content = get_page_content(url, course=False)
            # Navigate to list of courses
            # Parse Data
            courses = list_content.find_all('li',
                                            {'class': 'ais-InfiniteHits-item'})
            for course in courses:
                try:
                    course_tag = course.a.get('href')
                    course_type = get_course_type(course_tag)
                    course_title = course.h2.get_text()
                    course_rating = course.find('span', {
                        'class': 'ratings-text'
                    }).get_text()
                    course_link = 'https://www.coursera.org%s' % course_tag
                    # Base course_link to get more course infromation
                    course_content = get_page_content(url=course_link)
                    course_skill = get_course_skill(course_content)
                    course_job = get_course_job(course_content)
                    course_job = retry_get_job(course_job, course_link)
                    print([
                        course_type, course_title, course_rating, course_link,
                        course_skill, course_job
                    ])
                    course_description = get_course_description(
                        course_content)
                    # Write into the file
                    course_writer.writerow([
                        course_type, course_title, course_rating, course_link,
                        course_skill, course_job, course_description
                    ])
                except AttributeError as e:
                    print(e)