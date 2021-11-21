#!/usr/bin/env python
# coding: utf-8

# In[183]:


import gzip
import math
import random
from collections import defaultdict
import copy
import datetime
from matplotlib import pyplot as plt
import numpy as np
import random
from tqdm.notebook import tqdm
import zipfile
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import chi2


# In[2]:


# find files
import os
def list_file_path(root = './',ext = ''):
    for root, dirs, files in os.walk(root):
        for name in files:
            if ext in name:
                print(os.path.abspath(os.path.join(root, name)))
list_file_path(ext='zip')


# In[3]:


list_file_path(root = './project_data')


# In[5]:


#kaggle dataset
path_to_zip_file = "archive.zip"
directory_to_extract_to = "/home/yel004/CSE258/project_data"
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)


# # select dataset and decision on choosing files
# The Kaggle dataset is missing the readme file. By searching the source in Kaggle, I found the original dataset which includs a readme and formatted pdf of the survey. (Link: https://insights.stackoverflow.com/survey). However,Kaggle data has some preprocessing done beforehand. The main different is still with in the question files.

# ## StackOverFlow Original Schema files

# In[6]:


scheme_path = "/home/yel004/CSE258/project_data/survey_results_schema.csv"
schema = pd.read_csv(scheme_path)


# In[7]:


schema.head()


# In[8]:


schema['question'][0]


# ## StackOverFlow Original Response file

# In[9]:


stack_Response_path = "/home/yel004/CSE258/project_data/survey_results_public.csv"
stack_Response = pd.read_csv(stack_Response_path)


# In[10]:


stack_Response.head()


# In[11]:


stack_Response.iloc[0]


# ## Kaggle preprocessed question files

# In[12]:


questions_path ="/home/yel004/CSE258/project_data/survey_results_questions.csv"
questions = pd.read_csv(questions_path)


# In[13]:


questions.head()


# In[14]:


questions['question'][0]


# Kaggle preprocessed responses files

# In[15]:


kag_response_path = '/home/yel004/CSE258/project_data/survey_results_responses.csv'
kag_response = pd.read_csv(kag_response_path)


# In[16]:


kag_response.head()


# In[17]:


kag_response.iloc[0]


# ### Zero users without NA.  A smart way of handling missing values must be decided 

# In[18]:


len(kag_response)


# In[19]:


kag_response_naRem = kag_response.dropna()


# In[20]:


len(kag_response_naRem)


# In[21]:


kag_response.columns


# # TODO:
# 1. Formulate recommending system question
# 2. Many features are categorical; how to use them?

# In[116]:


def get_plot(dataframe,col_name:str,plot_type:str = 'bar',fig_size = (10,10),Table  =True):
    '''
    returb plot given a panda dataframe or series and plot type
    when categories are too many to plot and Table = True, table are show instead
    '''
    assert isinstance(dataframe,pd.core.frame.DataFrame) or isinstance(dataframe,pd.core.series.Series)
    assert isinstance(col_name,str)
    assert isinstance(plot_type,str)
    assert isinstance(fig_size,tuple)
    assert all([isinstance(size,int)or isinstance(size,float) for size in fig_size])
    count = dataframe[[col_name]].value_counts()
    total_count = count.sum()
    percent = count.apply(lambda x: x/total_count)
    table_df = pd.DataFrame({'Counts':count,'Density':percent})
    if len(dataframe[col_name].unique()) > 10 and Table:
        print("**************Too Many Categories To Plot********* ")
        print("***Showing Tables")
        print(table_df)
        print("**************End of Table")
    else:
        dataframe[[col_name]].apply(pd.value_counts).plot(kind = plot_type,subplots =True,figsize =fig_size,title =col_name)
    return table_df
    


# In[118]:


_ = get_plot(kag_response,'Country','pie',fig_size = (9,7))


# In[193]:


_ = get_plot(kag_response,'MainBranch','pie',fig_size = (9,7))


# In[194]:


_ = get_plot(kag_response,'EdLevel','bar',fig_size = (9,7))


# In[98]:


# remove survey related questions
names = ['MainBranch', 'Employment', 'Country', 
       'EdLevel', 'Age1stCode', 'LearnCode', 'YearsCode', 'YearsCodePro',
       'DevType', 'OrgSize', 'Currency', 'CompTotal', 'CompFreq',
       'LanguageHaveWorkedWith', 'LanguageWantToWorkWith',
       'DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith',
       'PlatformHaveWorkedWith', 'PlatformWantToWorkWith',
       'WebframeHaveWorkedWith', 'WebframeWantToWorkWith',
       'MiscTechHaveWorkedWith', 'MiscTechWantToWorkWith',
       'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith',
       'OperatingSystem','Age', 'Gender', 'Trans',
       'Sexuality', 'Ethnicity', 'Accessibility', 'MentalHealth','ConvertedCompYearly']


# In[119]:


for name in names:
    get_plot(kag_response,name,'pie',fig_size = (9,7))


# In[123]:


# null values
NA_counts = kag_response.isna().sum()


# In[135]:


# we can select target from these categories
NA_counts.sort_values()[1:15]


# In[184]:


# Pick Employment as the targetting label for now -> whether the person is full-time employed
# As many data are categorical we can perform chi-squre test to check the correlation
def chi_square(dataframe,col_name ,indpendent_prob = 0.95):
    '''
    prepare contingency_table for chi-square test
    default label: Full-time employment , Part-time or Unemployed
    '''
    assert isinstance(dataframe,pd.core.frame.DataFrame)
    assert col_name in dataframe.columns
    assert 'label' in dataframe.columns
    ct = pd.crosstab(index = kag_response['label'],columns = kag_response[col_name])
    stat, p, dof, expected = chi2_contingency(ct)
    # interpret test-statistic
    prob = indpendent_prob
    critical = chi2.ppf(prob, dof)
    alpha = 1.0 - prob
    print(f'Selected Feature: {col_name}')
    print('significance=%.3f, p=%.3f' % (alpha, p))
    if p <= alpha:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')
    return p


# In[164]:


kag_response['label'] = kag_response['Employment'].apply(lambda x: x == 'Employed full-time')


# In[189]:


pvalPerFeature = []
for name in kag_response.columns:
    if name not in ['label','Employment']:
        p =chi_square(kag_response,name)
        pvalPerFeature.append((p,name))


# In[192]:


# smaller the p value, likely the feature is relevent
# somehow only 'UK_Country' and 'Responseid' can be removed at this stage
sorted(pvalPerFeature)


# In[ ]:




