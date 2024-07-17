#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import request and BeautifulSoupLibrary
import requests
from bs4 import BeautifulSoup


# In[2]:


# Function to get a BeautifulSoup object containing the web structure
# and content of a URL
# Parameter: URL of the page we want to explore
# Return: BeautifulSoup object representing the page structure
def web_extract(url):
    # Make an HTTP request to the specified URL
    response = requests.get(url)

    # Declare a variable to hold the BeautifulSoup object
    soup = None

    # Check if the HTTP request was successful (status code 200)
    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Website successfully retrieved")
    # Handle the case where the HTTP request failed
    else:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")

    # Return the BeautifulSoup object (or None if the request failed)
    return soup


# In[3]:


#The base URL: first page of the Innovate UK
baseURL = 'https://iuk.ktn-uk.org/projects/?_sft_programme=investor-partnerships-future-economy'


# In[4]:


# Define the target class attributes to filter <a> tags
# This allows us to get the <a> tags that contain the href (link) 
# to each investor's description page on the Innovate UK website
targetClass = ['group', 'border-2', 'border-primary', 'flex', 'flex-col']


# In[5]:


def getDescriptionPageLink(soup, targetClass):
    """
    Function to get the links to the description pages 
    from the BeautifulSoup object of a given URL.

    Parameters:
    soup (BeautifulSoup): BeautifulSoup object containing the web structure and content.
    targetClass (list): List of class attributes to target specific <a> tags.

    Returns:
    list: List of links to all investor pages from the BeautifulSoup object.
    """
    # Find all <a> tags with the specified class attributes
    target_a_tags = [tag for tag in soup.find_all('a')
                     if 'class' in tag.attrs and tag.attrs['class'] == targetClass]

    # Extract the 'href' attribute from each target <a> tag
    hrefList = [tag.get('href') for tag in target_a_tags]

    return hrefList


# In[6]:


def getNextPage(soup):
    """
    Retrieves the URL of the next page from the BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): BeautifulSoup object representing the current page.

    Returns:
    str or None: URL of the next page if found, otherwise None.
    """
    next_atag = soup.find(lambda tag: tag.name == 'a' and tag.text == 'Next >')
    
    if next_atag:
        return next_atag.get('href')
    else:
        return None


# In[ ]:


def get_all_investorsLinkDescPagRecursively(URL, pageNum, target_class_, invList):
    """
    Recursively navigates through pages to extract links to investor description pages 
    from Innovate UK website.

    Parameters:
    URL (str): URL of the current page.
    pageNum (int): Current page number being processed.
    target_class_ (list): List of classes to filter <a> tags.
    invList (list): List of investor description page links collected so far.

    Returns:
    list: List of all investor description page links from all pages.
    """
    currentList = invList.copy()
    print(f"Page {pageNum}: ", end ='')
    soup = web_extract(URL)
    currentList.extend(getDescriptionPageLink(soup, target_class_))

    nextURL = getNextPage(soup)
    if nextURL:
        pageNum += 1
        return get_all_investorsLinkDescPagRecursively(nextURL, pageNum, target_class_, currentList)
    else:
        return currentList


# In[ ]:


# Compile a list of links to investor description pages on the Innovate UK website
compiledList = get_all_investorsLinkDescPagRecursively(baseURL, 1, targetClass, [])


# In[ ]:


#Iterate through the compiled list and view each link
for link in compiledList:
    print(link)

