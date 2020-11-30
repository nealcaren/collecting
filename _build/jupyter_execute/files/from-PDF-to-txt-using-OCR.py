#!/usr/bin/env python
# coding: utf-8

# ## Install the required packages 
# 
# 

# ```
# %conda install -c conda-forge pdf2image tesseract poppler
# %pip install pyocr
# ```
# 

# In[5]:


get_ipython().run_line_magic('conda', 'install poppler')


# Details about pdf2image
# 
# https://github.com/Belval/pdf2image
# 
# Datils about pyocr
# https://gitlab.gnome.org/World/OpenPaperwork/pyocr
# 
# 

# In[6]:


from pdf2image import convert_from_path


# In[7]:


flyer = convert_from_path('../data/NAWSA.pdf')


# In[8]:


flyer[0]


# In[9]:


from pyocr.tesseract import image_to_string


# In[10]:


text = image_to_string(flyer[0])


# In[11]:


print(text)


# In[12]:


journal_pages = convert_from_path('../data/Progressive_Woman_Vol-4_Iss-42.pdf') 


# In[13]:


len(journal_pages)


# In[14]:


journal_pages[1]


# In[15]:


print(image_to_string(journal_pages[1]))


# ![](../images/rough_graph.png)

# In[17]:


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


# In[18]:


import pandas as pd
df = pd.DataFrame(contents)


# In[19]:


df.head()


# In[20]:


df['image'][2]


# In[23]:


df.to_json('pw.json')


# In[33]:


df2 = pd.read_json('pw.json')


# In[34]:


df2


# In[35]:


df.to_pickle('pw.pickle')


# In[29]:


df2 = pd.read_pickle('pw.pickle')


# In[30]:


df2.head()


# In[31]:


df2['image'][2]


# In[39]:


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


# In[ ]:


df = pdf_ocr_df('../data/Mother-Earth_Vol-6_Iss-2.pdf')


# In[ ]:


df.head()


# In[ ]:


df['image'][6]


# In[ ]:


print(df['text'][6])

