# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as soup
import nltk
import pandas as pd
import numpy as np
import re
import string
import utilites as ut

# Create the application object
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home_page():
    return render_template('index.html')  # render a template


@app.route('/output')
def tag_output():
    #
       # Pull input
    url = request.args.get('user_input')

    # Case if empty
    if 0 < len(url) < 20:
        return render_template("index.html",
                               my_output="Unable to get job post. Please make sure it's valid and try again",
                               my_form_result="Empty")
    elif len(url) >= 20:
        r = requests.get(url)
        if r:
            page_content = soup(r.text, 'html.parser')
            job_description = ut.get_job_description(page_content)
            job_description = ut.clean_job_description(job_description)
            extracted_content = str(ut.extract_skillset(job_description))
            nltk.data.path.append('./nltk_data')
            results = ut.recommendation(
                extracted_content=extracted_content, course_num=5)

            return render_template("index.html",
                                   
                                   my_form_result="NotEmpty",
                                   tables=[results.to_html(classes='table table-bordered" id = "a_nice_table',
                                                           index=False, border=0)])
    else:
        fun_results = ut.fun_course(course_num=5)
        return render_template("index.html",
                               
                               my_form_result="Fun",
                               tables=[fun_results.to_html(classes='table table-bordered" id = "a_nice_table',
                                                           index=False, border=0)])


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug =True)  # will run locally http://127.0.0.1:5000/
