#run from app.py this has additional data for Keyword By Portal and search volume across portals. However, is not working.
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import plotly.express as px

#KEYWORD FILTERING----------------------------------------------

def filterterm(df, scatterterm, scattersearch):
	if scatterterm == 'no':
		dff = df
		message = st.empty()
		#Identify any lines with nan values
		dfna = df[df.isna().any(axis=1)]
		#message.text("Enter your search and select a visualization")
		#st.dataframe(dfna)
	elif scatterterm != 'no' and scattersearch=='term':
		st.write ("Search for the term " + scatterterm + " as a Keyword ")
		message = st.empty()
		dff = df.loc[(df['Keyword'].str.contains(scatterterm, na=False))]
		# changing the Volume column from text to numeric so we can sort and use a color scale
		#add a new column with the text for hover
		dff['CustomerSearch'] = df['Keyword'] + "<br>Page: " + df['Page']
		#st.dataframe(dff)
		#dff['Volume'] = pd.to_numeric(dff['Volume'])
	elif scatterterm != 'no' and scattersearch=='page':
		st.write ("Search for the term" + scatterterm + " in the page path.")
		message = st.empty()
		dff = df.loc[(df['Page'].str.contains(scatterterm, na=False))]
		#add a new column with the text for hover
		dff['CustomerSearch'] = df['Keyword'] + "<br>Page: " + df['Page']
		#st.dataframe(dff)
	else:
		dff = df.loc[(df['Keyword'].str.contains(scatterterm))]
		dff['CustomerSearch'] = df['Keyword'] + "<br>Page: " + df['Page']
	# if the term has no results, tell them and use the full data frame
	return dff

def matscatterplot3(scatterterm, scattersearch):
	if len(scatterterm) == 0:
		scatterterm = 'no'
#GRAPH WITHOUT LABELS----------------------------------------------
	scattertype = st.sidebar.radio(
		"Select a Visualization",
		('Blended Rank', 'Blended Rank Change', 'Keyword By Portal'))
# Note Plotly express can't be included directly in streamlit, you have to render it as an html page and then read it in
# the same way you do with networkx visualizations.

	plt.style.use('seaborn-whitegrid')
#upload main data for blended rank and blended rank change viz
	dfck = pd.read_csv("https://raw.githubusercontent.com/tyrin/content-dash/master/data/combinedKeywords.csv")
	dfbr = pd.read_csv("https://raw.githubusercontent.com/tyrin/content-dash/master/data/TotalOrganicKeywords-Jan2021vsJan2022.csv")
		
	if scattertype == "Keyword By Portal":
		dff = filterterm(dfck, scatterterm, scattersearch)
	else:
		dff = filterterm(dfbr, scatterterm, scattersearch)
	termresults = "yes"
	#before they've entered a keyword
	if scatterterm == "no" and scattertype == "Keyword By Portal":
		#st.dataframe(dfck)
		termresults = "no"
	if scatterterm == "no" and scattertype != "Keyword By Portal":
		#st.dataframe(dfbr)
		termresults = "no"
	#If they've put in a search string but didn't find any results
	elif dff.isnull().values.any() and scatterterm != "no":
		st.write("No results for your term. Check the data below to find a valid keyword.")
		if scattertype == "Keyword By Portal":
			st.dataframe(dfck)
		elif scattertype != "Keyword By Portal":
			st.dataframe(dfbr)
		termresults = "no"
	#If they've put in a search string to search and found results
	elif scatterterm != "no" or termresults !="no":
		#st.write("Your term is " + scatterterm)
		if scattertype == "Blended Rank":
			fig = px.scatter(dff, x="Blended Rank", y="Search Volume",
				text="CustomerSearch",
				log_x=True,
				size="Blended Rank",
				color="Blended Rank",
				size_max=25)
			#fig.update_traces(textposition='top center')
			fig.update_traces(mode="markers")
			fig.update_layout(
		    	height=800,
		    	title_text='Blended Rank and Search Volume'
			)

		elif scattertype == "Blended Rank Change":
			fig = px.scatter(dff, x="Blended Rank Change", y="Search Volume",
				text="CustomerSearch",
				log_x=False,
				error_x_minus="Blended Rank Change",
				size="Blended Rank",
				color="Blended Rank",
				size_max=25)

				#fig.update_traces(textposition='top center')
			fig.update_traces(mode="markers")
			fig.update_layout(
				height=800,
				title_text='Blended Rank Change and Search Volume'
			)
		elif scattertype == "Keyword By Portal":
			fig = px.bar(dff, x="Keyword", y=dff['Volume'], color="Portal", title="Keyword By Portals")
			fig.update_layout(
				height=800, width=1000
			)
			#Other variations of representation
			#fig = px.bar(dff, x="Keyword", y=dff['Volume'].astype(int), color=dff['Volume'].astype(int), title="Keyword By Portals")
			#fig = px.bar(df1, x=df1.time, y=df2.market, color=df1.sales)

	#if scatterterm != "no" or termresults !="no"
		fig.write_html("scatter.html")
		HtmlFile = open("scatter.html", 'r', encoding='utf-8')
		source_code = HtmlFile.read()
		components.html(source_code, height = 700,width=900)
		st.dataframe(dff)
		
		def convert_df(dff):
		   return dff.to_csv().encode('utf-8')

		csv = convert_df(dff)

		st.download_button(
		   "Press to Download",
		   csv,
		   "file.csv",
		   "text/csv",
		   key='download-csv'
		)
def noresults(df):
	st.dataframe(df)
	return df
	#fig2.write_html("scatter.html")
