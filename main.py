import json
import requests
import nltk
import streamlit as st
import pandas as pd
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
from pprint import pprint
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

# COP4813
# Jeffrey N. Tjokroredjo
# 09/30/2020


st.title("COP4813 - Web Application Programming")
st.title("Project 1")
st.write("Part A - The Stories API")
st.write("This app uses the Top Stories API to display the most common"
         "words used in the top current articles based on a specified topic"
         "selected by the user. The data is displayed as a line chart and"
         "as a wordcloud.")
st.title("I - Topic Selection")

# st.write("Please enter your name:")

user_input = st.text_input("Please enter your name:")
option = st.selectbox(
    "Select a topic of your interest",
    ("arts","automobiles","books","business","fashion",
     "science","food","health","movies","sports","technology","theater",
     "travel")
)

if st.checkbox("Click here for additional info:"):
    st.write("Hi " + user_input + ", you have selected the " + option + " topic." )

api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]

url = "https://api.nytimes.com/svc/topstories/v2/"+option+".json?api-key=" + api_key

response = requests.get(url).json()

main_functions.save_to_file(response, "JSON_Files/response.json")

my_articles = main_functions.read_from_file("JSON_Files/response.json")

str1 = ""

for i in my_articles["results"]:
    str1 = str1 + i["abstract"]

words = word_tokenize(str1)

words_no_punc = []
for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())

fdist2 = FreqDist(words_no_punc)

stopwords = stopwords.words("english")

clean_words=[]

for x in words_no_punc:
    if x not in stopwords:
        clean_words.append(x)

pprint(len(clean_words))

fdist3 = FreqDist(clean_words)

st.title("II - Frequency Distribution")

if st.checkbox("Click here to display a frequency distribution graph"):
    most_common = pd.DataFrame(fdist3.most_common((10)))
    df = pd.DataFrame({"topic": most_common[0],"count":most_common[1]})
    fig = px.line(df, x="topic", y="count",title="Your selected topic: " + option + "!")
    st.plotly_chart(fig)

st.title("III - Wordcloud")
if st.checkbox("Click here to generate wordcloud:"):
    st.write("Here is your wordcloud:")
    wordcloud = WordCloud().generate(str1)
    plt.imshow(wordcloud, interpolation='bilinear')

    plt.axis("off")
    plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

st.title("Part B - Most Popular Articles")
st.write("Select if you want to see the most shared, emailed or viewed articles.")

option2 = st.selectbox(
    "Select your preferred set of articles:",
    ["shared","emailed","viewed"]
)

option3 = st.selectbox(
    "Select the period of time(last days)",
    ["1", "7", "30"]
)

top_url = "https://api.nytimes.com/svc/mostpopular/v2/"+option2+"/"+option3+".json?api-key=" + api_key

response = requests.get(top_url).json()

main_functions.save_to_file(response, "JSON_Files/response2.json")

my_articles1 = main_functions.read_from_file("JSON_Files/response2.json")
str2 = ""

for i in my_articles1["results"]:
    str2 = str2 + i["abstract"]

if st.checkbox("Click here for your wordcloud:"):
    wordcloud1 = WordCloud().generate(str2)
    plt.figure()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.imshow(wordcloud1)
    plt.axis("off")
    plt.show()
    st.pyplot()













