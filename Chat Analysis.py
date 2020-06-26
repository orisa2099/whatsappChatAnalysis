# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 22:51:07 2020

@author: ISE-OLUWA
"""
from PIL import Image
import re
import pandas as pd
import emoji
import matplotlib.pyplot as plt
import seaborn as sns

#whatsapp text
dataset = open(r'./discn futbal.txt', mode ='r', encoding = 'utf8').read()

#data cleaning and sorting
#for general regex pattern of the whole dataset
pattern = re.compile('\d+/\d+/\d+,\s\d+:\d+\s-.*:.*')
messgset = re.findall(pattern, dataset)

listed2 = '\n'.join(messgset)

#regrex for messages
pattern3 = re.compile(":\s+.*")
message = re.findall(pattern3, listed2)
messages = [y.replace(':', '') for y in message]

#regrex for time
pattern2 = re.compile('\d+:\d+\s+-')
time1 = re.findall(pattern2, listed2)
time = [y.replace('-', '') for y in time1]

#regrex for names ("-.*:")
pattern = re.compile('\d+:\d+\s+-\s+([a-zA-Z0-9]+\s?[a-zA-Z0-9]+\s?[a-zA-Z0-9]+\s?):\s+')
names = re.findall(pattern,dataset)

#regrex for date
pattern1 = re.compile('\d+/\d+/\d+')
date = re.findall(pattern1, listed2)

#moving to dataframe
df = pd.DataFrame()
df["date"] = date
df["time"] = time
df["names"] = names
df["messages"] = messages

#letter count
df["Letter_Count"]=df['messages'].apply(lambda w: len(w.replace(' ','')))

#word count
df["Word_Count"]=df['messages'].apply(lambda w: len(w.split(' ')))

#average word lenght 
df['Avg_Word_length']=df['Letter_Count']//df["Word_Count"]

#exporting df should in case you want to do analysis with tableau
df.to_csv('Discusn futbal new.csv', index=False, encoding='utf-8')

#importing df
df = pd.read_csv('Discusn futbal new.csv', index_col=None)

#converting date and time to timsstamp
df['DateTime']=pd.to_datetime(df['date']+ ' '+ df["time"], dayfirst=True) 
#section end

#indexing with the timestamp, 
df.index=df['DateTime']
#section end

#number of messages sent by each group member
number_of_messages_per_person = df.names.value_counts()
plt.figure(figsize=[15,5])
plt.xlabel('Group Members')
plt.ylabel('No. of Messages')
number_of_messages_per_person.plot.bar(figsize=[15,5], color={'r','g','b','y'})
plt.xticks(rotation=90)
plt.title('Activity of all group members')
plt.show()
#section end

#top 10 most active memeber of the group
number_of_messages_per_person = df.names.value_counts().head(10)
plt.figure(figsize=[15,5])
plt.xlabel('Group Members')
plt.ylabel('No. of Messages')
number_of_messages_per_person.plot.bar(figsize=[15,5], color={'r','g','b','y'})
plt.xticks(rotation=90)
plt.title('top 10 most active memeber of the group')
plt.show()
#section end

#top 10 least active member of the group
number_of_messages_per_person = df.names.value_counts().tail(10)
plt.figure(figsize=[15,5])
plt.xlabel('Group Members')
plt.ylabel('No. of Messages')
number_of_messages_per_person.plot.bar(figsize=[15,5], color={'r','g','b','y'})
plt.xticks(rotation=90)
plt.title('top 10 most active memeber of the group')
plt.show()
#section end

df[['hour',"minute"]] = df.time.str.split(':', expand=True).astype('int64')
hour = df['time'].apply(lambda x: x.split(':')[0])
df['hour'] = hour
#top 5 active hours of the day
top_5_active_hours_of_the_day = df.hour.value_counts().head()
plt.figure
plt.xlabel('Hour of the Day')
plt.ylabel('No. of Messages')
top_5_active_hours_of_the_day.plot.bar(color={'r','g','b','y'})
plt.xticks(rotation=90)
plt.title('top 5 active hours of the day')
plt.show()
#section end

#least 5 active hours of the day
least_5_active_hours_of_the_day = df.hour.value_counts().tail()
plt.figure
plt.xlabel('Hour of the Day')
plt.ylabel('No. of Messages')
top_5_active_hours_of_the_day.plot.bar(color={'r','g','b','y'})
plt.xticks(rotation=90)
plt.title('least 5 active hours of the day')
plt.show()
#section end

#messages at night
messages_at_night = df[df['hour']<6]
who_sends_messages_at_night = messages_at_night.names.value_counts().head()
plt.figure()
plt.xlabel('Group Members')
plt.ylabel('No. of Messages')
who_sends_messages_at_night.plot.bar(color={'r','g','b','y'})
plt.xticks(rotation=90)
plt.title('messages at night')
plt.show()
#to get the people always sleeping early just change the head to tail in the messages at nigh section
#section end

#top 10 active days of the group
top_10_active_days_of_the_group = df['date'].value_counts().head(10).plot.bar(color={'r','g','b','y'})
plt.title('top 10 active days of the group')
plt.xlabel('no. of messages')
plt.ylabel('dates')
#just as above change the head to tail to get the least active days of the group
#section end

#active hours of the on 24/02/2020
A_hours = df[df['date'] == '24/02/2020']
plt.figure()
plt.xlabel('Hour of the Day')
plt.ylabel('No. of Messages')
active_hours_of_24022020 = A_hours.hour.value_counts().head().plot.bar(color={'r','g','b','y'})
plt.xticks(rotation=90)
plt.title('active hours of the on 24/02/2020')
plt.show()
#most active members on 24/02/2020
plt.figure()
plt.xlabel('Group members')
plt.ylabel('No. of Messages')
active_hours_of_24022020 = A_hours.names.value_counts().head().plot.bar(color={'r','g','b','y'})
plt.xticks(rotation=90)
plt.title('most active members on 24/02/2020')
plt.show()
#section end

#who sends most media messages in the group
media_message_df = df[df['messages'] == ' <Media omitted>']
sender_media_value_counts = media_message_df['names'].value_counts()
top_10_sender_media_value_counts = sender_media_value_counts.head(10) 
top_10_sender_media_value_counts.plot.bar(color={'r','g','b','y'})
plt.title('who sends most media')
plt.xlabel('names')
plt.ylabel('no. of media posted')
#section end

#top 10 group members who deletes messages the most
messages_deleted_df = df[df['messages'] == ' This message was deleted']
sender_messages_deleted_value_counts = messages_deleted_df['names'].value_counts()
top_10_sender_messages_deleted_value_counts = sender_messages_deleted_value_counts.head(10) 
top_10_sender_messages_deleted_value_counts.plot.bar(color={'r','g','b','y'})
plt.title('who deletes messages the most')
plt.xlabel('names')
plt.ylabel('no. of deleted messages')
#section end

#letter and word count
max_word_count = df[df['Word_Count']==df['Word_Count'].max()]
top_5_letter_typing_guys = df.sort_values(by=['Letter_Count'],ascending=False).head(5)
top_5_word_typing_guys = df.sort_values(by=['Word_Count'],ascending=False)
top_5_word_typing_guys.plot.bar(top_5_word_typing_guys['Word_Count'], top_5_word_typing_guys['names'])
plt.title('top_5_word_typing_guys')
plt.xlabel('no. of words,letters')
plt.ylabel('names')
#section end

#top 5 longest messages sent and thier sender 
top_5_word_typing_guys = df.sort_values(by=['Word_Count'],ascending=False).head(5)
long_msg = top_5_word_typing_guys [['names', 'Word_Count']]
plt.figure()
sns.barplot(x='names', y='Word_Count', hue ="names", data = long_msg)
plt.title('top 5 longest messages sent and thier sender')
plt.show()
#frequency of occurence of each longest sentences
longest_sentences_frequency1 = df['Word_Count'].value_counts().head(20).plot.bar()
longest_sentences_frequency1 = df['Word_Count'].value_counts().tail(20).plot.bar()
#section end

word_count=df[['names','Letter_Count','Word_Count','Avg_Word_length']]
word_count.index=word_count['names']

#top 5 people who has sent the longest messages with highest number of characters in a single message in the group
word_count.sort_values(by=['Letter_Count'],ascending=False).head(5).plot.bar()
plt.title('top 5 highest number of characters in a single message')
plt.xlabel('Names')
plt.ylabel('No of character')
#top 5 people who has sent the longest messages with highest number of characters all through the chat timeline in the group
word_count2=df[['names','Letter_Count','Word_Count','Avg_Word_length']]
word_count2.groupby(df["names"]).sum().sort_values(by=['Letter_Count'],ascending=False ).head(5).plot.bar(figsize=[15,5])
plt.title('top 5 highest number of characters all through and their sender')
plt.xlabel('Names')
plt.show()
#who send long messages on an average 
word_count2=df[['names','Letter_Count','Word_Count','Avg_Word_length']]
word_count2.groupby(df["names"]).mean().sort_values(by=['Letter_Count'],ascending=False ).head(5).plot.bar(figsize=[15,5])
plt.title('top 5 highest number of characters and their sender on an average')
plt.xlabel('Names')
plt.show()
#section end

#splitting date to get out disntc year
year = df['date'].apply(lambda x: x.split('/')[2])
df['year'] =year
#section end

#number of messages in 2019 and 2020
plt.figure()
plt.xlabel('Year')
plt.ylabel('No.ofMessages')
df.index.year.value_counts().plot.bar(color={'r','b'})
plt.title('Number of Messages Sent in 2019 and 2020')
plt.show()
#splitingthedatasetinto2019and2020groups 
date2019=df[df.index.year==2019]
date2020=df[df.index.year==2020]
date2020.describe()
#top 10 days wth high activities in 2019
top_10_active_days_of_the_group_in_2019 = date2019['date'].value_counts().head(10).plot.bar(color={'r','g','b','y'})
plt.title('top 10 days wth activities in 2019')
plt.xlabel('no. of messages')
plt.ylabel('dates')
#top 10 days wth high activities in 2020
top_10_active_days_of_the_group_in_2020 = date2020['date'].value_counts().head(10).plot.bar(color={'r','g','b','y'})
plt.title('top 10 days wth activities in 2020')
plt.xlabel('no. of messages')
plt.ylabel('dates')
#top 10 days wth least activities in 2019
top_10_active_days_of_the_group_in_2019 = date2019['date'].value_counts().tail(10).plot.bar(color={'r','g','b','y'})
plt.title('top 10 days wth activities in 2019')
plt.xlabel('no. of messages')
plt.ylabel('dates')
#top 10 days wth activities in 2020
top_10_active_days_of_the_group_in_2020 = date2020['date'].value_counts().tail(10).plot.bar(color={'r','g','b','y'})
plt.title('top 10 days wth activities in 2020')
plt.xlabel('no. of messages')
plt.ylabel('dates')
#section end

#creatin month df
month = df['date'].apply(lambda x: x.split('/')[1])
df['month'] =month

#Ccomparing activity between 2019 and 2020
a =dateG2019.groupby(dateG2019.index.month)["messages"].count().plot.line(color={'b'})
a1 =dateG2020.groupby(dateG2020.index.month)["messages"].count().plot.line(color={'r'})
plt.title('LineGraphCmparingTheActivityIntheGroupfor2019and2020')
plt.xlabel('Months of the year')
plt.ylabel('Number of Messages')
plt.show()
#
dateG2019.groupby(dateG2019.index.month).sum().plot.line()
dateG2020.groupby(dateG2020.index.month).sum().plot.line()
plt.title('LineGraphCmparingTheActivityIntheGroupfor2019and2020')
plt.xlabel('no.ofmessages')
plt.ylabel('Monthsoftheyear')
plt.show()

#most used words in the group
def gen_text(col):
    col=col.dropna()
    txt="".join(message for message in col)
    txt=re.sub('.....omitted','',txt)
    return txt
 
text2019=gen_text(date2019['messages'])
text2020=gen_text(date2020['messages'])

from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
stopwords=set(STOPWORDS)
wordcloud19=WordCloud(max_font_size=50,max_words=100,background_color="white",stopwords=stopwords).generate(text=text2019)
wordcloud20=WordCloud(max_font_size=50,max_words=100,background_color="white",stopwords=stopwords).generate(text=text2020)

#most used word in 2019
plt.figure(figsize=[15,5])
plt.imshow(wordcloud19,interpolation='bilinear')
plt.axis("off")
plt.show()
#most used word in 2020
plt.figure(figsize=[15,5])
plt.imshow(wordcloud20,interpolation='bilinear')
plt.axis("off")
plt.show()
#section end

#emoji analysis
#opening original raw data before cleaning and sorting
dataset = open(r'./discn futbal.txt', mode ='r', encoding = 'utf8').read()


pattern = re.compile('\d+:\d+\s+-\s+([a-zA-Z0-9]+\s?[a-zA-Z0-9]+\s?[a-zA-Z0-9]+\s?):\s+')
messengers = re.findall(pattern,dataset)
messengers


# emoji count
count_messages={}
for each in messengers:
    if each in count_messages.keys():
        count_messages[each]+=1
    else:
        count_messages[each]=1
count_messages

messages_split = pattern.split(dataset)
messages_split[9:11]

sep_msgs=[]
for each in count_messages.keys():
    for msg in range(len(messages_split)):
        if each == messages_split[msg]:
            sep_msgs.append(messages_split[msg+1])   #obtaining the message mentioned after sender along with dates
print(len(sep_msgs))   
sep_msgs[7]


cleaned_sep_msg = []
for each in sep_msgs:
    if '\n0' in each:
        cleaned_sep_msg.append(each.split('\n0'))
    elif '\n1' in each:
        cleaned_sep_msg.append(each.split('\n1'))
    elif '\n2' in each:
        cleaned_sep_msg.append(each.split('\n2'))
    elif '\n3' in each:
        cleaned_sep_msg.append(each.split('\n3'))
my_msg = []
for each in cleaned_sep_msg:
    my_msg.append(each[0])
print(len(my_msg))
my_msg[7]

who_sent_what = []
prev = 0
for each in count_messages.keys():
    num = count_messages[each]
    
    nex = num+prev
    messages = my_msg[prev:nex]
    who_sent_what.append(messages)
    prev = nex
who_sent_what
my_df=pd.DataFrame(who_sent_what)
my_df = my_df.transpose()
my_df.columns = [list(count_messages.keys())[0],list(count_messages.keys())[1],list(count_messages.keys())[2],list(count_messages.keys())[3],
                 list(count_messages.keys())[4],list(count_messages.keys())[5],list(count_messages.keys())[6],list(count_messages.keys())[7],
                 list(count_messages.keys())[8],list(count_messages.keys())[9],list(count_messages.keys())[10],list(count_messages.keys())[11],
                 list(count_messages.keys())[12],list(count_messages.keys())[13],list(count_messages.keys())[14],
                 list(count_messages.keys())[15],list(count_messages.keys())[16],list(count_messages.keys())[17],
                 list(count_messages.keys())[18],list(count_messages.keys())[19],list(count_messages.keys())[20],
                 list(count_messages.keys())[21],list(count_messages.keys())[22]]

def extract_emojis(columnname):
    emojis=[]
    for string in my_df[columnname]:
        my_str = str(string)
        for each in my_str:
            if each in emoji.UNICODE_EMOJI:
                emojis.append(each)
    return emojis


#top 10 emoji used
emoji_dict={}
for keys in count_messages.keys():
    keys
    emoji_dict[keys] = extract_emojis(keys)
    emoji_df = pd.DataFrame(emoji_dict[keys])
    emj_count = pd.DataFrame(emoji_df[0].value_counts()[:10])
    emj_count.plot.bar()   #top 10 common emoji used
    plt.title('top 10 common emoji used')
    plt.xlabel('emojis')
    plt.ylabel('emoji_count')
    plt.savefig('top 10 common emoji used', dpi = 500)
    

#top 5 emoji used per person    
emoji_dict={}
for keys in count_messages.keys():
    print(keys)
    emoji_dict[keys] = extract_emojis(keys)
    emoji_df = pd.DataFrame(emoji_dict[keys])
    print(emoji_df[0].value_counts()[:5])
    
#who uses highest number emojis
data = pd.read_excel('emojicount.xlsx')
data.to_csv('data.csv')
data = pd.read_csv('data.csv')
#so basically i just created an excel file and plotted a bar chat from the excel file .....lol 
#the emoji analysis was just done not with much understanding would appreciate if it can be worked on














