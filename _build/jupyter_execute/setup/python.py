#!/usr/bin/env python
# coding: utf-8

# # Python Basics

# 
# This section introduces some of the most relevant aspects of working with Python for social scientists. This includes the different data types available and ways to modify them. 
# 

# ## Strings
# 

# Dorothy Parker is credited with the expression, 
# 
# > Heterosexuality is not normal, it is just common.
# 

# To store that in Python, create a new variable called `sentence`

# In[1]:


sentence =  'Heterosexuality is not normal, it is just common.'


# The text is surrounded by a single quote (`'`) on each side. 
# To make sure that you typed the tweet correctly, you can type `sentence`:

# In[2]:


sentence


# You can get almost the same response using the `print` function:
# 
# 

# In[3]:


print(sentence)


# The only difference is that the first response was wrapped in single quotes and the second wasn’t. As a side note, the single quotes weren’t because you put them there. If you used double quotes, Python would still show a single-quote.

# In[4]:


sentence =  "Heterosexuality is not normal, it is just common."

sentence


# In addition to `'` and `"`, strings can also be marked with a `'''`. This last one is particularly useful when your text contains contractions or quotation marks. 

# In[5]:


new_sentence = '''According to Parker, "Heterosexuality is not normal, it is just common."'''


# In[6]:


print(new_sentence)


# ### String Exercise 1
# 
# 
# Create a new string called `food` that is a sentence about your most recent meal. Display the contents of your new string. 
# 

# In[7]:


# Type your answer here


# In[8]:


food = 'I had a pizza for lunch.'
print(food)


# Python has a few tools for manipulating text, such as `lower` for making the string lower-case.

# In[9]:


sentence.lower()


# This did not alter the original string, however.

# In[10]:


sentence


# In Python, strings are immmutable, meaning once a string is created, it cannot be altered in place. To get around this, we can store the results from the `lower` command in a new variable.

# In[11]:


lower_sentence = sentence.lower()

lower_sentence


# ### String Exercise 2
# 
# Create a new, lower cased version of your `food` string.
# 

# In[12]:


# Your answer here.


# In[13]:


food_lower = food.lower()


# We can also `replace` text within the string.

# In[14]:


sentence.replace("Heterosexuality", "Monogamy")


# `replace` can also be used to remove text without replacement.

# In[15]:


sentence.replace(",", "")


# As before, this does not alter the original string. If you wanted to save the string edits, you would need to create a new variable.
# 
# 
# 
# 
# 

# In[16]:


edited_sentence = sentence.lower()
print(edited_sentence)


# If you were doing a series of manipulations, you could reuse a varaiable name, although it is best practice to keep a version of the original string in case you ever need to go back to it. 

# In[17]:


edited_sentence = sentence.lower()
print(edited_sentence)

edited_sentence = edited_sentence.replace(".", "")
print(edited_sentence)


# You can also stack multiple transformations together, although combining too many may make your code harder to follow.

# In[18]:


edited_sentence.replace(".", "").lower()


# ### String Exercise 3
# 
# Create a new string called `boring` that removes the exclamation marks and capitalization from the sentence "Way to go!!!"  
# 

# In[19]:


# Your answer here.


# In[20]:


boring = "Way to go!!!".replace('!','').lower()
print(boring)

# Alternatively:
exciting = "Way to go!!!".replace('!','')
boring   = exciting.replace('!','')
boring   = boring.lower()
print(boring)


# ## Slicing
# 
# If you had a very long text, such as the entire text of a Wikipedia article, you might only want to look at the first few characters. In Python, this is called by slicing.

# In[21]:


sentence


# In[22]:


sentence[0:20]


# A slice is signaled with brackets (`[]`). The first number is the starting position, where 0 indicates the beginning. This is followed by a colon (`:`) and then the end position, which, in this case, is a 20. Note that this is splitting on characters, not words.
# 
# Here is a section from the middle of the string:

# In[23]:


sentence[20:32]


# For convience, if you ommit the number before the colon, it defaults to the string beginning.

# In[24]:


sentence[:40]


# Ommitting the second number defaults to the end.

# In[25]:


sentence[40:]


# Finally, negative numbers are interpreted as distance from the end of the string.

# In[26]:


sentence[-20:]


# ### Slicing Exercise 1
# 
# 
# Create a new string called `s` that contains `The weather is hot and humid today.` Find the slices for each of the following :
# * `The we`
# * `today.`
# * `hot and humid`
# 
# 

# In[27]:


#Your answer here.


# In[28]:


s = 'The weather is hot and humid today.'
print(s[:6])
print(s[-6:])
print(s[15:-7])


# ## Numbers
# 
# We can also count the number of characters in a string with the `len` function.

# In[29]:


len(sentence)


# In this case, Python returned an interger instead of string. This also can be stored in a variable.

# In[30]:


sentence_length = len(sentence)


# In[31]:


sentence_length


# ### Numbers Exercise 1
# 
# 
# What is the length of the sentence `How many dogs do you own?`? Store it in a variable called `sl`.
# 

# In[32]:


# Your answer here.


# In[33]:


sl = len('How many dogs do you own?')
print(sl)


# Since this is a number, we can do standard math operations with it.

# In[34]:


print(sentence_length * 3)


# In[35]:


print(sentence_length / 2)


# In[36]:


print(sentence_length + sentence_length)


# ### Numbers Exercise 2
# 
# 
# What is one-third the length of `sl`?
# 

# In[37]:


# Your answer here


# In[38]:


print(sl/3)


# As with strings, these can be saved in new variables.

# In[39]:


double_length = sentence_length + sentence_length

print(double_length)


# These same operators also work with strings.

# In[96]:


print('Frogs' * 3)


# In[97]:


print('sociology' + 'political science')


# The operators can't be used to combine different data types, however.

# In[98]:


print("The sentence was " + sentence_length + "characters.")


# Conviently, Python the `str` function will convert an interger to a string.

# In[99]:


print("The sentence was " + str(sentence_length) + " characters.")


# I manually had to include the spaces before and after `sentence_length`. Otherwise, it all is smushed together. 

# In[100]:


print("The sentence was" + str(sentence_length) + "characters.")


# ### Numbers Exercise 3
# 
# 
# Print `The length of the word "hippopotamus" is [x].` where `[x]` is the length of the word hippopotamus .
# 

# In[101]:


#Your answer here.


# In[102]:


l = len('hippopotamus')
s = 'The length of the word "hippopotamus" is ' + str(l) + '.'
print(s)


# ## Lists
# 
# We can also `split` the sentence into a series of strings. By default, this splits based on spaces and other whitespace characters such as a line break (`\n`) or tab character (`\t`). 

# In[103]:


print(sentence.split())


# What is returned here is a third data type (the first two were strings and intergers) called a list. A list is enclosed in brackets (`[]`) and the items are seperated by commas. In this case each item is in quotation marks because they are all strings. Items in a list, however, can be of any sort.

# In[104]:


my_list = ['Speeches', 7, 'Data']
my_list


# While `len` returned the number of characters in a string, it returns the number the items in a list.

# In[105]:


len(my_list)


# In[106]:


sentence_length = len(sentence.split())
sentence_length


# In the second example, the list created by `sentence.split()` is not saved in any way; only its length.

# ### Lists Exercise 1
# 
# 
# Create a list called `food` that includes at least three things you ate today. Use `len` to count the number of items in the list.

# In[107]:


# Your answer here


# In[108]:


food = ['pizza slice', 'naan', 'cupcake', 'grape']
print(len(food))


# Like, strings, lists can also be sliced. The first three items of a list:

# In[109]:


words = sentence.split()
print(words[:3])


# We can also extract specific items from a list by their position. As it did with strings, slicing in Python starts with 0.

# In[110]:


words[0]


# The third word:

# In[111]:


words[3]


# The fifth word from the end:

# In[112]:


words[-5]


# The last two words, returned as a list:

# In[113]:


words[-2:]


# ### Lists Exercise 2
# 
# 
# Display the first two items of your `food` list. What is the last item?
# 

# In[114]:


# Your answer here


# In[115]:


#Sample Answer 

print(food[:2])
print(food[-1])


# Unlike a string, lists are mutable. That means that we can remove or as is more frequently the case text analysis, add things to it. This is done with `append`.

# In[116]:


male_words = ['his', 'him', 'father']
male_words.append('brother')
print(male_words)


# Since `append` is changing `male_words`, we do not want to use an `=`. The Python interpreter is editing our original list but not returning anything.

# In[117]:


not_going_to_work = male_words.append('brother')
print(not_going_to_work)


# Lists can be also be combined using `+`.

# In[118]:


gendered_words = male_words + ['her', 'she', 'mother']
print(gendered_words)


# As note above, the items in a list can include a variety of data types. This includes lists.

# In[119]:


gendered_lists = [ male_words ,  ['her', 'she', 'mother'] ]


# Note the two closing brackets next to each other. The first closes the list that ends with 'mother' while the second closes our `gendered_lists`.

# In[120]:


len(gendered_lists)


# `gendered_lists` has a length of two because it contains just two items, each a list of varying lengths.

# In[121]:


print(gendered_lists)


# ### Lists Exercise 3
# 
# 
# Add three more items to your `food` list. Use`append` for the first item. 
# For the other two, place them in a new list and then combine the two lists.
# 

# In[122]:


# Your answer here


# In[123]:


# Sample answer

food.append('panini')
print(food)
food = food + ['burrito', 'box of donuts']
print(food)
print(len(food))


# ## Dictionaries

# A fourth useful data type is a dictionary. A dictionary is like a list in that it holds multiples items. The items in a list can be identified by their position in the list. In contrast, the values in a dictionary are associated with a keyword. The analogy here is a to a physical dictionary, which has a list of unique words, and each word has a definition. In this case, the entries are called keys, and the definitions, which can be any data type, are called values. 
# 
# Alternatively, you can think of a dictionary as a single row of data from a dataset, where the keys are the variable names.

# In[124]:


respondent = {'sex'   : "female",
              'abany' : 1,
              'educ'  : 'College'}


