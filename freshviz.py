#plotly distribution plot
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import os
import sys
import plotly.express as px

def convert_df(frame):
   return frame.to_csv().encode('utf-8')
   
def mergeframes(leftframe, rightframe, column):#---merges two tables based on the  column
	#mergeframe = pd.merge(leftframe, rightframe, on=["Username"])
	mergeframe = pd.merge(rightframe, leftframe, how="outer", on=column)
	st.write(mergeframe.shape)
	return(mergeframe)
   
def main():
# Add histogram data
	df = pd.read_csv("https://raw.githubusercontent.com/tyrin/content-dash/master/data/freshdata3.csv")
	dv = pd.read_csv("https://raw.githubusercontent.com/tyrin/content-dash/master/data/ViewsByTopic4Freshness.csv")
	
#define variables that the customer will input--------------------------------------------
	#Identify any lines with nan values. Use to test if you get weird bugs with a new data file.
	#dfna = df[df.isna().any(axis=1)]
	#st.dataframe(dfna)
	dfnb = dv[df.isna().any(axis=1)]
	st.dataframe(dfnb)
	sitelist= df['Portal'].unique()
	#Identify any lines with nan values
	dfna = df[df.isna().any(axis=1)]
	#st.dataframe(dfna)
	#site = np.ndarray.sort(sitelist)
	site = sitelist
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
		fd['Date'] = fd['Date'].astype('datetime64')
	if (len(portal) > 0) and (len(domain) > 0):
		#message.text("Filter by date")
		dfff = df.loc[(df['Portal'].isin(portal)) & (df['Group'].isin(domain))]
		fd = dfff.filter(items=['Date', 'Node'])
		fd['Date'] = fd['Date'].astype('datetime64')
#Using the below  causes an error in the streamlit dataframe call even though it should format the dates better, so I have to use the above.
#fd['Date']= pd.to_datetime(df['Date'])
		st.write("Merged Dataframes")
		colname = "Topic ID"
		vf = mergeframes(dfff, dv, colname)
		st.dataframe(vf)
# create a bar graph for freshness alone--------------------------------------------------

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
#---------
# Data type conversions
# my data is datetime64[ns, tzlocal()]
#df['created_at'] = df['created_at'].astype('datetime64[ns]')
#df['user_type'] = df['user_type'].astype('category')
#
## Show new data types
#df.dtypes


#--------
