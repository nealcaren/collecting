#!/usr/bin/env python
# coding: utf-8

# # Downloading newspaper articles  
# 

# If you are interested in scrapping newspaper data, you might not need to build your own scraper. The [Newspaper](https://newspaper.readthedocs.io/en/latest/) library is a powerful tool for scraping the text and relevant meta data, such as author and title from newspaper articles and other online media sources. 
# 
# Newspaper works by looking for commonly occurring  tags, such as "byline" or "author", to identify the relevant components of a newspaper article, including title, author, publication date, and text. Even when it doesn't work completely, by for example, extracting everything but the author, it can greatly reduce the amount of time you spend inspecting the parsing the HTML by hand.  

# If this is your first time running this notebook, you may need to install Newspaper:
# 
# ```
# !pip install newspaper3k
# ```

# Newspaper has the ability to scan the front page of a media source and identify all the articles on the page using the `build` method. A more common scenario for researchers is to have a list of articles URLs, created either from the paper's API or scrapped using the paper's search function. In this case, Newspaper's `Article` method is used to download, parse and extract the relevant information.

# In[2]:


get_ipython().system('pip install newspaper3k')
from newspaper import Article


# On February 25th, 2019, the Associated Press published, "[Worker visas in doubt as Trump immigration crackdown widens
# ](https://apnews.com/af878855969c4b48bc8b083b91c67018)".
# 
# ![visas](images\visas.png)

# I save the URL as a variable.

# In[3]:


url = "https://apnews.com/af878855969c4b48bc8b083b91c67018"


# Article is a three step process. First, create an Article object, which I'll call article. The page then needs to be download and parsed.

# In[4]:


article = Article(url)
article.download()
article.parse()


# The article object stores the results of the parse as different properties of the object. The most relevant of these are title, authors, publish_date and text. I check these four to make sure that page was able to be parsed.

# In[5]:


article.title


# In[6]:


article.authors


# Authors returns a list. In this case, it only has one item. 

# In[7]:


article.publish_date


# In this case, publish_date returns the publication date and time converted into a Python datetime object. 

# In[8]:


print(article.text)


# In this case, the full-text of the article has been returned. It also returned the image caption (at the top) and author contact information (at the bottom). These might need to be trimmed later on. 

# Anytime I'm using Newspaper, I want to store data on many different newspaper articles. To automate this process, I created a function that takes a URL and returns a dictionary containing the extracted meta data along with the html code, in case I want to extract additional information later on by hand. It also good to always have the data you are collecting in the original format, rather than just the parsed information. Note that one limitation of Newspaper is that it does not work on HTML files you have downloaded elsewhere. 

# In[9]:


def get_article_info(url):
    """Download and parse a newspaper url."""
    article = Article(url)
    article.download()
    article.parse()

    article_details = {
        "title": article.title,
        "text": article.text,
        "webUrl": article.url,
        "authors": article.authors,
        "html": article.html,
        "date": article.publish_date,
        "description": article.meta_description,
    }
    return article_details


# I confirm that it works.

# In[10]:


a = get_article_info(url)
print(a["title"])


# One of the many uses of the pandas library is to convert and store different types of data. In this case, pandas can be used to convert the dictionary returned by `get_article_info` into a dataframe, which can be subsequntly stored as a JSON file.

# In[11]:


import pandas as pd


# In[12]:


df = pd.DataFrame.from_records(a)


# In[13]:


df.head()


# In[14]:


df.to_json("ap_articles.json", orient="records")


# While this might seem like overkill for one article, it scales up quite nicely if you have a longer list of URLs.

# In[15]:


urls = [
    "https://apnews.com/43bcb090972f4cc48999e8cc32de38a3",
    "https://apnews.com/1cc6b8d081154945addfd71fadb88561",
    "https://apnews.com/7820c2fdb5b14ef9baef8b1e5cad3c0b",
]


# In[16]:


article_data = []  # Blank list to store results

# Loop over each URL
for url in urls:
    a = get_article_info(url)
    article_data.append(a)

# convert list of dictionaries to dataframe
df = pd.DataFrame.from_records(article_data)


# In[17]:


df.head()


# I have some suggests on best practices for [downloading a lot of files](https://github.com/nealcaren/Lessons/blob/master/Notebooks/Downloading.ipynb), which are relevant here, since you want to avoid downloading each article more than once. 
# 
# I have found that the most common issue with newspaper is that it missing the author information. A second issue is that it sometimes only retrieves part of the text with articles ending, "Click here to continue." In either of those cases, I usually start by using Newspaper to download and parse all the information and supplement the columns it creates with additional ones based on parsing the article text store in the HTML column. 
