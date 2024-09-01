#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import necessary libraries
import pandas as pd
from scipy import stats


# In[2]:


# Assign GitHub link to data source variable
# Ensure to change 'blob' in the link to 'raw'
gitRepo = 'https://github.com/colabLearn/PandasDFrameVideoScripts/raw/main/testData/Student_performance_data.csv'


# In[3]:


# Extract student data from the CSV file using the PyArrow engine for efficient datatype handling
studentData = pd.read_csv(gitRepo, dtype_backend="pyarrow", engine="pyarrow")


# In[4]:


# View the first few rows of student data to understand its structure
print(studentData.head())


# In[5]:


# Extract the 'GPA' column into a Pandas Series
studentGPA = studentData['GPA']


# In[6]:


# View the GPA Series to check its contents
print(studentGPA.head())


# In[7]:


# Calculate the 25th and 75th percentiles of the GPA data
gpa_25 = studentGPA.quantile(0.25)  # 25th percentile (lower quartile)
gpa_75 = studentGPA.quantile(0.75)  # 75th percentile (upper quartile)


# In[8]:


# Create a mask for students whose GPA is below the 25th percentile
mask_gpa_below_25 = studentGPA.lt(gpa_25)


# In[9]:


# View the mask to see which students fall below the 25th percentile
print(mask_gpa_below_25.head())


# In[10]:


# Create a mask for students whose GPA is above the 75th percentile
mask_gpa_above_75 = studentGPA.gt(gpa_75)


# In[11]:


# View the mask to see which students score above the 75th percentile
print(mask_gpa_above_75.head())


# In[12]:


# Function to evaluate if there is a significant difference between two related datasets
def significant_diff(series1, series2):
    t_stat, p_value = stats.ttest_rel(series1, series2)
    result = {"T-Statistic": t_stat, "P-Value": p_value}
    
    # Interpret the result based on the significance level (alpha)
    alpha = 0.05
    if p_value < alpha:
        result['interpret'] = "The difference is statistically significant."
    else:
        result['interpret'] = "The difference is not statistically significant."
    
    return pd.Series(result)


# In[13]:


# List of column headers of interest
headers_ = ['Age', 'Gender', 'Ethnicity', 'ParentalEducation',
            'StudyTimeWeekly', 'Absences', 'Tutoring',
            'ParentalSupport', 'Extracurricular', 'Sports',
            'Music', 'Volunteering']


# In[14]:


#Column the are categorical
catData = ['Gender', 'Ethnicity', 'ParentalEducation','Tutoring',
            'ParentalSupport', 'Extracurricular', 'Sports',
            'Music', 'Volunteering']


# In[15]:


def get_column_series(data, col_header):
    if col_header in catData:
        return data[col_header].astype('category')
    else:
        return data[col_header]


# In[16]:


# Function to extract two Series for each column:
# 1. For students below the 25th percentile
# 2. For students above the 75th percentile
def extract_low_high_scorers(series_dict, high_score_mask, low_score_mask):
    high_low_scorer_dict = {}
    for col_name, series in series_dict.items():
        high_low_tuple = (series[high_score_mask], series[low_score_mask])
        high_low_scorer_dict[col_name] = high_low_tuple
    return high_low_scorer_dict


# In[17]:


# Function to assess significant differences in student variables
# between students who score below the 25th percentile and those who score above the 75th percentile
def assess_significant_diff(dataframe, header_list, high_score_mask, low_score_mask):
    result_dict = {}
    series_dict =get_column_series(dataframe, header_list)
    high_low_scorer_dict = extract_low_high_scorers(series_dict, high_score_mask, low_score_mask)
    
    for col_name, high_low_tuple in high_low_scorer_dict.items():
        sig_diff_result = significant_diff(high_low_tuple[0], high_low_tuple[1])
        result_dict[col_name] = sig_diff_result
    
    return result_dict


# In[18]:


# Get significant difference results for the student variables
result = assess_significant_diff(studentData, headers_, mask_gpa_above_75, mask_gpa_below_25)


# In[19]:


# Print results
print("Below 25% GPA Percentile Versus Above 75% Percentile GPA")
print("===============================================================")
for col in headers_:
    print(f"================= Students Variable: {col} ==========================")
    print(result[col])


# In[20]:


# List variables that show a significant difference
print("\nVariables with significant differences:")
print("-----------------------------------------")
for col in headers_:
    if result[col]['P-Value'] < 0.05:
        print(col)


# In[ ]:




