#!/usr/bin/env python
# coding: utf-8

# # Word Documents

# The best package for reading the contents of modern Word documents (i.e,. files with a  docx exctension) is `docx2txt`. It returns the full text, stripping out all formatting information. 
# 
# To install (from within a notebook):
# ~~~~
#     %conda install -c conda-forge docx2txt
# ~~~~

# In[1]:


import docx2txt


# In[2]:


text = docx2txt.process('../data/pandas_wiki.docx')


# In[3]:


text


# In[4]:


print(text)


# In[ ]:




