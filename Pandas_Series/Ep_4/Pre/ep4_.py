#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


#https://github.com/colabLearn/PandasDFrameVideoScripts/blob/main/testData/Student_performance_data.csv
gitRepo = "https://github.com/colabLearn/PandasDFrameVideoScripts/raw/main/testData/Student_performance_data.csv"


# In[3]:


studentData = pd.read_csv(gitRepo, dtype_backend="pyarrow", engine="pyarrow")


# In[4]:


studentData


# In[5]:


#One thing we may want to look at regarding the ]
#overall performance of the students is the mean GPA
# Let's extract the studentGPA from the dataframe
#into a Series
studentGPA = studentData['GPA']


# ### Single aggregation methods

# In[6]:


#we can compute the mean GPA
#using this aggregation method of the series
studentGPA.mean()

This value represents the central point in the students 
GPA score. It provides an indication of the typical score
among the studentGPA data. 
# However, mean can be sensitive to outliers
# for example if you have this kind of data
# [22,24,26,31,99]

# In[7]:


testData = pd.Series([22,24,26,31,99])


# In[8]:


testData.mean()


# In[9]:


#This value does not truly 
#represent typical value of
#data in this data set


# In[10]:


#In this case median could be 
#a better measure to indicate
#typical values in the data
testData.median()

it indicates that the data is likely symmetrically distributed 
with minimal skewness. 
This often suggests that the dataset does not have extreme outliers 
or is not heavily skewed to one side, making the mean a reliable measure 
of central tendency. In such cases, the data tends to cluster around a 
central value, and both the mean and median effectively represent the "center" 
of the distribution.A useful statistical measure to assess the asymmetry of your data distribution 
and to identify potential outliers is the skew() function. This function helps 
determine whether your data is skewed toward higher or lower values.This is also an aggregation method; however, the PyArrow data type does not support 
the skew() function. To apply this method, we need to convert the data to the native 
Pandas 'double' type, which is equivalent to float64.
# In[11]:


#skew()
studentGPA.astype('double').skew()


# - 0: Perfectly symmetric distribution.
# - Positive value: Right-skewed (long tail on the right side).
# - Negative value: Left-skewed (long tail on the left side).
# In practical terms:
# - Skewness between -0.5 and 0.5: Indicates a fairly symmetric distribution.
# - Skewness between -1 and -0.5 or 0.5 and 1: Indicates moderate skewness.
# - Skewness less than -1 or greater than 1: Indicates significant skewness.
Given that your skewness is 0.0145, it suggests that the distribution of 
of the students' GPT is almost perfectly symmetric, with negligible skew. 
This is typically considered a good indicator of normality in the dataset
# In[12]:


print(studentGPA.mean(), studentGPA.median())


# In[13]:


#Mean and median will be very close if data is symmetrical


# In[14]:


#There are many other aggregation methods like this that we call on a series object
#Such as:
studentGPA.min() #Minmum value in the data


# In[15]:


studentGPA.max()


# In[16]:


studentGPA.var()


# In[17]:


studentGPA.std()


# #### Mention the .agg()

# Another useful method if the .agg method
# - obviously from its name it aggregates data, like quantile,
# - it transform data depending on the argument you use to call the method
# - you can call .agg method to computer the mean of data like this:

# In[18]:


studentGPA.agg('mean')


# but of course the studentGPA.mean() method is suffice 
# to compute mean. Where .agg method provide a better use
# is in this example:

# ##### Key Advantages of Using .agg():
# - Combine Multiple Aggregation Functions: .agg() allows you to apply multiple aggregation functions (e.g., mean, sum, min, max) simultaneously on a Series or DataFrame, enabling comprehensive summary statistics in a single step.
# - Custom Aggregation Functions: You can pass user-defined functions to .agg(), allowing for customized aggregation logic beyond the built-in methods.

# In[19]:


studentGPA.agg(['mean', 'var', 'max', 'min'])


# In[20]:


#Let's assume we make the pass GPA =1.5
#So that all students with GPT>=1.5 pass, otherwise fail
studentGPA.ge(1.5)

The output is a boolean series with True or False values. 
To get the number of students who passed, you can use the sum() 
function on the boolean series. This will return the count of 
indices where the value is True.
# In[21]:


studentGPA.ge(1.5).sum()


# In[22]:


def no_student_score_gt_mean_gpa(s):
    return s.gt(1.5).sum()


# In[23]:


studentGPA.agg(['mean', 'var', 'max', 'min', no_student_score_gt_mean_gpa])


# In[24]:


#An approach to get the % of these student that pass
(studentGPA.ge(1.5).sum()/studentGPA.count())*100

There is trick we can use with this, applying the native pandas boolean data type 
which sees True as 1 and  False as 0. 
Although this is not currently supported by bool[pyarrow]
We can exploit this trick using pandas bool datatype
# In[25]:


studentGPA.describe()


# In[26]:


studentGPA.quantile()

The default is the 50th percentile, meaning that 50% of students in the dataset 
have a GPA below 1.890, while the other 50% have a GPA above this value.
# In[27]:


studentGPA.quantile(0.25)


# In[28]:


studentGPA.quantile(0.75)


# In[29]:


studentGPA.quantile([0.25, 0.5, 0.75])


# In[30]:


studentGPA.is_unique


# In[31]:


studentID = studentData['StudentID']


# In[32]:


studentID.is_unique

Let’s consider a second example with an illustration. Suppose we want to 
check if our dataset is in increasing order, meaning each data point is 
greater than or equal to the one before it, like in this set: 
[1, 2, 3, 3, 4, 6, 7, 7, 9].
# In[33]:


#testSeries = pd.Series([1, 2, 3, 3, 4, 6, 7, 7, 9])  #-->This first
testSeries = pd.Series([1, 2, 3, 3, 5, 4, 6, 7, 7, 9])
#testSeries = pd.Series([ ])


# In[34]:


#We may want to write a function like this;
def is_increasing(in_series):
    for i in range(len(in_series)-1):
        if(in_series[i]>in_series[i+1]):
            return False
    return True   


# In[35]:


len(testSeries)

This looks like a good one, but what about applying this 
property of the pandas seriesAnother interesting method is the .quantile method. 
This method returns values that offer insights into the 
distribution of a dataset by dividing it into equal-sized 
intervals. 
Specifically, quantiles help you understand how data points 
are spread across the range of values.
# In[36]:


#If we call the quatile method without any arugment 
#Like this --> the output is the 50% quantile
#That is, the median of our dataset
studentGPA.quantile()


# This output indicates that:
# - 50% of the students score below 1.89GPA
# - And, 50% score above it
We can specify another quantile level such:
# In[37]:


#25% quantile
studentGPA.quantile(0.25)

Alternatively, you can pass a list of levels, such as 25%, 50%, and 75% quantiles. 
In this case, the output will not be a single value but a series, with the specified 
quantiles as the keys.
# In[38]:


studentGPA.quantile([.25,.5, .75])


# This output indicate that:
# - 25% of the students score below: 1.17
# - 50% score below 1.89
# - 75% score below 2.62 GPA

# - 90% of the students score below:3.13 GPA

# In[39]:


#You can as well specify other levels of quantiles such as:
studentGPA.quantile(0.9)


# In[40]:


#bool[pyarrow] datatype will not support this
studentGPA.ge(1.5).astype('bool').mul(100).mean()


# In[41]:


percentile_25_mask = studentGPA.lt(studentGPA.quantile(0.25))


# In[42]:


percentile_75_mask = studentGPA.gt(studentGPA.quantile(0.75))


# In[43]:


studyTime_25 = studentData['StudyTimeWeekly'][percentile_25_mask]
studyTime_75 = studentData['StudyTimeWeekly'][percentile_75_mask]


# In[44]:


studyTime_25


# In[45]:


studyTime_75


# This kind of looks neater 

# In[46]:


from scipy import stats
t_stat, p_value = stats.ttest_rel(studyTime_25,studyTime_75)
print("T-Statistic: ", t_stat)
print("P-Value: ", p_value)

#Interprt the result
alpha  = 0.05
if p_value < alpha:
    print("The difference is statistically significant.")
else:
    print("The difference is not statistically significant.")

