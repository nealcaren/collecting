#!/usr/bin/env python
# coding: utf-8

# # Convert PDF to text 

# ```
# %conda install -c conda-forge pdf2image tesseract poppler
# %pip install pyocr
# ```
# 

# Details about pdf2image
# 
# https://github.com/Belval/pdf2image
# 
# Datils about pyocr
# https://gitlab.gnome.org/World/OpenPaperwork/pyocr
# 
# 

# In[1]:


from pdf2image import convert_from_path


# In[2]:


flyer = convert_from_path('../data/NAWSA.pdf')


# In[3]:


flyer[0]


# In[4]:


from pyocr.tesseract import image_to_string


# In[5]:


text = image_to_string(flyer[0])


# In[6]:


print(text)


# In[7]:


journal_pages = convert_from_path('../data/Progressive_Woman_Vol-4_Iss-42.pdf') 


# In[8]:


len(journal_pages)


# In[9]:


journal_pages[1]


# In[10]:


print(image_to_string(journal_pages[1]))


# ![](../images/rough_graph.png)

# In[11]:


file_name = '../data/Progressive_Woman_Vol-4_Iss-42.pdf'

pages = convert_from_path(file_name)
pages = pages[:3]


contents = []
for n, page in enumerate(pages):
    meta = {'text'        : image_to_string(page),
           'page_number'  : n + 1,
           'image'        : page,
           'fn'           : file_name}
    
    contents.append(meta)


# In[12]:


import pandas as pd
df = pd.DataFrame(contents)


# In[13]:


df.head()


# In[14]:


df['image'][2]


# In[15]:


df.to_json('pw.json')


# In[16]:


df2 = pd.read_json('pw.json')


# In[17]:


df2


# In[18]:


df.to_pickle('pw.pickle')


# In[19]:


df2 = pd.read_pickle('pw.pickle')


# In[20]:


df2.head()


# In[21]:


df2['image'][2]


# In[22]:


from pdf2image import convert_from_path
from pyocr.tesseract import image_to_string
import pandas as pd


def pdf_ocr_df(file_name):
    """
    OCR PDF returning a dataframe.
    """

    pages = convert_from_path(file_name)

    contents = []
    for n, page in enumerate(pages):
        meta = {
            "text": image_to_string(page),
            "page_number": n + 1,
            "image": page,
            "fn": file_name,
        }

        contents.append(meta)
    return pd.DataFrame(contents)


# In[23]:


df = pdf_ocr_df('../data/Mother-Earth_Vol-6_Iss-2.pdf')


# In[24]:


df.head()


# In[25]:


df['image'][6]


# In[26]:


print(df['text'][6])

