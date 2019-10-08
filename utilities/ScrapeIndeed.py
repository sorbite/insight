# inport libraries
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


class JobList:
    def __init__(self, list_name='default_job_list', job_list=['Graphic Designers', 'Data Scientist', 'Security Engineer', 'Pharmacist', 'Marketing Specialist', 'Business Analyst', 'Accountant', 'Customer Care Rep', 'Biologist', 'Librarian', 'Entrepreneur', 'Teacher', 'Photographer']):
        self.list_name = list_name
        self.job_list = job_list


def get_job_urls(job_title, page_number):
    """
    Get the urls of each job posters on the page.
    """
    job_title.replace(' ', '+')
    url_gta = []  # url for Toronto job posing
    for page in range(0, 10):
        url_page = r'https://ca.indeed.com/jobs?q=' + job_title + \
            r'&l=Greater+Toronto+Area,+ON&start=' + str(page*10)
        url_gta.append(url_page)
    return url_gta


def get_page_content(url, job_list=True):
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
        if job_list == True:
            time.sleep(2)
        else:
            try:
                wait = WebDriverWait(driver, timeout=2)
                wait.until(expected.presence_of_all_elements_located(
                    (By.TAG_NAME, 'a')))
                time.sleep(randint(1, 3))
            except:
                pass
        html = driver.page_source
        page_content = soup(html, 'html.parser')
        driver.close()  # Closed the browser opened in each loop.
        return page_content
    except HTTPError as e:
        print(e)


def get_job_description(job_content):
    """
    Get the detailed description from job posters.
    """
    job_description = []
    job_description_temp = job_content.find_all(
        'li')
    for link in job_description_temp:
        job_description.append(link.get_text())
    return job_description


def scrap_indeed(csvfile='indeed.csv', urls='url_gta'):
    root_url = 'https://ca.indeed.com/'
    """
    Scrape indeed job postings.
    Save the result in csvfile.
    """
    with open(csvfile, 'w') as indeed:
        indeed_writer = csv.writer(indeed, delimiter=',')
        indeed_writer.writerow([
            'job_title', 'job_description'
        ])  # Generate the header of csvfile.

        # loop through all the pages
        for url in urls:
            list_content = get_page_content(url, job_list=True)
            # Navigate to list of job postings
            # Parse Data
            jobs = list_content.find_all('div', {'class': 'title'})[
                3:]  # First three are ads
            for job in jobs:
                try:
                    job_href = job.a.get('href')
                    job_title = job.a.get('title')
                    job_link = root_url+job_href
                    # Base job_link to get job description
                    job_content = get_page_content(
                        url=job_link, job_list=False)
                    job_description = get_job_description(job_content)
                    print([
                        job_title, job_description
                    ])
                    # Write into the file
                    indeed_writer.writerow([
                        job_title, job_description
                    ])
                except AttributeError as e:
                    print(e)
