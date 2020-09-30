import streamlit as st
import pandas as pd
import numpy as np
from requests import get
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from controller import api_token


data = get('http://localhost:5000/data/6000/{}'.format(api_token)).json()
data_dfs = {key: pd.DataFrame(data[key]) for key in list(dict(data).keys())}
st.title("Smart house data Dashboard")
st.markdown('The dashboard will visualize the situation in smart house')
st.sidebar.title("Visualization Selector")
st.sidebar.markdown("Select the Charts/Plots accordingly:")
select_table = st.sidebar.selectbox('Table: ', list(dict(data).keys()), key='1')
#if not st.sidebar.checkbox("Hide", True, key='1'):
select_column = st.sidebar.selectbox('Column: ', data_dfs[select_table].columns[1:], key='3')
#if not st.sidebar.checkbox("Hide", True, key='4'):
select_chart = st.sidebar.selectbox('Chart type: ', ['linear', 'histogram'], key='5')
if select_chart == 'linear':
    fig = px.line(data_dfs[select_table], x=0, y=select_column)
else:
    fig = px.histogram(data_dfs[select_table], x = select_column)
st.plotly_chart(fig)