- T-Statistic: -7.83: This value represents the difference between the means of the two 
groups relative to the variation in the data. A large absolute value (like this one) 
suggests a significant difference between the groups.

- P-Value: 1.336e-14: The p-value is extremely small, much smaller than a typical significance 
threshold (e.g., 0.05). This suggests that the observed difference between the groups is highly 
unlikely to have occurred by chance.- Interpretation:
Given these results:
- The negative t-statistic suggests that the mean of the first group is lower than that of the second group.
- The extremely small p-value (close to zero) indicates strong evidence against the null hypothesis, meaning 
the difference between the two groups is statistically significant.
- In summary, the data suggests there is a highly significant difference between the two groups you're comparing.
# In[47]:


print(is_increasing(testSeries))


# In[48]:


testSeries.is_monotonic_increasing


# In[49]:


def significant_diff(series1, series2):
    t_stat, p_value = stats.ttest_rel(series1, series2)
    result = {"T-Statistic":t_stat, "P-Value":p_value}
    
    #Interprt the result
    alpha  = 0.05
    if p_value < alpha:
        result['interpret']="The difference is statistically significant."
    else:
        result['interpret'] = "The difference is not statistically significant."  

    return pd.Series(result)


# In[50]:


significant_diff(studyTime_25, studyTime_75)


# In[51]:


#We have 49.62% of the student that study more thatn 9.77hours per week


# In[52]:


studentGPA.describe()


# Common Aggregation Functions:
# - 'mean': Mean of the values.
# - 'sum': Sum of the values.
# - 'min': Minimum value.
# - 'max': Maximum value.
# - 'median': Median value.
# - 'var': Variance.
# - 'std': Standard deviation.
# - 'count': Count of non-null values.
# - 'prod': Product of the values.
# - 'first': First value.
# - 'last': Last value.

# Statistical Aggregations:
# - series.mean(): Returns the average (mean) of the values in the Series.
# - series.sum(): Computes the sum of all values in the Series.
# - series.min(): Returns the smallest value in the Series.
# - series.max(): Returns the largest value in the Series.
# - series.median(): Calculates the median (middle value) of the Series.
# - series.var():  Computes the variance of the values, which measures the spread of the values around the mean.
# - series.std(): Calculates the standard deviation, which is the square root of the variance.
# - series.prod(): Returns the product of all values in the Series.
# - series.cumsum(): Computes the cumulative sum of the values in the Series.
# - series.cumprod(): Computes the cumulative product of the values in the Series.
# Count and Frequency:
# - series.count(): Counts the number of non-NA/null entries in the Series.
# - series.value_counts(): Description: Returns a Series with counts of unique values.
# - series.nunique(): Description: Returns the number of unique values in the Series.
# Aggregation with agg():
# - series.agg(): Allows applying multiple aggregation functions to the Series at once. The output depends on the functions used (e.g., ['mean', 'sum']).
# Custom Aggregations:
# - Custom functions passed to agg():  You can pass custom functions to perform specific aggregations. The output varies based on the custom function provided. For example, lambda x: x.sum() / len(x) calculates the mean.
# 

# ### Properties for Series
# Descriptive Statistics:
# - series. describe(): Provides a summary of statistics including count, mean, standard deviation, min, 25th percentile, median (50th percentile), 75th percentile, and max.
# - series.is_unique: Checks if all values in the Series are unique. Output is a boolean (True or False).
# - series.is_monotonic:Checks if the Series is either monotonically increasing or decreasing. Output is a boolean (True or False).
# - series.is_monotonic_increasing: Checks if the Series is monotonically increasing. Output is  boolean (True or False).
# - series.is_monotonic_decreasing: Checks if the Series is monotonically decreasing. Output is boolean (True or False).
# 
# Duplicates and Unique Values:
# - series.duplicated(): Returns a boolean Series indicating whether each value is a duplicate of an earlier value.
# - series.unique(): Returns an array of unique values.
# - series.drop_duplicates(): Returns a Series with duplicate values removed. The output maintains the original order of the first occurrence.
# Additional Properties:
# - series.first(): (For GroupBy objects, not directly for Series) Returns the first value in each group.
# 

# In[ ]:




