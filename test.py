#plotly distribution plot
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import numpy as np
import pandas as pd

def main():
# Add  data
	df = pd.read_csv('/Users/tavery/content-dash/data/DataCloudDevDocAnalysis2.csv')
	#de.columns = de.columns.str.replace(' ', '_')
	#df = de.transpose()
	st.dataframe (df)
	#cols = df.columns.values.tolist()
	#label = df.iloc[0]
	#Remove the first column
	#labels = label[1:]
	#st.write (label)
	
	#df.reset_index(drop=True)
	#df = df.reset_index('Competitor', drop=True)
	#df.columns = df.columns.str.replace(' ', '_')
	dtypes = df.infer_objects().dtypes
	#st.write (dtypes)
	#df.columns.name = "Competitor"
	#fig = px.bar(df, x=df.index, y=label, title="Data Cloud Dev Doc Competitive Analysis")
	#fig = px.bar(df, x="Feature", y=labels, title="Data Cloud Dev Doc Competitive Analysis")
	df = df.set_index('Competitor')
	fig = px.bar(df, title="Data Cloud Dev Doc Competitive Analysis", color_discrete_sequence=px.colors.qualitative.Prism)
	fig2 = px.imshow(df, title="Data Cloud Dev Doc Competitive Analysis", text_auto=True, color_continuous_scale="PiYG")
	#fig3 = px.bar_polar(df, r="Competitor", theta="direction",
   	#               color="Competitor", template="plotly_dark",
   	#               color_discrete_sequence= px.colors.sequential.Plasma_r)
	st.plotly_chart(fig, use_container_width=True)
	st.plotly_chart(fig2, use_container_width=True)
	
	