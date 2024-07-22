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


# In[11]:


from openai import OpenAI


# In[18]:


def createPrompt(in_text):
    """
    Creates a prompt for extracting specific information from a given text.

    Parameters:
    in_text (str): The input text from which to extract information.

    Returns:
    str: A formatted prompt string for extracting "Investment Amount" and "Sector of focus".
    """
    # Format the prompt with instructions for extraction and include the input text
    prompt = f"""
    Extract "Investment Amount" and "Sector of focus" from this text. Return the output in two lines of text in this format:
    "Investment amount": 'investment amount' if provided in the text OR 'None' if not provided
    "Sector of focus": 'sector of focus' if provided in the text OR 'None' if not provided:
    {in_text}
    """

    return prompt


# In[19]:


def promptGPT_API(prompt):
    """
    Sends a prompt to the GPT API and streams the response.

    Parameters:
    prompt (str): The prompt to send to the GPT model.

    Returns:
    list: A list containing the response chunks from the GPT model.
    """
    
    # Initialize the OpenAI client (assuming the API key is set in the environment)
    client = OpenAI()

    #You can assign the API key directly in the script by using:
    #client = OpenAI(api_key='your-api-key')

    # Create a streaming chat completion request with the specified model and prompt
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    # Initialize a list to store the response chunks
    response = []

    # Iterate over the streamed response chunks
    for chunk in stream:
        # Check if the current chunk has content
        if chunk.choices[0].delta.content is not None:
            # Extract the content from the current chunk
            content = chunk.choices[0].delta.content
            # Append the content to the response list
            response.append(content)
            # Print the content to the console without adding a newline
            #print(chunk.choices[0].delta.content, end="")
    
    # Print a newline character to end the streaming output
    #print()
    
    # Return the list of response chunks
    return response


# In[20]:


def getCleanTextFromSoup(soup_obj):
    """
    Cleans and extracts text from a BeautifulSoup object by removing newline,
    tab, and carriage return characters.

    Parameters:
    soup_obj (BeautifulSoup): The BeautifulSoup object from which to extract and clean text.

    Returns:
    str: The cleaned text extracted from the BeautifulSoup object.
    """
    # Extract the text from the BeautifulSoup object and replace newline characters with an empty string
    text = soup_obj.text.replace('\n', "")
    # Replace tab characters with an empty string
    text = text.replace('\t', "")
    # Replace carriage return characters with an empty string
    text = text.replace('\r', "")

    # Return the cleaned text
    return text


# In[21]:


def editResponse(gptResp):
    """
    Processes the response from the GPT API to extract investment amount and sector information.

    Parameters:
    gptResp (list): A list of strings representing the chunks of text from the GPT response.

    Returns:
    tuple: A tuple containing two elements:
           - Investment (str): The investment amount extracted from the response.
           - Sector (str): The sector extracted from the response.
    """
    # Join all chunks of the GPT response into a single string
    respText = ''.join(gptResp)
    
    # Split the concatenated response text by newline characters to separate lines
    InvAmoun_Sector = respText.split('\n')
    
    # Extract the investment amount from the first line by splitting on ':' and trimming whitespace
    Investment = InvAmoun_Sector[0].split(":")[1].strip()
    
    # Extract the sector from the second line by splitting on ':' and trimming whitespace
    Sector = InvAmoun_Sector[1].split(":")[1].strip()

    # Return the extracted investment amount and sector as a tuple
    return Investment, Sector


# In[22]:


def get_InvAmnt_Sector(in_soup):
    """
    Extracts investment amount and sector information from a BeautifulSoup object by
    sending the text content to the GPT API and processing the response.

    Parameters:
    in_soup (BeautifulSoup): The BeautifulSoup object containing the HTML content to be processed.

    Returns:
    tuple: A tuple containing two elements:
           - InvAmnt (str): The extracted investment amount.
           - Sector (str): The extracted sector.
    """
    # Clean and extract text from the BeautifulSoup object
    text = getCleanTextFromSoup(in_soup)
    
    # Create a prompt for the GPT API using the cleaned text
    gptPrompt = createPrompt(text)
    
    # Send the prompt to the GPT API and retrieve the response
    resp = promptGPT_API(gptPrompt)
    
    # Process the GPT response to extract investment amount and sector
    InvAmnt, Sector = editResponse(resp)

    # Return the extracted investment amount and sector as a tuple
    return InvAmnt, Sector


# In[23]:


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
    investor_nameList = []  # List to store investor names
    investor_emailList = []  # List to store investor email addresses
    investor_spec_webList = []  # List to store specific web links for each investor
    investment_amnt = []  # List to store investment amounts
    sector_of_focus = []  # List to store sectors of focus for each investor

    # Retrieve all investor description page links by recursively scraping pages
    investorDescripLinkList = get_all_investorsLinkDescPagRecursively(URL, pageNum, target_class_, invList)

    # Store the list of investor description page links in the dictionary
    investorData['Investor_Description_PageLink'] = investorDescripLinkList

    num = 1  # Counter for tracking the number of processed investor links
    for link in investorDescripLinkList:
        print(str(num) + ":", end=' ')  # Print the current link number
        
        # Extract and process the HTML content of the investor's description page
        tempSoup = web_extract(link)  # Fetch and parse the HTML content using BeautifulSoup
        investor_nameList.append(getInvestorName(tempSoup))  # Extract and store investor name
        investor_spec_webList.append(getInvestorSpecificPage(tempSoup))  # Extract and store specific web link
        investor_emailList.append(getInvestorPartnersEmail(tempSoup))  # Extract and store investor email
        inv, sec = get_InvAmnt_Sector(tempSoup)  # Extract investment amount and sector
        investment_amnt.append(inv)  # Store the investment amount
        sector_of_focus.append(sec)  # Store the sector of focus

        num += 1  # Increment the counter

    # Store all extracted data in the dictionary
    investorData['Investor_Partner_Name'] = investor_nameList
    investorData['Investor_Partner_Web'] = investor_spec_webList
    investorData['Investor_Partner_EmailContact'] = investor_emailList
    investorData['Investment_Amount'] = investment_amnt
    investorData['Focused_Sector'] = sector_of_focus

    # Convert the dictionary to a pandas DataFrame (commented out in this code)
    # investorDataframe = pd.DataFrame(investorData)

    # Return the dictionary containing the extracted investor data
    return investorData


# In[24]:


Inv_Data_Dict = getParnerDataFromInnovateUK(baseURL, 1, targetClass, [])


# In[26]:


import pandas as pd
invData_compiled = pd.DataFrame(Inv_Data_Dict)


# In[27]:


invData_compiled


# In[28]:


invData_compiled.to_csv('compiledData.csv')


# In[ ]:




