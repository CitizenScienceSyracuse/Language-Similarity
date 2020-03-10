
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import pickle 

# import the data we have generated from "aggregated data by month" which is named as "months.pkl" file
#  months is a list of nonthly data tables which we are going to do further processing

months_pkl = open('months.pkl', 'rb')
months = pickle.load(months_pkl)


# this fuction creates a list of comments which excepet the inidvidual user we are going to compair.
# then we merge the list into one string and made it into a modified community corpus for each user.
# each user's commnuity corpus is a single string which is the collection of strings joined with white space

def corpus(month_all_comments,x,l=None):
    com_corpus = [i for i in month_all_comments if i not in x]
    return ' '.join(com_corpus)
    

# generate the new tables of the 1st to 6th month
monthly_data = []
for month in months[0:6]:
    comments = month['filtered_words2']
    month['community_corpus'] = month['filtered_words2'].apply(lambda x: corpus(comments,x))
    monthly_data.append(month)


# generate the new tables of the 7th to 12th month
for month in months[6:12]:
    comments = month['filtered_words2']
    month['community_corpus'] = month['filtered_words2'].apply(lambda x: corpus(comments,x))
    monthly_data.append(month)



# check the result of 12th month
monthly_data[11].head()

# store the result of 12 months
output4 = open('monthly_data12.pkl','wb')
pickle.dump(monthly_data,output4)


# generate tables of the 13th to 18th month
monthly_data2 = []
for month in months[12:18]:
    comments = month['filtered_words2']
    month['community_corpus'] = month['filtered_words2'].apply(lambda x: corpus(comments,x))
    monthly_data2.append(month)


# stored the result in  .pkl file
output5 = open('monthly_data13_to_18.pkl','wb')
pickle.dump(monthly_data2,output5)

 
#############################################################################################################

# memorry error campe up when processing the 19th month data
# 19th, 20th, 21st, 22nd, 23rd, 24th they all have the same problem because of the size

m19 = months[18]
comments = m19['filtered_words2']
m19['community_corpus'] = m19['filtered_words2'].apply(lambda x: corpus(comments,x))
    monthly_data2.append(month)


# generate the rest of the last 6 months (month19 to month24)

monthly_data3 = []
for month in months[18::]:
    comments = month['filtered_words2']
    month['community_corpus'] = month['filtered_words2'].apply(lambda x: corpus(comments,x))
    monthly_data3.append(month)

# save result to .pkl file
output6 = open('monthly_data19_to_24.pkl','wb')
pickle.dump(monthly_data,output6)
