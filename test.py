import streamlit as st
import pandas as pd
import numpy as np
import numpy as np
import plotly.express as px


def main():
		df = pd.read_csv('/Users/tavery/content-dash/data/teststc1.csv')
		st.dataframe(df)
		fig = px.bar(df, title="Monthly Total",x= 'Month',y = 'Views')
		st.plotly_chart(fig, use_container_width=True)