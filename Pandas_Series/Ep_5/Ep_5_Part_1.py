#!/usr/bin/env python
# coding: utf-8

# Link to assignment from episode 4:
# - .ipynb https://github.com/colabLearn/PandasDFrameVideoScripts/blob/8402456a32334b49f69829f3c23cd87bee72ab2f/Pandas_Series/Ep_5/Pre_/Ep4_Assign_.ipynb
# - .py
# https://github.com/colabLearn/PandasDFrameVideoScripts/blob/8402456a32334b49f69829f3c23cd87bee72ab2f/Pandas_Series/Ep_5/Pre_/Ep4_Assign_.py

# In[1]:


import pandas as pd


# In[2]:


# Assign GitHub link to data source variable
# Ensure to change 'blob' in the link to 'raw'
gitRepo ='https://github.com/colabLearn/PandasDFrameVideoScripts/raw/8402456a32334b49f69829f3c23cd87bee72ab2f/testData/global_air_quality_data_10000.csv'


# In[3]:


# Extract student data from the CSV file using the PyArrow engine for efficient datatype handling
global_air_quality = pd.read_csv(gitRepo, dtype_backend="pyarrow", engine="pyarrow")


# In[4]:


print(global_air_quality.head())


# In[5]:


cities = global_air_quality.City


# In[6]:


cities


# .apply() 

# In[7]:


interested_in = ['London','New York', 'Johannesburg', 'Cairo']


# In[8]:


def extract_city(val):
    if val in interested_in:
        return val
    else:
        return 'others'


# In[9]:


get_ipython().run_cell_magic('timeit', '', 'cities.apply(extract_city)\n')


# In[10]:


get_ipython().run_cell_magic('timeit', '', "cities.where(cities.isin(interested_in), 'others')\n")


# In[11]:


from IPython.display import Image
Image(filename='Pre_//images//apply_.jpg')


# In[12]:


Image(filename='Pre_//images//where_.jpg')


# In[13]:


cities.mask(~cities.isin(interested_in), 'others')


# In[14]:


first_choices = ['London','New York', 'Johannesburg', 'Cairo']
second_choices = ['Toronto', 'Los Angeles', 'Tokyo', 'Beijing']


# In[15]:


def extract_city_2(val):
    if val in first_choices:
        return val
    elif val in second_choices:
        return "Second Priority"
    else:
        return 'others'


# In[16]:


cities.apply(extract_city_2)


# In[17]:


get_ipython().run_cell_magic('timeit', '', "(cities.case_when(\n    caselist = [\n        (cities.isin(second_choices), 'Second Priority'),\n        (~cities.isin(first_choices), 'other'),\n    ]\n)\n)\n")


# ### Missing Data

# In[18]:


print(global_air_quality.head())


# In[19]:


re_global_air_quality = global_air_quality.pivot_table(index = 'Date',
                                                       columns='City',
                                                       values = 'NO2',
                                                       aggfunc='mean'
                                                      )                                                    


# In[20]:


re_global_air_quality


# In[21]:


re_global_air_quality['New York'].isna().sum()


# In[22]:


testData1 = re_global_air_quality['New York'].fillna(1)


# In[23]:


testData1.isna().sum()


# In[24]:


testData2 =re_global_air_quality['New York'].dropna()


# In[25]:


testData2.size


# In[26]:


re_global_air_quality['New York'].size


# In[27]:


testData4 = pd.Series([23,21,19,None,None, 27, 29])


# In[28]:


testData4.ffill()


# In[29]:


re_global_air_quality['New York'].ffill().isna().sum()


# In[30]:


re_global_air_quality['New York'].interpolate()


# In this session, we explored several key functions that help with data manipulation and analysis in Series. So far, we have covered the following:
# 
# - The .apply() function
# - The .where() function
# - The .mask() function
# - The .case_when() function
# - Additionally, we looked at handling missing data using these methods:
# - Getting an overview of missing data with .isna().sum()
# - Filling missing values with .fillna(value)
# - Dropping missing data with .dropna()
# - Interpolating missing data with .interpolate()

# In[ ]:




