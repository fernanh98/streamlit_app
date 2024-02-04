import streamlit as st
import pandas as pd
import numpy as np
from plotnine import *
import folium
from streamlit_folium import st_folium, folium_static
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from plotnine import *
from app_functions import *

# Leemos y preparamos los datos
accomodations = pd.read_csv('accomodations.csv')

# Creamos un DataFrame con las medias y cuentas de las variables agrupadas por cada estado de USA
grouped_states = accomodations.groupby('state').agg(
    price=('price', 'mean'),
    num_comments=('num_comments', 'mean'),
    rating=('rating', 'mean'),
    wifi=('wifi', 'sum'),
    gym=('gym', 'sum'),
    swimming_pool=('swimming_pool', 'sum'),
    breakfast=('breakfast_included', 'sum'),
    count=('state', 'count')
)

# Puntuación que obtiene de media los alojamientos en cada estado por cada 100€ que cuesta
grouped_states['rating_price'] = round(grouped_states['rating'] / grouped_states['price'] * 100, 1)

# Porcentajes de servicios que se ofrecen en los alojamientos de cada estado
grouped_states['prop_gym'] = round(grouped_states['gym'] / grouped_states['count'] * 100, 1)
grouped_states['prop_breakfast'] = round(grouped_states['breakfast'] / grouped_states['count'] * 100, 1)
grouped_states['prop_swimming_pool'] = round(grouped_states['swimming_pool'] / grouped_states['count'] * 100, 1)
grouped_states['prop_wifi'] = round(grouped_states['wifi'] / grouped_states['count'] * 100, 1)
grouped_states = grouped_states.sort_values('price', ascending = False).reset_index()



# Configuramos nuestra página
st.set_page_config(page_title='Vacaciones en USA')

st.sidebar.header('Análisis de alojamientos en USA')


menu = st.sidebar.radio(
    'Elije',
    ('Análisis Precio y Calidad', 'Precio y Puntuación', 'Mapas'),
)

if menu == 'Análisis Precio y Calidad':
    set_analysis(grouped_states)
elif menu == 'Precio y Puntuación':
    set_distributions(accomodations)
elif menu == 'Mapas':
    set_map(accomodations, grouped_states)
    
    
    