# Dictionaries are surrounded by curly brackets (`{}`). Each entry is pair consisting of the key, which must be a string, followed, by a colon and then the value. Like in a list, entries are seperated by commas.
# 
# 

# We can access the contents of a dictionary by enclosing the key in brackets (`[]`).

# In[125]:


respondent['sex']


# If the key is not dictionary, you will get a `KeyError`.

# In[126]:


respondent['gender']


# You can inspect all the keys in a dictionary, in case you forgot or someone else made it.

# In[127]:


respondent.keys()


# In[128]:


len(respondent.keys())


# Dictionaries are mutable, so we can change the value of existing keys, remove keys, or add new ones.

# In[129]:


respondent['race'] = 'Black'

print(respondent)


# In[130]:


respondent['abany'] = 'Yes'

print(respondent)


# ### Dictionaries Exercise 1
# 
# Add a new key to the dictionary called `age` with a value of 37. Confirm that you did it correctly by dispaying the value of `age`.

# In[131]:


# Your answer here.


# In[132]:


respondent['age'] = 37
print(respondent['age'])


# As noted above, while the keys have to be strings, the values can be any data type.

# In[133]:


respondent['children ages'] = [3, 5, 10]

print(respondent)


# ## Spaces
# 

# Within the Python community, there are strong norms about how code should be written. Many of these are centered around making the code readable, both by others and by your future self. As a trivial example, `2+2` is allowed, but is almost always written `2 + 2`. Likewise, I defined my respondent dictionary with plenty of white space to maximize readability.

# In[78]:


respondent = {'sex'   : "female",
              'abany' : 1,
              'educ'  : 'College'}


# This is identical to:

# In[79]:


respondent={'sex':'female','abany':1,'educ':'College'}


# 
# 
# but putting it all on one line obscures the logic of the dictionary. In this case, what is a key and what is a value is quite clear in the first version, while distinguishing between the two is more problematic in the single-line version. 
# 
# 

# In[80]:


r2 = {'sex':'male',   'abany':1, 'educ':'College'     }
r3 = {'sex':'female', 'abany':0, 'educ':'High School' }
r4 = {'sex':'male',   'abany':0, 'educ':'Some College'}


# In[81]:


respondents = [respondent, r2, r3, r4]


# In[82]:


respondents


# This now looks a lot like the common data format JSON!

# ## Loops

# In[83]:


for person in respondents:
    print(person['educ'])


# In[84]:


for item in [1,2,'bobcat']:
    print(item)


# ### Loops Exercise 1
# 
# 
# Loop over the items in your `food` list. For each item, print its length.

# In[143]:


#Your answer here.


# In[144]:


for item in food:
    item_len = len(item)
    print(item_len)


# 
# 
# ## Functions

# For those who come from Stata or R background, one of the more striking aspects of Python code is the frequency of user-defined functions. These functions are deployed both for cases where you are surprised that no one has already written a function, such as counting words in a sentence, and for highly-custom situations, such as scraping the contents of a particular web page.   Programming with many small functions tends to make code more readable and easier to debug than code written in a more traditional social science style.
# 
# A standard function has three parts. First, the function is named. Subsequent line(s) do the legwork of performing the desired task. Finally, the results are returned.  
# 
# A trivial function that returns the `Hello!` might look like:

# In[87]:


def make_hello():
    word = 'Hello!'
    return word


# Of note, `def` signals that you are defining a function. This is followed by the name of the function. In this case, `make_hello`. Since this function doesn't take any arguments, such as accepting a variable to modify or have any options, it is followed by `()`. The first line ends with a colon.
# 
# All subsequent lines are indented. The second line creates a new string variable called `word` which contains `Hello!`. The third and final line of the functions returns the value stored in word. 

# In[88]:


make_hello()


# More commonly in text analysis, a user-defined function modifies an existing string. In this case, the variable name that will be used within the function is established within the parentheses on the opening line. 
# 
# A second trivial function takes a text string and returns an all-caps version. 

# In[135]:


def scream(text):
    text_upper = text.upper()
    return text_upper


# In[136]:


scream('Hi there!')


# The `text` and `text_upper` variable only exist within the function. That means that you can pass a variable not called `text` to the function.

# In[137]:


text_upper


# It is a good idea to include a comment within the function that explains the function. This is helpful for other people reading your code and when you return to your own code months and days later.

# In[140]:


def scream(text):
    '''Returns an all-caps version of text string.'''
    text_upper = text.upper()
    return text_upper


# ### Functions Exercise 1
# 
# 
# Make a function called "whisper" that replaces all exclamation marks with a period and returns a lower case version of a string. Test it out.

# In[141]:


#Your answer here.

def whisper(text):
    ''''''
    
    return quiet_text


# In[142]:


def whisper(text):
    '''Lower case string and replace
       ! with .'''
    quiet_text = text.replace('!','.')
    quiet_text = quiet_text.lower()
    return quiet_text

#Testing it out: 
whisper('ASDFASDFAS!')


# Congratulations! You've now been introduced to the basics of Python for social scientists.
