# insight Project: Moocs recomendation system based on job posting.

1. Files in notebook
Coursera_Scraper.ipynb: to scrape all course imformation from Coursera
Indeed_job_post_scraper.ipynb: to scrape 100 job post from indeed.ca with selected job titles
Clean_coursera_dataset.ipynb: to check and dropna the text content scraped from Coursera
Clean_indeed_dataset.ipynb : to check and dropna the text content scraped from indeed.ca
Coursera_preprocessing_data.ipynb : to remove punctuation, tokenize, remove stopwords, and lemmatize the course description 
NER.ipynb : to train the NER model and extract skillset from processed job postings.
Word2Vec and cos similarity.ipynb : to use word embedding and cosine similarity to recommedate the courses beased on job descriptions
Validate NER with testdata.json.ipynb : (to do) to validate the model