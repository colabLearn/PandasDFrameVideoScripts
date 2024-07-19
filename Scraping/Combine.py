#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing the 'requests' library to handle HTTP requests
import requests

# Importing 'BeautifulSoup' from the 'bs4' library to parse HTML and XML documents
from bs4 import BeautifulSoup


# In[2]:


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


# In[3]:


# Assign the URL of the base page of 
#->Innovate UK's Investor Partnerships Future Economy 
#-->projects to the variable baseURL
baseURL = 'https://iuk.ktn-uk.org/projects/?_sft_programme=investor-partnerships-future-economy'


# In[4]:


#Class attribute to help extract each of the investors description page link
targetClass =  ['group', 'border-2', 'border-primary', 'flex', 'flex-col']


# In[5]:


def getDescriptionPageLink(soup, targetClass):
    """
    Extracts links to description pages from a BeautifulSoup object.
    
    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML of the webpage.
    targetClass (list): The class attribute to filter the target <a> tags.

    Returns:
    list: A list of links to the description pages.
    """
    
    # Find all <a> tags with the specified class attribute
    target_a_tag = [tag for tag in soup.find_all('a')
                    if 'class' in tag.attrs
                    and tag.attrs['class'] == targetClass]

    # Extract the href attribute (link) from each <a> tag
    hrefList = [tag.get('href') for tag in target_a_tag]

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


# In[7]:


def get_all_investorsLinkDescPagRecursively(URL, pageNum, target_class_, invList):
    """
    Recursively navigates through pages to collect links to investor description pages.
    
    Parameters:
    URL (str): The URL of the current page.
    pageNum (int): The current page number.
    target_class_ (list): The class attribute to filter the target <a> tags.
    invList (list): The list to store the collected links.
    
    Returns:
    list: A list of all collected links to investor description pages from all pages.
    """
    # Create a copy of the current list of links
    currentList = invList.copy()
    
    # Print the current page number
    print(f"Page {pageNum}: ", end='')
    
    # Extract the BeautifulSoup object from the URL
    soup = web_extract(URL)
    
    # Extend the current list with links extracted from the current page
    currentList.extend(getDescriptionPageLink(soup, target_class_))
    
    # Get the URL for the next page
    nextURL = getNextPage(soup)
    
    # If there is a next page, increment the page number and continue recursion
    if nextURL:
        pageNum += 1
        return get_all_investorsLinkDescPagRecursively(nextURL, pageNum, target_class_, currentList)
    else:
        # Return the compiled list of links when no more pages are available
        return currentList


# In[8]:


def getInvestorName(in_soup):
    """
    Extracts the investor's name from the title of the investor's description page.

    Parameters:
    in_soup (BeautifulSoup object): The BeautifulSoup object representing the investor's 
    description page.

    Returns:
    str: The extracted investor's name.
    """
    # Extract the text from the <title> tag of the investor's description page
    name = in_soup.title.text
    
    # Split the title text by the '-' character to separate the name from any additional details
    splitName = name.split('-')
    
    # Take the first part of the split text as the investor's name and remove any leading/trailing whitespace
    name = splitName[0].strip()
    
    # Return the cleaned investor's name
    return name


# In[9]:


def getInvestorSpecificPage(in_soup):
    """
    Extracts the URL of the specific investor's page from the BeautifulSoup object of the 
    investor's description page.

    Parameters:
    in_soup (BeautifulSoup object): The BeautifulSoup object representing the investor's 
    description page.

    Returns:
    str or None: The URL of the specific investor's page if found, otherwise None.
    """
    # Find the tag with the specified class attributes indicating the link to the investor's page
    targetTag = in_soup.find(lambda tag: 'class' in tag.attrs and 
                          tag.attrs['class'] == ['line-clamp-1', 'underline'])
    
    # If the target tag is found, extract the href attribute from the <a> tag within it
    if targetTag:
       return targetTag.find('a').get('href')
    else:
        # Return None if the target tag is not found
        return None


# In[10]:


def getInvestorPartnersEmail(in_soup):
    """
    Extracts the email address of the investor's partner from the BeautifulSoup 
    object of the investor's description page.

    Parameters:
    in_soup (BeautifulSoup object): The BeautifulSoup object representing the 
    investor's description page.

    Returns:
    str or None: The email address of the investor's partner if found, otherwise None.
    """
    # Find the <a> tag with an 'href' attribute starting with 'mailto:'
    tempTag = in_soup.find('a', href=lambda href: href and href.startswith('mailto:'))
    
    # If the <a> tag is found, extract and return the email address
    if tempTag:
        mailTo = tempTag.get('href')  # Get the 'href' attribute value
        splitMailText = mailTo.split(':')  # Split the string at ':'
        return splitMailText[1]  # Return the part after ':'
    else:
        # Return None if no email address is found
        return None


# In[13]:


import pandas as pd

def getParnerDataFromInnovateUK(URL, pageNum, target_class_, invList):
    """
    Extracts data about investors from the Innovate UK website and compiles it into a DataFrame.

    Parameters:
    URL (str): The base URL of the Innovate UK website to start scraping.
    pageNum (int): The current page number for pagination.
    target_class_ (list): The target class attributes used to filter investor description links.
    invList (list): A list to accumulate investor description page links.

    Returns:
    DataFrame: A pandas DataFrame containing the extracted investor data.
    """
    # Initialize dictionaries and lists to store investor data
    investorData = {}
    investor_nameList = []
    investor_emailList = []
    investor_spec_webList = []

    # Retrieve all investor description page links
    investorDescripLinkList = get_all_investorsLinkDescPagRecursively(URL, pageNum, target_class_, invList)

    # Store the list of investor description page links in the dictionary
    investorData['Investor_Description_PageLink'] = investorDescripLinkList

    num = 1  # Counter for tracking the number of processed links
    for link in investorDescripLinkList:
        print(str(num) + ":", end=' ')
        
        # Extract and process the HTML content of the investor's description page
        tempSoup = web_extract(link)
        investor_nameList.append(getInvestorName(tempSoup))  # Extract investor name
        investor_spec_webList.append(getInvestorSpecificPage(tempSoup))  # Extract specific web link
        investor_emailList.append(getInvestorPartnersEmail(tempSoup))  # Extract investor email

        num += 1  # Increment the counter

    # Store the extracted data in the dictionary
    investorData['Investor_Partner_Name'] = investor_nameList
    investorData['Investor_Partner_Web'] = investor_spec_webList
    investorData['Investor_Partner_EmailContact'] = investor_emailList

    # Convert the dictionary to a pandas DataFrame
    investorDataframe = pd.DataFrame(investorData)

    return investorDataframe  # Return the DataFrame containing the investor data


# In[14]:


investorData = getParnerDataFromInnovateUK(baseURL, 1, targetClass, [])


# In[15]:


investorData


# In[ ]:




