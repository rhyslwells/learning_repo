#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import STOPWORDS
import re

#    - Visualize distributions of key features like salary (`median_salary`), 
# experience level (`formatted_experience_level`), job classifications, etc., to understand their characteristics.
#    - Investigate relationships between features, for example, the relationship between job classification and median salary, or between pay period and maximum salary.


# Load data
df = pd.read_csv('preprocessed_job_postings.csv')


# Experience level
# distribution of formatted_experience_level as bar graph
plt.figure(figsize=(10, 6))
sns.countplot(x='formatted_experience_level', data=df)
plt.title('Count of Jobs by Experience Level')
plt.show()


# Job title
most_common_titles = df['title'].value_counts().head(10)
print("Top 10 most common job titles:\n", most_common_titles)
top_titles_list = most_common_titles.index.tolist()
print("List of Top 10 most common job titles:\n", top_titles_list)

# Additional features


# Posting effectiveness
df['posting_effectiveness'] = df['applies'].apply(lambda x: 'Bad' if x == 0 else ('Okay' if 0 < x < 10 else ('Effective' if x < 100 else 'Too Many')))
print(df['posting_effectiveness'])




#---------------------------------------------------------------


def pull_company_data(company_id):
    # Read employee counts data
    employee_counts = pd.read_csv('company_details/employee_counts.csv')
    employee_counts = employee_counts[employee_counts['company_id'] == company_id]

    # Read company specialties data
    company_specialties = pd.read_csv('company_details/company_specialties.csv')
    company_specialties = company_specialties[company_specialties['company_id'] == company_id]

    # Read company industries data
    company_industries = pd.read_csv('company_details/company_industries.csv')
    company_industries = company_industries[company_industries['company_id'] == company_id]

    # Read companies data
    companies = pd.read_csv('company_details/companies.csv')
    company_info = companies[companies['company_id'] == company_id]

    # Concatenate all dataframes into one
    processed_data = pd.concat([employee_counts, company_specialties, company_industries, company_info], axis=1)

    return processed_data

# Example usage:
# company_id = 12345  # Replace with the desired company ID
# company_data = pull_company_data(company_id)
# print(company_data)


def pull_job_data(job_id):
    #get all the data for a specific job id

    # Read benefits data
    benefits = pd.read_csv('job_details/benefits.csv')
    benefits = benefits[benefits['job_id'] == job_id]

    # Read job industries data
    job_industries = pd.read_csv('job_details/job_industries.csv')
    job_industries = job_industries[job_industries['job_id'] == job_id]

    # Map industry IDs to industry names using industries.csv
    industries = pd.read_csv('maps/industries.csv')
    job_industries = pd.merge(job_industries, industries, on='industry_id', how='left')

    # Read job skills data
    job_skills = pd.read_csv('job_details/job_skills.csv')
    job_skills = job_skills[job_skills['job_id'] == job_id]

    # Map skill abbreviations to skill names using skills.csv
    skills = pd.read_csv('maps/skills.csv')
    job_skills = pd.merge(job_skills, skills, left_on='skill_abr', right_on='skill_abr', how='left')

    # Read salaries data
    salaries = pd.read_csv('job_details/salaries.csv')
    salaries = salaries[salaries['job_id'] == job_id]

    # Concatenate all dataframes into one
    processed_data = pd.concat([benefits, job_industries, job_skills, salaries], axis=1)

    return processed_data


# Example usage:
# job_id = 12345  # Replace with the desired job ID
# job_data = pull_job_data(job_id)
# print(job_data)

# What are all the attributes we have for a job posting?
# we have two dataframes for agiven job posting.