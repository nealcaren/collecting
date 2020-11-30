#!/usr/bin/env python
# coding: utf-8

# # Downloading in Bulk

# Web scraping frequently involves analyzing hundreds or thousands of files. Figuring out what data you need from a page, along with the best method for extracting this data, is often an iterative process. After processing all the documents, your scraper might not have worked the way you thought it was working. The format of the pages might be different for a subsample of the pages and your scraper returns nothing for them. Six months later, you might want to get one more piece of information from each page. Downloading web pages or using an API takes time and costs the provider money. The content of pages and their availability also changes over time. This all means that it makes the most sense to gather all your web data and store it locally before you start analyzing it. 
# 
# This lesson walks you through the basic steps for downloading and storing data. The lesson assumes that you have some basic knowledge of Python and a list of URLs you want to download.
# 

# I begin by importing the standard library for acessessing web pages or APIs, [requests](http://docs.python-requests.org/en/master/). 

# In[1]:


import requests


# No matter how many URLs I eventually need to download, I always start with a single sample URL to make sure the process works before creating a loop. In this case, I'm interested in Fox News opinion pieces:

# In[2]:


url = 'https://www.foxnews.com/opinion/gutfeld-on-hiring-combat-vets-to-defend-schools'


# Using `requests`, I access the page and retrieve the HTML.

# In[3]:


r = requests.get(url)
html = r.text


# Sometimes this works, but the actual content is not what you get when you access the web page using a browser. To confirm that things went as planned, I display the contents of the file as a browser would.

# In[4]:


from IPython.display import HTML

HTML(html)


# Since that worked, I want to save the file. I create a directory to store what will eventually be numerous files.

# In[5]:


import os 

os.mkdir('fox-html')


# If the directory already exists, this command will produce an error.
# 
# Before the file is saved, it needs a name.  URLs often involve characters that can cause trouble in file names, such as `\` `,` `:` or `?`. I use slugify to create an operating-system safe name for the file. This may need to be added to your Python installation. I use `conda` so that the package is integrated into my existing environment with the `conda-forge` since python-slugify is not in the default conda channel.
# 

# Slugify creates a filename that is both usable by your computer as a filename and is human readable.

# In[13]:


from slugify import slugify

slugify('Convert to /file name!.please.html')


# In[14]:


slugify(url)


# Saving text files, such as the one we've downloaded, is one of the less intuitive aspects of Python for those coming from a social science background. Unfortuntately, pandas can't solve this problem.
# 
# In this case, we need to both create the file name and make sure the file is put into the correct directory.

# In[8]:


file_name = slugify(url)
directory = "fox-html"

location = os.path.join(directory, file_name)

with open(location, "w") as outfile:
    outfile.write(html)


# I'll use this process of downloading and saving many times, so I put it in a function that takes two parameters: the URL to create the filename and the HTML text to be saved. I put the construction of a the file location in a separate function because I will need to use that piece later in a different context. I also have the script pause for three seconds so the web server is not overwhelmed by our program. 

# In[ ]:


from time import sleep


def locate(url):
    """Create file name and place in directory"""
    file_name = slugify(url)
    location = os.path.join("fox-html", file_name)
    return location


def get_html(url):
    """Download & save a HTML url as a text file.
    using the url to create the filename."""
    sleep(3)
    r = requests.get(url)
    html = r.text

    location = locate(url)

    with open(location, "w") as outfile:
        outfile.write(html)


# When it works, it does not return or display anything. 

# In[16]:


get_html(url)


# Note that the project-specific "fox-html" directory is hard coded into the function. If you copy and paste this function, be sure to update the directory to include whatever name you are using.

# The function can now be used to download many URLs. For example, if you had a list of six URLs, you could loop over them.

# In[23]:


urls = [
    "https://www.foxnews.com/opinion/newt-gingrich-i-saw-the-south-korean-miracle-for-myself-it-was-incredible",
    "https://www.foxnews.com/opinion/gutfeld-on-hiring-combat-vets-to-defend-schools",
    "https://www.foxnews.com/opinion/doug-schoen-amazons-cancellation-of-a-move-to-nyc-is-bad-news-and-could-hurt-far-left-dems-at-polls",
    "https://www.foxnews.com/opinion/amazon-quits-new-york-victory-by-progressives-helps-city-wave-good-bye-to-25000-jobs",
    "https://www.foxnews.com/opinion/william-barr-is-our-new-attorney-general-here-are-four-things-he-should-focus-on-right-away",
    "https://www.foxnews.com/opinion/karl-rove-trumps-approval-numbers-are-going-up-three-things-could-keep-his-momentum-going",
]


# In[24]:


for url in urls:
    get_html(url)


# If something went wrong, the loop will stop and display an error message. 
# 
# We can confirm that it worked by listing the files in the HTML directory.

# In[25]:


os.listdir('fox-html')


# If you had a modest sized list of files to download, you are done. You now have a directory with all your files ready for subsequent analysis.
# 
# If you have a larger list of files, however, you'll want a loop that is robust to errors and to that is able to restart without re-downloading files you have already collected. 

# The `get_html` code can be modified so that, if something goes wrong with the download, it prints out an error message and pauses for 10 seconds. Since the problem may be related to the server, you'll want to slow down the process when things are not going well.

# In[28]:


def get_html(url):
    """Download & save HTML text using the url to create the filename."""
    sleep(3)
    try:
        r = requests.get(url)
        html = r.text
    except:
        print("Problem with", url)
        sleep(10)
    else:
        location = locate(url)
        with open(location, "w") as outfile:
            outfile.write(html)


# The loop can also modified to  download the file from the internet only once. If you are downloading thousands of files, you don't want all your work to go to waste just because something will almost inevitably go wrong along the way. 
# 
# Python's way of including this check in the loop is to first confirm whether or not the file exists. If it doesn't exist, because our attempt to open it fails, then, and only then, do we download it.
# 
# I first write a helper function that attempts to load the file based on the URL name. This takes advantage of our previously defined `locate` function.

# In[ ]:


def confirm_file(url):
    """Attempt to open a file based on the url."""
    location = locate(url)

    with open(location, "r") as infile:
        html = infile.read()


# I now update the loop. First, I try to opening the file. When that doesn't work, I attempt to download it.

# In[ ]:


for url in urls:
    try:
        confirm_file(url)
    except:
        get_html(url)


# When you are running a loop like this on a modest number of URLs, you might add a `print` statement for each URL just to make sure that things are progressing. For 100,000 URLs, however, this will clog up your screen and your computer memory, so make sure to remove them before letting the script run wild.

# # Putting it all together

# One issue with re-using the same set of loops and functions for different projects is that the directory for the project is hard coded into the `locate` function. This can be fixed by adding a second parameter, `directory`. The directory variable has a default value of `HTML`. 

# In[66]:


def locate(url, directory = "HTML"):
    """Create file name and place in directory"""

    file_name = slugify(url)
    location = os.path.join(directory, file_name)
    return location


# The function can be expanded to create the directory if it is missing.

# In[67]:


def locate(url, directory = "HTML"):
    """Create file name and place in directory"""

    # Confirm directory exists
    if os.path.isdir(directory) == False:
        print("Creating %s directory" % directory)
        os.mkdir(directory)

    file_name = slugify(url)
    location = os.path.join(directory, file_name)
    return location


# We need to update the other two functions to include the directory information.

# In[68]:


def get_html(url, directory='HTML'):
    """Download & save a HTML url as a text file.
    using the url to create the filename."""
    sleep(3)
    r = requests.get(url)
    html = r.text

    location = locate(url, directory)

    with open(location, "w") as outfile:
        outfile.write(html)
        
def confirm_file(url, directory='HTML'):
    """Attempt to open a file based on the url."""
    location = locate(url, directory)

    with open(location, "r") as infile:
        html = infile.read()
        


# The `confirm` and `download` functions can be combined into one function. We can also make the function a little more friendly to long lists by having the function stop when you interrupt it with a keyboard break, rather than just moving on to the next URL.

# In[69]:


def get_url(url, directory="HTML"):
    """If URL not stored locally, download it."""
    try:
        confirm_file(url, directory)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        get_html(url, directory)


# Finally, the loop can be rewritten as a function that takes a URL directory. 

# In[70]:


for url in urls:
    get_url(url)


# # URLs in Pandas

# In one of the columns in your pandas data frames, you could download all the HTML files by using the `apply` method with the `get_url` function on the column. 

# In[76]:


import pandas as pd

df = pd.DataFrame(urls, columns=['url'])


# In[77]:


df


# In[78]:


df['url'].apply(get_url)


# Since our `get_url` function only downloads the files but doesn't return anything, pandas returned an empty series. However, the functions could be altered slightly to return the text. Since the HTML is processed during both the `get_html` and `confirm_html` functions, we can add a `return` statement to send back the results. 

# In[83]:


def get_html(url, directory='HTML'):
    """Download & save a HTML url as a text file.
    using the url to create the filename."""
    sleep(3)
    r = requests.get(url)
    html = r.text

    location = locate(url, directory)

    with open(location, "w") as outfile:
        outfile.write(html)
        
    return html # new line
        
def confirm_file(url, directory='HTML'):
    """Attempt to open a file based on the url."""
    location = locate(url, directory)

    with open(location, "r") as infile:
        html = infile.read()
        
    return html # new line   
        
def get_url(url, directory="HTML"):
    """If URL not stored locally, download it."""
    try:
        return confirm_file(url, directory) # updated line    
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return get_html(url, directory) # updated line       


# The new function can be be used to create a dataframe column that contains the HTML of the URLs for later text analysis. 

# In[85]:


df['html'] = df['url'].apply(get_url)

df.head()

