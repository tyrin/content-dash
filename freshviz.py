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
	mergeframe = pd.merge(rightframe, leftframe, how="outer", on=column)
	return(mergeframe)

def main():
# select viz
	viztype = st.sidebar.radio(
		"Select a visualization",
		('Freshness and Views', 'Freshness'))

#Caching data functions
	@st.cache_data 	
	def load_data(url):
		df = pd.read_csv(url)
		return df

	@st.cache_data 	
	def load_data_delimiter(url):
		df = pd.read_csv(url, sep=',', thousands=',')
		return df
 # Add histogram data
	ldf = load_data("https://raw.githubusercontent.com/tyrin/content-dash/master/data/freshdata3.csv")
	ldv = load_data_delimiter("https://raw.githubusercontent.com/tyrin/content-dash/master/data/ViewsByTopic4Freshness.csv")

	@st.cache_data
	def transform(df):
		if 'Date' in df.columns:
			df['Date'] = df['Date'].astype('datetime64')
		df['Topic ID'] = df['Topic ID'].astype(str)
		df = df.fillna(value='0')
		return df
	df = transform(ldf)
	dv = transform(ldv)

	
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
		dff = df.loc[df['Portal'].isin(portal)]
		dfs = dff.sort_values(by='Group')
		group = dfs['Group'].unique()
		domain = st.sidebar.multiselect('Content Domain:', group)
		dfff = df.loc[df['Portal'].isin(portal)]
		fd = dfff.filter(items=['Date', 'Node'])
	if (len(portal) > 0) and (len(domain) > 0):
# if you've selected a portal and domain then create a data frame limited to that
		dfff = df.loc[(df['Portal'].isin(portal)) & (df['Group'].isin(domain))]
#create new data frame that's only date and node for the visualization
		fd = dfff.filter(items=['Date', 'Node'])
		#st.write(portal)
		colname = "Topic ID"
#combine the view data and the freshness data by filling the full values 
		#st.dataframe(dfff)
		#st.dataframe(dv)
		if 'help' in portal or 'workbook' in portal: 
			dvf = dfff.merge(dv, how='inner', on='Topic ID')
			#st.write("inside help loop")
		else:
			dfc = df.combine_first(dv)
			dvf = dfc.loc[(dfc['Portal'].isin(portal)) & (dfc['Group'].isin(domain))]
			#st.write("inside else loop")
		if viztype == "Freshness":
			freshbars(fd, portal, dfff)
			#minvalue = fd["Date"].min()
			#maxvalue = fd["Date"].max()
			#daterange = st.slider("Select a date range", value=[minvalue, maxvalue])
		if viztype == "Freshness and Views":
			#st.write ("In Beta")
			freshviews(dvf, portal)
# create a bar graph for freshness alone--------------------------------------------------
def freshbars(fd, portal, dfff):
	fig, ax = plt.subplots(figsize=(7,3))
	fd["Date"].astype(np.int64).plot.hist(ax=ax)
	
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
