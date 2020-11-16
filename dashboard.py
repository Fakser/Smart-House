import streamlit as st
import pandas as pd
import numpy as np
from requests import get
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
from controller import api_token
import io


st.title("Smart house data Dashboard")
st.markdown('Dashboard that visualize the situation in smart house')
st.sidebar.title("Visualization Selector")

st.sidebar.markdown("Select the Charts/Plots accordingly:")
select_viz = st.sidebar.selectbox('Vizualization of: ', ['Data', 'ML Models'], key='0')
if select_viz == 'Data':
    data = get('http://localhost:5000/data/8000/{}'.format(api_token)).json()
    data_dfs = {key: pd.DataFrame(data[key]) for key in list(dict(data).keys())}
    select_table = st.sidebar.selectbox('Table: ', list(dict(data).keys()), key='1')
    select_column = st.sidebar.selectbox('Column: ', data_dfs[select_table].columns[1:], key='3')
    
    st.markdown('Linear plot')
    fig1 = px.line(data_dfs[select_table], x='date', y=select_column)
    st.plotly_chart(fig1)
    st.markdown('Histogram')
    fig2 = px.histogram(data_dfs[select_table], x = select_column)
    st.plotly_chart(fig2)
elif select_viz == 'ML Models':
    models_names = get('http://localhost:5000/rules/{}'.format(api_token)).json()
    select_model = st.sidebar.selectbox('Model: ', list(models_names), key='2')
    model_json = get('http://localhost:5000/rules/{}/{}'.format(select_model, api_token)).json()
    
    img = Image.open(io.BytesIO(bytes(model_json['model_graph'].encode('ISO-8859-1'))))
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    st.image(buffer)