#!/usr/bin/env python
# coding: utf-8

# In[15]:


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


# In[17]:


# find files
import os
def list_file_path(root = './',ext = ''):
    for root, dirs, files in os.walk(root):
        for name in files:
            if ext in name:
                print(os.path.abspath(os.path.join(root, name)))
list_file_path(ext='zip')


# In[29]:


list_file_path(root = './project_data')


# In[28]:


#kaggle dataset
path_to_zip_file = "archive.zip"
directory_to_extract_to = "/home/yel004/CSE258/project_data"
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)


# # select dataset and decision on choosing files
# The Kaggle dataset is missing the readme file. By searching the source in Kaggle, I found the original dataset which includs a readme and formatted pdf of the survey. (Link: https://insights.stackoverflow.com/survey). However,Kaggle data has some preprocessing done beforehand. The main different is still with in the question files.

# ## StackOverFlow Original Schema files

# In[19]:


scheme_path = "/home/yel004/CSE258/project_data/survey_results_schema.csv"
schema = pd.read_csv(scheme_path)


# In[24]:


schema.head()


# In[27]:


schema['question'][0]


# ## StackOverFlow Original Response file

# In[33]:


stack_Response_path = "/home/yel004/CSE258/project_data/survey_results_public.csv"
stack_Response = pd.read_csv(stack_Response_path)


# In[34]:


stack_Response.head()


# In[35]:


stack_Response.iloc[0]


# ## Kaggle preprocessed question files

# In[30]:


questions_path ="/home/yel004/CSE258/project_data/survey_results_questions.csv"
questions = pd.read_csv(questions_path)


# In[31]:


questions.head()


# In[32]:


questions['question'][0]


# Kaggle preprocessed responses files

# In[36]:


kag_response_path = '/home/yel004/CSE258/project_data/survey_results_responses.csv'
kag_response = pd.read_csv(kag_response_path)


# In[37]:


kag_response.head()


# In[38]:


kag_response.iloc[0]


# ### Zero users without NA.  A smart way of handling missing values must be decided 

# In[39]:


len(kag_response)


# In[40]:


kag_response_naRem = kag_response.dropna()


# In[41]:


len(kag_response_naRem)


# In[45]:


kag_response.columns


# # TODO:
# 1. Formulate recommending system question
# 2. Many features are categorical; how to use them?

# In[ ]:




