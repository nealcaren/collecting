#!/usr/bin/env python
# coding: utf-8

# # Undocument APIs

# Social scientists are often interested in collecting massive amounts of digital data from specific websites. When you are fortunate, someone else has already scrapped it for you and has released in on [GitHub](https://github.com) or as a [Kaggle dataset](https://www.kaggle.com/datasets). Sometimes the website provides an [API](https://en.wikipedia.org/wiki/Web_API), an interface for collecting the data in a systematic way that is usually reasonably well-document. The most prominent of these for social scientists is probably [Twitter](https://developer.twitter.com/en/docs.html), who have enabled hundreds of academic studies by making available information about posts and users. 
# 
# Other times, an API exists and is being used by the website, but information about is not publicly available. Most website searches, for example, involve using an internal web API. Your search term, along with other relevant parameters, is used to extract the corresponding results from a dataset and then displayed on a web page. While we see the data as part of a web page, the data is often transmitted in a different, more research-friend format, usually in a [JSON](https://en.wikipedia.org/wiki/JSON) format. Using an undocumented API allows you to systematically collect the data without the parsing the HTML of each page. 
# 
# Below, I walk through the steps I recently used  when trying to gather Fox News Opinion articles. In this case, the API doesn't return the full text of the articles, but, as is often the case, returns all the metadata about the article, including the article URL for subsequent scraping.
# 
# I use Python, but the overall logic is similar for other languages. 

# I begin by enabling the developer toolbar on my browser. In Safari, this is under **Preferences->Advanced** and then clicking **Show Develop Menu in Menu Bar**. The process is similar in Chrome. 

# I visited the front page.
# ![frontpage](../images/frontpage.png)
# 

# I clicked on **Opinion**, the section I wanted to scrape.
# ![opinion](../images/opinion.png)

# I scrolled down the page and found a list of articles with a **Show More** button. This type of button, which leads to the next set of results, is a key component for understanding how the webpage is structured.  
# ![more.png](../images/more.png)
# 

# In this case, **Show More** does not load a new page but it does expand the number of results shown on the existing page. If you copy the link associated with this button (`https://www.foxnews.com/opinion#`) and paste it in a new browser window, it merely displays the first set of results, so that is a dead end for uncovering an API. 
# 
# To be confident that there might be a decent number of articles available, I clicked the **Show More** button several times. Each time it loaded more articles.
# ![more.png](../images/more2.png)

# Lots of data is passed between my computer and the Foxnews website with each click. Additional information about these streams can be revealed through the **Develop** menu and then the **Show Page Resources** option.
# 
# ![develop.png](../images/develop.png)
# 

# This defaults to showing the page's HTML code.
# ![html.png](../images/html.png)

# To look for signs of an API, I click on the **Network** tab. Results are sometimes already listed, but I start clean by using the trash icon on the far right. With the **Network** tab visible, I then click **Show More** on the web page. Each resource exchanged between my computer and various servers are now displayed. When the action stops, I sort the list by size. 
# ![network.png](../images/network1.png)

# I now review each of the items for something that looks like the results of search API, a plain text file with the search results. 
# 
# Usually, the top of the list displays the images that the page retrieved. Images usually have a .png or .jpg extension. Selecting the first item in the results, an JPG with a name full of numbers, confirms that it is a picture. 
# 
# ![image.png](../images/network_image.png)

# The name of the second item, **article-search** has more promise. The **Preview** tab shows that this is a JSON object that appears to be a list of the articles that were returned after the **Show More** button was pressed. Bingo!
# 
# ![image.png](../images/network_search.png)
# 

# The **Header** tab reveals the specific URL that returned this JSON. 
# ![image.png](../images/network_header.png)
# 

# The URL has all the signs of an undocumented API. First, it contains "API" as part of the string. Second, it includes a series of search parameters, such as `isCategory` and `size`.  Now I copy the URL and paste and save it as a Python string. I split the string over several lines to view it more clearly.

# In[1]:


url = ('https://www.foxnews.com/api/article-search?'
       'isCategory=true&isTag=false&isKeyword=false&'
       'isFixed=false&isFeedUrl=false&searchSelected=opinion&'
       'contentTypes=%7B%22interactive%22:true,%22slideshow%22:true,%22video%22:false,%22article%22:true%7D&'
       'size=11&offset=30')


# The next step is to see if Python can access the API with a straightforward command. Some APIs require confirmation that the search is originating from original websites, while others do not enforce that. Figuring out the right way to programmatically access the website is a process of trial and error. I use the `requests` library.

# In[2]:


import requests

r = requests.get(url)
r.status_code


# A status code of 200 means that something was returned. 
# 
# Since it looked like a JSON object when viewed in the browser, I take advantage of the `requests` JSON decoder.

# In[3]:


r.json()


# The best way to turn a JSON into usable a format is with the `pandas` library.

# In[4]:


import pandas as pd

df = pd.DataFrame(r.json())


# In[5]:


df.head()


# That looks pretty good. The JSON appears to have some nested elements in it. For example, Category contains a dictionary. These can often be flattened with `json_normalize`.

# In[6]:


from pandas.io.json import json_normalize

df = json_normalize(r.json())

df.head()


# Great! This process demonstrates that FoxNews has an undocumented API that can be accessed via Python. The dataset, however, only has a few cases.

# In[7]:


len(df)


# The next step is to see if more data can be collected. I usually focus on two parameters: How do I get to the next set of results? Can I get more results with each call? 

# In[8]:


print(url)


# Looking back at the URL, the likely suspects for manipulation are `size`, which usually determines the number of results, and `offset` which usually means "start with the nth result". I first check to see how many results can be returned in one call. If the answer is 10,000, I don't need to do much more.
# 
# Since I'll be making many calls using the API, I write a quick function to take the URL and return a dataframe. Once I'm confident it will work, I would likely make a more robust function that allows more direct manipulation of the parameters, but I don't want to spend too much time on that if the whole API is a dead end.

# In[9]:


def fox_df(url):
    r = requests.get(url)
    df = json_normalize(r.json())
    print('Return a dataframe of length',len(df))
    return df


# I confirm that the function works using the original url.

# In[10]:


fox_df(url)


# As a first attempt, I try to retrieve 100 results.

# In[11]:


url100 = url.replace('size=11','size=100')

fox_df(url100)


# This does not return 100 results, but it does return 30, which appears to be the internal maximum.  Collecting a larger corpus of article metadata will need to be done in batches of 30. 
# 
# The next question is how far back can the API go? Here, the first suspect is the `offset` parameter. The current value of 30 is usually associated with starting with the 30th results. So an `offset` of 30 with a `size` of `10` is likely to return results 30-39.
# 
# As a first pass, I set the value of `offset` to 0 to get the most recent results.

# In[12]:


url_off = url.replace('offset=30','offset=0')

fox_df(url_off)


# The `lastPublicationDate` value of the first row is 2019-02-08. Hopefully a larger value will be associated with articles published earlier.

# In[13]:


url_off = url.replace('offset=30','offset=100')

fox_df(url_off)


# The article with an offset value of 100 was published on 2019-02-01, or roughly a week before our offset 0. Perfect! Increasing the offset value yields additional article metadata in chronological order. 
# 
# Next, how far back can we go?

# In[14]:


url_off = url.replace('offset=30','offset=1000')

fox_df(url_off)


# An offset of 1,000 takes us back about nine months.

# In[15]:


url_off = url.replace('offset=30','offset=5000')

fox_df(url_off)


# 5,000 brings us back to 2017. 

# In[16]:


url_off = url.replace('offset=30','offset=10000')

fox_df(url_off)


# But 10,000 fails. 😞.
# 
# After attempting multiple values, it appears something around 9,950 is the maximum offset that will return results, which is approximately three years of data. This limit could be hard coded into the API or this could simply be all the data that is available on the website. 

# In[17]:


url_off = url.replace('offset=30','offset=9950')

fox_df(url_off)


# The final step in collecting the article metadata via the API is to make all the necessary API calls to gather all the relevant article metadata. I slightly revise the `fox_df` function so that it takes a value of an offset. I hardcoded the URL, fixing the size to 30.  A more robust function would turn the entire set of parameters into a dictionary that was modifiable. I also took out the print statement which would clutter the results. 

# In[18]:


def fox_df(offset):
    url = ('https://www.foxnews.com/api/article-search?'
           'isCategory=true&isTag=false&isKeyword=false&'
           'isFixed=false&isFeedUrl=false&searchSelected=opinion&'
           'contentTypes=%7B%22interactive%22:true,%22slideshow%22:true,%22video%22:false,%22article%22:true%7D&'
           'size=30&offset=0')
    
    url = url.replace('offset=0', 'offset=%s' % offset)
    
    r = requests.get(url)
    df = json_normalize(r.json())
    return df


# Finally, I loop over the function. I create an empty dataframe and then append the results after each loop. I pause three seconds each pass in order to not access the web server too many times. The first time I ran this, I only retrieved a few pages of results to make sure everything worked.

# In[19]:


from time import sleep # for pausing

# create empty dataframe to store results
fox_opinion_df = pd.DataFrame() 

# Create a loop that counts up by 30.
for offset in range(0, 1000, 30):
    new_df = fox_df(offset)
    
    # Add the new results to the existing database
    fox_opinion_df = fox_opinion_df.append(new_df, ignore_index=True)
    
    # Pause for three seconds to be polite to the web server
    sleep(3)
    


# In[20]:


fox_opinion_df.tail()


# The dataframe can be stored as either as CSV file or JSON. CSV is best if you want to use it elsewhere, while a JSON usually is more robust to handling text strings which somtimes trip up CSV readers. 

# In[21]:


fox_opinion_df.to_csv('foxnews_opinion.csv')


# In[22]:


fox_opinion_df.to_json('foxnews_opinion.json', orient ='records')


# Things aren't always this easy, but when you stumble across an undocumented API you can quickly put together a dataset.
