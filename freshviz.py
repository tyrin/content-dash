#plotly distribution plot
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import os
import sys
import plotly.express as px
from dateutil.parser import parse

def convert_df(frame):
   return frame.to_csv().encode('utf-8')
   
def mergeframes(leftframe, rightframe, column):#---merges two tables based on the  column
	#mergeframe = pd.merge(leftframe, rightframe, on=["Username"])
	mergeframe = pd.merge(rightframe, leftframe, how="outer", on=column)
	#st.write(mergeframe.shape)
	return(mergeframe)

def main():
# select viz
	viztype = st.sidebar.radio(
		"Select a visualization",
		('Freshness and Views', 'Freshness'))
# Add histogram data
	df = pd.read_csv("https://raw.githubusercontent.com/tyrin/content-dash/master/data/freshdata3.csv")
	dv = pd.read_csv("https://raw.githubusercontent.com/tyrin/content-dash/master/data/ViewsByTopic4Freshness.csv", sep=',', thousands=',')
	df['Date'] = df['Date'].astype('datetime64')
	#Set the topic ID column as string
	df['Topic ID'] = df['Topic ID'].astype(str)
	dv['Topic ID'] = dv['Topic ID'].astype(str)

	#Fill in all naan values with zero
	df = df.fillna(value='0')
	dv = dv.fillna(value='0')
	
#define variables that the customer will input--------------------------------------------

	sitelist= df['Portal'].unique()
	#Identify any lines with nan values
	dfna = df[df.isna().any(axis=1)]
	#st.dataframe(dfna)
	site = np.sort(sitelist)
	domain=""
	portal=""
	portal = st.sidebar.multiselect(
	'Portal:', site)
	message = st.empty()
	if len(portal) == 0:
		message.text("Select a portal")

	if (len(portal) > 0) and (len(domain) == 0):
		message = st.empty()
		#df[df['country'] == country]
		dff = df.loc[df['Portal'].isin(portal)]
		dfs = dff.sort_values(by='Group')
		group = dfs['Group'].unique()
		domain = st.sidebar.multiselect('Content Domain:', group)
		dfff = df.loc[df['Portal'].isin(portal)]
		fd = dfff.filter(items=['Date', 'Node'])
		#fd['Date'] = fd['Date'].astype('datetime64[ns]')
		#fd['Date'] = fd['Date'].astype('datetime64')
	if (len(portal) > 0) and (len(domain) > 0):
		#message.text("Filter by date")
		dfff = df.loc[(df['Portal'].isin(portal)) & (df['Group'].isin(domain))]
		fd = dfff.filter(items=['Date', 'Node'])
		#fd['Date'] = fd['Date'].astype('datetime64')
#Using the below  causes an error in the streamlit dataframe call even though it should format the dates better, so I have to use the above.
#fd['Date']= pd.to_datetime(df['Date'])
		
		colname = "Topic ID"
		#vf = mergeframes(dfff, dv, colname)
		dfc = df.combine_first(dv)
		dvf = dfc.loc[(dfc['Portal'].isin(portal)) & (dfc['Group'].isin(domain))]
		#dv = dv.fillna(value='0')

		if viztype == "Freshness":
			freshbars(fd, portal, dfff)
		if viztype == "Freshness and Views":
			#st.write ("In Beta")
			freshviews(dvf, portal)
# create a bar graph for freshness alone--------------------------------------------------
def freshbars(fd, portal, dfff):
	fig, ax = plt.subplots(figsize=(7,3))
	fd["Date"].astype(np.int64).plot.hist(ax=ax)
	#Creating side bar so it reflect current data
	#min_value = fd.index.min()
	#start_time = st.sidebar.slider(
 	#	"When do you start?",
 	#	value=fd.index.min(),
 	#	format="MM/DD/YY - hh:mm")
	#st.sidebar.write("Start time:", fd.index.min())


	ax.set_ylabel('# of Files')
	labels = ax.get_xticks().tolist()
	labels = pd.to_datetime(labels)
	ax.set_xticks(ax.get_xticks())  # just get and reset whatever you already have
	ax.set_xticklabels(labels, rotation=90)
	#ax.legend()

	st.pyplot(fig, use_container_width=True)
	st.dataframe(dfff)

	if len(portal) != 0:
		csv = convert_df(dfff)
		st.download_button(
		   "Press to Download",
		   csv,
		   "freshness.csv",
		   "text/csv",
		   key='download-csv'
		)
def freshviews(dvf, portal):
	st.write("Prioritize Content for Maintenance")

	#--------- Figure

	fig = px.scatter(dvf, x="Date", y="Views",
		text="Topic ID",
		log_x=False,
		#error_x_minus="Date",
		size='Secs',
		color='Views',
		size_max=15
		)
#
	#	#fig.update_traces(textposition='top center')
	fig.update_traces(mode="markers")
	##fig.update_xaxes(tickformat="%Y %b %e")
	fig.update_layout(
		height=800,
		title_text='Last Changed Date and Number of Views'
	)
#
	#fig.write_html("scatter.html")
	#HtmlFile = open("scatter.html", 'r', encoding='utf-8')
	#source_code = HtmlFile.read()
	#components.html(source_code, height = 700,width=900)
	#freshtypes = dvf.dtypes
	#st.write(freshtypes)
	
	st.plotly_chart(fig, use_container_width=True)
	st.dataframe(dvf)
	def convert_df(dvf):
	   return dvf.to_csv().encode('utf-8')

	csv = convert_df(dvf)

	st.download_button(
	   "Press to Download",
	   csv,
	   "file.csv",
	   "text/csv",
	   key='download-csv'
	)

#--------
