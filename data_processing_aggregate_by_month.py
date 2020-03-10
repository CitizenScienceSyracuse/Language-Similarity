
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords 
import re 

import pickle    # this package is used for store the data we have generated in different steps
                 # if there is something goes wrong in any step, we can import the data from .pkl file and redo it 



df1 = pd.read_csv(r'C:\Users\...\gravityspy_prep2.csv')

# this step imports the stopword list from NLTK 
english_stopword = stopwords.words('english')


# read the file mallet.txt and import the words in this file as stopword
with open(r'C:\Users\wangtao\Documents\summer_intern_gravity spy\code for the project\mallet.txt','r')as f:
    stopword = f.read().split('\n')
    
    # the word in the list ["zero","example","novel","help","none","above","q"] should be excluded from the stopword list  
    a = ["zero","example","novel","help","none","above","q"] 
    
    # add in NLTK stopwords to the mallet stopword
    stopword.extend(english_stopword)
    
    # exclude the stopwords in list "a"
    stopword_list = [x for x in stopword if x not in a]


## As we checked the data above, the number of users who commended from 2016-03 to 2018-02 is 1448 
## the next analysing is depend on the users from gravityspy_prep2 
## split part of the table from gravityspy_prep2 and create a new table which contains user_login, user_id, comment_time and comments

df3 = df1[['comment_user_login','comment_user_id','comment_created_at','filtered_words']].copy()

# This step is filtering the commas in the original string
df3['filter_comma'] = df3['filtered_words'].apply(lambda x: str(x).replace( "[\\pP+~$`^=|<>～｀＄＾＋＝｜＜＞￥×]" , ""))

# This step is tokenizing the unigrams in the previous filtered data now the string is made into list
df3['split']=df3['filter_comma'].apply(lambda x: nltk.word_tokenize(str(x))) 

# This step is made the list back to string data for next processing 
# so each user's filtered_words data is a string of unigrams
df3['filtered_words2'] = df3['split'].apply(lambda x :' '.join([w for w in x if w not in stopword_list]))

# drop the columns we do not need  
df3 = df3.drop(['split','filtered_words','filter_comma'],axis=1)



## Build the funtion of generating the data for each months
## in this step the month data is not aggregated by month
## so the tables we generate contains only one month's data

# this is the string pattern we are going to use to seperate the original table df3 by month
list_of_date = ['2016\-03\-','2016\-04\-','2016\-05\-','2016\-06\-','2016\-07\-','2016\-08\-','2016\-09\-',
                '2016\-09\-','2016\-10\-','2016\-11\-','2016\-12\-','2017\-01\-','2017\-02\-','2017\-03\-',
                '2017\-04\-','2017\-05\-','2017\-06\-','2017\-08\-','2017\-09\-','2017\-09\-','2017\-10\-',
                '2017\-11\-','2017\-12-','2018\-01\-','2018\-02\-']

## Here is the function of generating table for each months. we collect each user's comment in every moths in the list
## using groupby method in pandas to summarizing each user's comment every month, the output is a list that contain's each month's data

def month_collection(df3,list_of_date,list_of_tables = None):
    list_of_tables = []
    n = 0
    for string in list_of_date:
        month = df3['comment_created_at'].str.contains(string)
        table = df3[month].copy()
        table1 = table.groupby(['comment_user_login','comment_user_id'])['filtered_words2'].apply(' '.join).reset_index()
        n +=1
        table1['month'] = str(n)  # add in new column to identify the number of month
        list_of_tables.append(table1)
    return list_of_tables
    



tables = month_collection(df3,list_of_date)



## For our research, the data of every month should be aggragated 
## For example, the data of the second month should contails two-months' data which are data of"2016-03"and "2016-04" 
## in this step we aggregate data by month 

## Here is the function of generating monthly data 
## x is the number of months
def append_tables(x,tables):
    n=0 
    if x==1:
        ntable = tables[0]  
    else:
        ntable = tables[0]
        while n<x-1:
            n+=1
            ntable = ntable.append(tables[n])
            if n>len(tables):
                break
    return ntable


## Generate a list of monthly data

months = []
for i in range (1,25):
    d = append_tables(i,tables)
    d = d.groupby(['comment_user_id','comment_user_login'])['filtered_words2'].apply(''.join).reset_index()
    months.append(d)


# store the result in .pkl file
output = open ("months.pkl","wb")
pickle.dump(months, output)


# test the data we pickled to see whether it is stored rightly
months_pkl = open('months.pkl', 'rb')
months1 = pickle.load(months_pkl)

# check the data of the second month
months1[1].head()
