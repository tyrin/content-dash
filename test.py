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
	dw = pd.read_csv('/Users/tavery/content-dash/data/DevDocAnalysisWeighted.csv')
	dw2 = pd.read_csv('/Users/tavery/content-dash/data/DevDocAnalysisWeighted2.csv')
	#de.columns = de.columns.str.replace(' ', '_')
	#df = de.transpose()
	#st.dataframe (df)
	#cols = df.columns.values.tolist()
	#label = df.iloc[0]
	#Remove the first column
	#labels = label[1:]
	#st.write (label)
	
	#df.reset_index(drop=True)
	#df = df.reset_index('Competitor', drop=True)
	#df.columns = df.columns.str.replace(' ', '_')
	#dtypes = df.infer_objects().dtypes
	#st.write (dtypes)
	#df.columns.name = "Competitor"
	#fig = px.bar(df, x=df.index, y=label, title="Data Cloud Dev Doc Competitive Analysis")
	#fig = px.bar(df, x="Feature", y=labels, title="Data Cloud Dev Doc Competitive Analysis")
	df = df.set_index('Competitor')
	fig = px.bar(df, title="Data Cloud Dev Doc Competitive Analysis", color_discrete_sequence=px.colors.qualitative.Prism)
	fig2 = px.imshow(df, title="Data Cloud Dev Doc Competitive Analysis", text_auto=True, color_continuous_scale="PiYG")
	fig2.layout.height = 500
	fig2.layout.width = 800
	fig2.update_layout(
    	font=dict(
        	family="Arial",
        	size=18,  # Set the font size here
        	color="black"
    	)
	)
	#fig3 = px.bar_polar(df, r="Competitor", theta="direction",
   	#               color="Competitor", template="plotly_dark",
   	#               color_discrete_sequence= px.colors.sequential.Plasma_r)
	st.plotly_chart(fig, use_container_width=True)
	st.plotly_chart(fig2, use_container_width=True)
	
	dw = dw.set_index('Feature')
	figw = px.bar(dw, title="Data Cloud Dev Doc Competitive Analysis by Feature", color_discrete_sequence=px.colors.qualitative.Vivid)	
	fig2w = px.imshow(dw, title="Data Cloud Dev Doc Competitive Heatmap by Feature", text_auto=True, color_continuous_scale="PiYG")
	st.plotly_chart(figw, use_container_width=True)
	st.plotly_chart(fig2w, use_container_width=True)
	
	st.dataframe (dw2)
	dw2 = dw2.set_index('Competitor')
	figw2 = px.bar(dw2, title="Data Cloud Dev Doc Weighted Competitive Analysis", color_discrete_sequence=px.colors.qualitative.Prism)
	fig2w2 = px.imshow(dw, title="Data Cloud Dev Doc Weighted Heatmap", text_auto=True, color_continuous_scale="PiYG")
	fig2w3 = px.imshow(dw, title="Test", text_auto=True, color_continuous_scale="PiYG")
	fig2w3.layout.height = 800
	fig2w3.layout.width = 800
	fig2w3.update_layout(
    	font=dict(family="Arial", size=18, color='black')
	)

	st.plotly_chart(figw2, use_container_width=True)
	st.plotly_chart(fig2w2, use_container_width=True)
	st.plotly_chart(fig2w3)