import re
import os
import nltk
import string
import random
import base64
import requests
import numpy as np
import tweepy as tw
import pandas as pd
import datetime as DT
from PIL import Image
import streamlit as st
from nltk.tag import pos_tag
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
#from wordcloud import WordCloud, STOPWORDS
#from wordcloud import get_single_color_func

url = "http://127.0.0.1:5000/"

st.markdown('<style>body{background-color:powderblue;}</style>',unsafe_allow_html=True)

st.sidebar.header("Sentiment Analysis😷🔬")
ch = st.sidebar.selectbox(
    "Choice",
    [
        "Home",
        "Certificate Generator",
        "Gallery"
    ],
    key="main_select",
    )

if ch == "Home":
	a = "Certificate Generator😷🔬"
	st.title(a)

	a = '<p style="text-align: justify;font-size:20px;">Certificate Generator is the system which will be used to generate certificates '
	a+='automatically, just by uploading a csv file and the template for the certificate.'
	a+='We will be using tesseract and OCR for identifying blank spaces, then we will fill in the spaces with the input given<br><br>'
	a+='by the user. We will also br providing a few templates which can be directly used to generate certificates.'
	a+=' </p><br>'

	st.markdown(a,unsafe_allow_html=True)

	a ="<p style='text-align: justify;font-size:20px;'>This project gives its users the knowledge of the world's reactions on any given topic.<br><br>"
	a+=" <b>Features</b><ul><li style='text-align: justify;font-size:20px;'>Interactive Dashboard to Analyze the Data</li><li style='text-align: justify;font-size:20px;'>Real Time data scraping from twitter</li>"
	a+="<li style='text-align: justify;font-size:20px;'>File upload Option to Analyze data of different Source</li><li style='text-align: justify;font-size:20px;'>Classification / Sentiment Analysis of data in Positive and Negative sentiment</li>"
	a+="<li style='text-align: justify;font-size:20px;'>Various analytical visualization of data such as Daily count, Daily Positive count and Daily Negative count plot</li>"
	a+="<li style='text-align: justify;font-size:20px;'>Word Cloud plot for word level analysis</li><li style='text-align: justify;font-size:20px;'>Sentiment Cloud plot for Analysis of Positive and Negative words</li>"
	a+="<li style='text-align: justify;font-size:20px;'>Download option to save scapeed tweets.</li></ul></p>"

	st.markdown(a,unsafe_allow_html=True)

	a = "<p style='text-align: justify;font-size:20px;'>Please choose sentiment Analysis Tool from the sidebar to proceed.</p>"
	st.markdown(a,unsafe_allow_html=True)

elif ch=="Sentiment Analysis Tool":
	a = "Sentiment Analysis Tool!! 😷🔬"
	st.title(a)
	a = '<p style="text-allign: justify; font-size: 20px;">Enter the hashtag you want the analysis on or select a csv file.</p>'
	st.markdown(a,unsafe_allow_html=True)
	a = '<p style="font-size: 30px;">Instructions for uploading CSV file:</p>'
	a+='<ol><li>File should have 2 columns named <b>text</b> and <b>timestamp</b></li>'
	a+='<li>The text column will contain the tweets.</li><li>The text column will contain the date of the text</li>'
	a+='<li>The format of timestamp should be "Day Month Date"</li>Eg: Tue Oct 18</ol>'
	st.markdown(a,unsafe_allow_html=True)

	uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv",encoding="ISO-8859-1")
	if uploaded_file is not None:
		DATASET_ENCODING = "ISO-8859-1"
		tweet = pd.read_csv(uploaded_file)
		b = tweet.columns
		if 'text' in b:
			if 'timestamp' in b:
				tweet = predict(tweet)
				z = visualize(tweet)
				wordcloudplot(tweet)
				#st.markdown(get_table_download_link(tweet), unsafe_allow_html=True)
				if st.sidebar.button('Download Data as CSV',key='csv'):
					tweet.to_csv (r'twwets.csv', index = False, header=True)
			else:
				st.markdown('<h2>The uploaded file does not adhere to the instructions.<h2>',unsafe_allow_html=True)
		else:
			st.markdown('<h2>The uploaded file does not adhere to the instructions.<h2>',unsafe_allow_html=True)

	h = st.sidebar.text_input(label ='Enter hashtag')
	if len(h)>0:
		if h[0]!='#':
			h = '#'+h
		tweet = get_tweets(h)

		if st.sidebar.button('Download Data as CSV',key='tweet'):
			tweet.to_csv (r'twwets.csv', index = False, header=True)
		tweet = predict(tweet)
		z = visualize(tweet)
		wordcloudplot(tweet)

else:
	a = "Some sample results of our Sentiment Analysis Tool"
	st.title(a)
	st.sidebar.markdown("Choose a file for results")
	b = st.sidebar.selectbox("Choice",
		["Iphone11 tweets","Oneplus7 tweets"],
		key="select",
		)
	if b=="Iphone11 tweets":
		tweet = pd.read_csv('./Gallery/iphone.csv',encoding="ISO-8859-1")
		a=list(tweet['Prediction'])
		pos=[]
		neg=[]
		i=0
		for j in range(len(tweet)):
			if tweet['Prediction'][j]=='positive':
				pos.append(tweet['hashtag'][j][:75])
				i+=1
				if i==3:
					break
		i=0
		for j in range(len(tweet)):
			if tweet['Prediction'][j]=='negative':
				neg.append(tweet['hashtag'][j][:75])
				i+=1
				if i==3:
					break
		st.markdown('<h3>Sample Predicted results</h3>',unsafe_allow_html=True)
		if len(pos)>=3 and len(neg)>=3:
			a ='<table><tr><th>Tweet</th><th>Sentiment</th></tr>'
			a+='<tr><td>{}</td><td>positive</td></tr>'.format(pos[0])
			a+='<tr><td>{}</td><td>positive</td></tr>'.format(pos[1])
			a+='<tr><td>{}</td><td>positive</td></tr>'.format(pos[2])
			a+='<tr><td>{}</td><td>negative</td></tr>'.format(neg[0])
			a+='<tr><td>{}</td><td>negative</td></tr>'.format(neg[1])
			a+='<tr><td>{}</td><td>negative</td></tr></table><br>'.format(neg[2])
			st.markdown('<style>table{background-color:white;}</style>',unsafe_allow_html=True)
			st.markdown(a,unsafe_allow_html=True)
		image = Image.open('./Gallery/iphonedaywise.png')
		st.image(image, use_column_width=True)
		image1 = Image.open('./Gallery/iphonetweet.png')
		st.image(image1, use_column_width=True)
		st.markdown('<h3>Word Cloud</h3>',unsafe_allow_html=True)
		image2 = Image.open('./Gallery/iphonewc1.png')
		st.image(image2, use_column_width=True)
		c = st.selectbox('Choice',['Sentiment WordCloud','Positive Sentiment WordCloud','Negative Sentiment WordCloud'],key="main_select")
		if c=="Sentiment WordCloud":
			st.markdown('<h3>Sentiment Word Cloud</h3>',unsafe_allow_html=True)
			image3 = Image.open('./Gallery/iphonesent.png')
			st.image(image3,use_column_width=True)
		elif c=="Positive Sentiment WordCloud":
			st.markdown('<h3>Sentiment Word Cloud : Positive</h3>',unsafe_allow_html=True)
			image3 = Image.open('./Gallery/iphonepositive.png')
			st.image(image3,use_column_width=True)
		else:
			st.markdown('<h3>Sentiment Word Cloud : Negative</h3>',unsafe_allow_html=True)
			image3 = Image.open('./Gallery/iphoneneg.png')
			st.image(image3,use_column_width=True)
	if b=="Oneplus7 tweets":
		tweet = pd.read_csv('./Gallery/oneplus.csv',encoding="ISO-8859-1")
		a=list(tweet['Prediction'])
		pos=[]
		neg=[]
		i=0
		for j in range(len(tweet)):
			if tweet['Prediction'][j]=='positive':
				pos.append(tweet['hashtag'][j][:50])
				i+=1
				if i==3:
					break
		i=0
		for j in range(len(tweet)):
			if tweet['Prediction'][j]=='negative':
				neg.append(tweet['hashtag'][j][:50])
				i+=1
				if i==3:
					break
		st.markdown('<h3>Sample Predicted results</h3>',unsafe_allow_html=True)
		if len(pos)>=3 and len(neg)>=3:
			a ='<table><tr><th>Tweet</th><th>Sentiment</th></tr>'
			a+='<tr><td>{}</td><td>positive</td></tr>'.format(pos[0])
			a+='<tr><td>{}</td><td>positive</td></tr>'.format(pos[1])
			a+='<tr><td>{}</td><td>positive</td></tr>'.format(pos[2])
			a+='<tr><td>{}</td><td>negative</td></tr>'.format(neg[0])
			a+='<tr><td>{}</td><td>negative</td></tr>'.format(neg[1])
			a+='<tr><td>{}</td><td>negative</td></tr></table><br>'.format(neg[2])
			st.markdown('<style>table{background-color:white;}</style>',unsafe_allow_html=True)
			st.markdown(a,unsafe_allow_html=True)
		image = Image.open('./Gallery/oneplusdaywise.png')
		st.image(image, use_column_width=True)
		image1 = Image.open('./Gallery/oneplustweet.png')
		st.image(image1, use_column_width=True)
		st.markdown('<h3>Word Cloud</h3>',unsafe_allow_html=True)
		image2 = Image.open('./Gallery/onepluswc.png')
		st.image(image2, use_column_width=True)
		c = st.selectbox('Choice',['Sentiment WordCloud','Positive Sentiment WordCloud','Negative Sentiment WordCloud'],key="main")
		if c=="Sentiment WordCloud":
			st.markdown('<h3>Sentiment Word Cloud</h3>',unsafe_allow_html=True)
			image3 = Image.open('./Gallery/oneplussent.png')
			st.image(image3,use_column_width=True)
		elif c=="Positive Sentiment WordCloud":
			st.markdown('<h3>Sentiment Word Cloud : Positive</h3>',unsafe_allow_html=True)
			image3 = Image.open('./Gallery/onepluspositive.png')
			st.image(image3,use_column_width=True)
		else:
			st.markdown('<h3>Sentiment Word Cloud : Negative</h3>',unsafe_allow_html=True)
			image3 = Image.open('./Gallery/oneplusneg.png')
			st.image(image3,use_column_width=True)
