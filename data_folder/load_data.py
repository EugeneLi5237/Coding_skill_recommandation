#!/usr/bin/env python
# coding: utf-8

# In[15]:


def get_data(filename=  'data_pos_neg_neu.txt'):
    '''
    read the list of dict for postive,negative,neutral feedback
    '''
    data = []
    with open(filename) as f:
        for i, line in enumerate(f):
            try:
                d = eval(line)
            except:
                print("*****Error*****")
                print(i,line)
                print("*********END of ERROR *******")
                break
            else:
                data.append(d)
    return data


# In[17]:


def transform_data(data,four_deg = True):
    '''
    read in the postive, negative,neutral data
    perform one of the following transformation
        if four_deg:
          4 degree "one-hot encoding" (0:missing,1:Neutral, 5:positive,-5 negative)
        else:
          user-product interact 
    '''
    transformed = []
    with open('product_id_map.txt', 'r', encoding='utf-8') as map_file:
        product_id_map = eval(map_file.readline())
    for i,sample in enumerate(data):
        user_id = i+1
        if four_deg:
            product_feedback = [0] * len(product_id_map)
            # pos : 5 ,neg: -5, neutral: 1 missing 0
            for p in sample['pos']:
                product_feedback[product_id_map[p]] = 5
            for neg in sample['neg']:
                product_feedback[product_id_map[neg]] = -5
            for neu in sample['neu']:
                product_feedback[product_id_map[neg]] = 1
            transformed.append([user_id]+product_feedback)
        else:
            for p in sample['pos']:
                transformed.append([user_id,product_id_map[p],5])
            for neg in sample['neg']:
                transformed.append([user_id,product_id_map[neg],-5])
            for neu in sample['neu']:
                transformed.append([user_id,product_id_map[neu],1])
    return transformed


# In[32]:


def load_transformed(file_path = 'transformed_user_product_interaction.txt'):
    transformed = []
    with open(file_path,'r') as inf:
        for line in inf:
            transformed.append(eval(line))
    return transformed

