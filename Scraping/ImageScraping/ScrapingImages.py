#!/usr/bin/env python
# coding: utf-8

# In[1]:


baseURL = "https://africanclothingstore.co.uk/"


# In[2]:


# Importing the 'requests' library to handle HTTP requests
import requests

# Importing 'BeautifulSoup' from the 'bs4' library to parse HTML and XML documents
from bs4 import BeautifulSoup


# In[3]:


# Function to get the BeautifulSoup object which contains the web structure and content of a URL
def web_extract(url):
    # Declare variable soup and initialize it to None
    soup = None
    try:
        # Make an HTTP request to the given URL
        response = requests.get(url)
        
        # Check if the HTTP request is successful
        if response.status_code == 200:
            # Parse the HTML content of the response using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            print("Website successfully retrieved")
        # If there is any issue with the HTTP request, print the status code
        else:
            print(f"Fail to retrieve the web page. Status code: {response.status_code}")
    except Exception as e:
        # Handle any exceptions that occur during the HTTP request
        print(f"Error processing the link {url}: {e}")
    
    # Return the BeautifulSoup object
    return soup


# In[4]:


#web_soup = web_extract(baseURL)


# In[5]:


#print(web_soup.prettify())


# In[6]:


import re
def getTagetLink(soup):
    # Compile a regular expression pattern to match URLs starting with the given string
    pattern = re.compile(r'^https://africanclothingstore.co.uk/collections')
    
    # Find all <a> tags in the BeautifulSoup object that have an href attribute matching the pattern
    a_tags = soup.find_all('a', href=pattern)
    
    # Extract the href attribute from each <a> tag and store it in a list
    target_href = [tag.get('href') for tag in a_tags]

    # Return the list of target hrefs
    return target_href


# In[7]:


def filterImgType(src):
    # Initialize fileTypeResult to None, which will store the result if a valid file type is found
    fileTypeResult = None
    
    # Split the source URL by '/', resulting in a list of parts of the URL path
    srcSplit = src.split('/')
    
    # Extract the last part of the URL path, which should be the file name with extension
    fileType = srcSplit[len(srcSplit) - 1]
    
    # Split the file name by '.', resulting in a list where the second element should be the file extension
    filtTypeSplit = fileType.split('.')
    
    # Check if the split resulted in exactly two parts (a name and an extension)
    if len(filtTypeSplit) == 2:
        # If so, set fileTypeResult to the extension part
        fileTypeResult = filtTypeSplit[1]
    
    # Return the result, which will be the file extension if found, or None otherwise
    return fileTypeResult


# In[8]:


def scrapeImagFromWeb(url):
    # Initialize an empty list to store the image source URLs
    imgSrcList = []
    
    # Extract the base HTML content from the given URL using a web extraction function
    baseSoup = web_extract(url)
    
    # Get a list of target links from the base HTML content using a function
    groupHrf = getTagetLink(baseSoup)

    # Iterate over each link in the list of target links
    for link in groupHrf:
        # Extract the HTML content from the current link
        Link_soup = web_extract(link)
        
        # Find all <img> tags in the extracted HTML content
        img_tags = Link_soup.find_all('img')
        
        # Get the 'src' attribute of each <img> tag
        targetImgSrc = [tag.get('src') for tag in img_tags]
        
        # Filter the image sources to include only those with 'jpg' or 'jpeg' file types
        targetImgSrc = [src for src in targetImgSrc if filterImgType(src) in ['jpg', 'jpeg']]
        
        # Extend the main image source list with the filtered image sources
        imgSrcList.extend(targetImgSrc)
    
    # Return the list of image source URLs
    return imgSrcList


# In[10]:


imgSrcList = scrapeImagFromWeb(baseURL)


# In[11]:


# Convert the list of image source URLs to a set to remove any duplicate URLs,
# then convert the set back to a list to maintain the list format.
cleanImgList = list(set(imgSrcList))


# In[12]:


len(cleanImgList)


# In[14]:


cleanImgList


# In[ ]:




