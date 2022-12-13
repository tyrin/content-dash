#plotly distribution plot
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import pandas as pd

def mergeframes(leftframe, rightframe, column):#---merges two tables based on the Topic ID column
	#mergeframe = pd.merge(leftframe, rightframe, on=["Topic ID"])
	mergeframe = pd.merge(rightframe, leftframe, how="outer", on=column)
#	st.write(mergeframe.shape)
def main():
# Add freshness histogram data
	df = pd.read_csv("https://raw.githubusercontent.com/tyrin/content-dash/master/data/freshdata2.csv")
# Add page view data for scatterplot
	dg = pd.read_csv("https://raw.githubusercontent.com/tyrin/content-dash-dash/master/data/freshdata2.csv")
#define variables that the customer will input
	sitelist= df['Portal'].unique()
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
		dfr = dfff.filter(items=['Date', 'Node'])
		#dfr['Date'] = dfr['Date'].astype('datetime64[ns]')
		dfr['Date'] = dfr['Date'].astype('datetime64')
	if (len(portal) > 0) and (len(domain) > 0):
		#message.text("Filter by date")
		dfff = df.loc[(df['Portal'].isin(portal)) & (df['Group'].isin(domain))]
		dfr = dfff.filter(items=['Date', 'Node'])
		dfr['Date'] = dfr['Date'].astype('datetime64')
#Using the below  causes an error in the streamlit dataframe call even though it should format the dates better, so I have to use the above.
#fd['Date']= pd.to_datetime(df['Date'])
		fd = 
		fig, ax = plt.subplots(figsize=(7,3))
		dfr["Date"].astype(np.int64).plot.hist(ax=ax)
		#Creating side bar so it reflect current data
		#min_value = dfr.index.min()
		#start_time = st.sidebar.slider(
     	#	"When do you start?",
     	#	value=dfr.index.min(),
     	#	format="MM/DD/YY - hh:mm")
		#st.sidebar.write("Start time:", dfr.index.min())

		labels = ax.get_xticks().tolist()
		ax.set_ylabel('# of Files')
		labels = pd.to_datetime(labels)
		ax.set_xticklabels(labels, rotation=90)
		#ax.legend()

		st.pyplot(fig, use_container_width=True)
		st.dataframe(dfr)
	@st.cache
	def convert_df(dfr):
	   return dff.to_csv().encode('utf-8')
	if len(portal) != 0:
		csv = convert_df(dfr)

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
