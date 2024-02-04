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

# Diccionario de estados y su identificador para relacionar mi base de datos con el geojson de USA
# al crear un mapa de choropleth
state_codes = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI',
    'Wyoming': 'WY'
}


def plot_state_bar(data, column, title, y_label, y_range, second_axis=False, sec_column=None, sec_y_label=None, sec_range=None):
    
    '''
    Crea un gráfico de barras con los estados de USA en función de una variable column. 
    Tiene la opción de añadir otra variable al eje y de la derecha
    '''
    
    def get_order_categorical(df, column):
        '''
        Extrae los estados de USA ordenados en función de una variable (column)
        '''
        values = df.sort_values(column, ascending=False)['state'].to_list()
        return values
    
    fig = px.bar(data, x='state', y=column, title=title,
                 labels={column: y_label},
                 category_orders={'state': get_order_categorical(data, 'price')})
    
    fig.update_xaxes(showticklabels=False, visible=False)
    fig.update_traces(marker_color='#ff5f75', customdata=data[sec_column])
    fig.update_layout(legend=dict(orientation="h", y=1.2, x=0.55))
    #fig.update_xaxes(showticklabels=True, title_text='Estado', title_standoff=20)
    fig.update_yaxes(title_text=y_label)
    
    if second_axis:
        # Añadimos información al popup para que se vea como queramos
        custom_data_sec = data[sec_column] if sec_column in data.columns else None
        fig.add_trace(go.Scatter(x=data['state'], y=data[sec_column], mode='lines+markers',
                             yaxis='y2', name=sec_y_label, line=dict(color='#0e0565'), customdata=custom_data_sec))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right', range=sec_range, title_text=sec_y_label))
    
    # Configuración del popup
    hovertemplate = f"<b>Estado</b>: %{{x}}<br><b>{y_label}</b>: %{{y}}<br>"
    if second_axis:
        hovertemplate += f"<b>{sec_y_label}</b>: %{{customdata}}<extra></extra>"
    else:
        hovertemplate += "<extra></extra>"

    fig.update_traces(hovertemplate=hovertemplate)
    
    return fig


def set_analysis(data):
    '''
    Crea 4 gráficos de barras y los muestra con un expander.
    '''
    
    plots = {
    'Plot 1': plot_state_bar(data=data, 
                   column='price', 
                   title='Relación precio calidad', y_label='Precio medio (€)',
                   y_range = [0, max(data['price'])+500],
                   second_axis = True, sec_y_label='Puntuación obtenida por cada 100€',
                   sec_column='rating_price', sec_range = [0, max(data['rating_price'] + 0.5)]),
    
    'Plot 2': plot_state_bar(data=data, 
                   column='price', 
                   title='Relación precio y servicio de gimnasio', y_label='Precio medio (€)',
                   y_range = [0, max(data['price'])+500],
                   second_axis = True, sec_y_label='% Alojamientos con gimnasio',
                   sec_column='prop_gym', sec_range = [0, 100]),
    
    'Plot 3': plot_state_bar(data=data, 
                   column='price', 
                   title='Relación precio y servicio de desayuno', y_label='Precio medio (€)',
                   y_range = [0, max(data['price'])+500],
                   second_axis = True, sec_y_label='% Alojamientos con desayuno',
                   sec_column='prop_breakfast', sec_range = [0, 100]),
    
    'Plot 4': plot_state_bar(data=data, 
                   column='price', 
                   title='Relación precio y servicio de piscina', y_label='Precio medio (€)',
                   y_range = [0, max(data['price'])+500],
                   second_axis = True, sec_y_label='% Alojamientos con piscina',
                   sec_column='prop_swimming_pool', sec_range = [0, 100])
    }
    

    st.header('Comparación del precio de los alojamientos y sus servicios')
    st.write('En los gráficos siguientes se muestran los estados de USA ordenados según\
             el precio medio de sus alojamientos. Además, se incluye información sobre\
                 la puntuación y la cantidad de servicios que ofrece.')
    with st.expander('Gráfico relación precio calidad'):
        st.plotly_chart(plots['Plot 1'])
    with st.expander('Gráfico relación precio y porcentaje de gimnasios'):
        st.plotly_chart(plots['Plot 2'])
    with st.expander('Gráfico relación precio y porcentaje de servicios de desayuno'):
        st.plotly_chart(plots['Plot 3'])
    with st.expander('Gráfico relación precio y porcentaje de piscinas'):
        st.plotly_chart(plots['Plot 4'])
    st.write('Como se observa en los gráficos, en USA un alojamiento más barato\
             no implica que la calidad sea peor. De hecho, resulta curioso que aquellos\
                 estados con alojamientos más baratos, son los que ofrecen mayor\
                     cantidad de servicios (gimnasio, piscina y desayuno incluido).')
    


def set_distributions(df):
    
    '''
    Crea histogramas de Precio y Puntuación con un selector para elegir de qué estado de USA mostrar la información.
    '''
    # Creamos una lista con cada estado de USA y una opcion de 'Todos'
    states_list = ['Todos']
    states_list.extend(list(df['state'].unique()))
    st.header('Distribución de precios y puntuación')
    st.write('A continuación se muestran los histogramas de precios y puntuación\
             por estado. La línea azul muestra la mediana de la variable.')
    state_select = st.selectbox('Estado', states_list)
    sub_data = df.loc[df['state'] == state_select]
    col1, col2 = st.columns(2)
    col1.write('Distribución de precios')
    col2.write('Distribución de puntuación')
    
    def calculate_bin(df, column):
        '''
        Calcula la anchura que debería tener el bin al representar el histograma
        según la Regla de Freedman-Diaconis
        '''
        # Calculamos rango intercuartilico
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        
        # Regla de Freedman-Diaconis
        n = len(df)
        bin_width = 2 * iqr * (n**(-1/3))
        return bin_width
    
    if state_select == 'Todos':
        with col1:
            p = ggplot(df, aes(x='price'))\
                + geom_histogram(binwidth=200, fill='#ff5f75')\
                + geom_vline(xintercept=df['price'].median(), linetype='dashed', color='#0e0565')\
                + labs(x='Precio (€)', y='')
            st.pyplot(ggplot.draw(p))
        with col2:
            p = ggplot(df.dropna(subset='rating'), aes(x='rating'))\
                + geom_histogram(binwidth=0.4, fill='#ff5f75')\
                + geom_vline(xintercept=df.dropna(subset='rating')['rating'].median(), linetype='dashed', color='#0e0565')\
                + labs(x='Puntuación', y='')
            st.pyplot(ggplot.draw(p))
    else:
        with col1:
            price_bin = calculate_bin(sub_data, 'price')
            p = ggplot(sub_data, aes(x='price'))\
                + geom_histogram(binwidth=price_bin, fill='#ff5f75')\
                + geom_vline(xintercept=sub_data['price'].median(), linetype='dashed', color='#0e0565')\
                + labs(x='Precio (€)', y='')
            st.pyplot(ggplot.draw(p))
        with col2:
            rating_bin = calculate_bin(sub_data.dropna(subset='rating'), 'rating')
            p = ggplot(sub_data.dropna(subset='rating'), aes(x='rating'))\
                + geom_histogram(binwidth=rating_bin, fill='#ff5f75')\
                + geom_vline(xintercept=sub_data.dropna(subset='rating')['rating'].median(), linetype='dashed', color='#0e0565')\
                + labs(x='Puntuación', y='')
            st.pyplot(ggplot.draw(p))



def set_map(df1, df2):
    
    '''
    Crea dos mapas distintos y un selector para elegir qué mapa visualizar
    '''
    def get_geojson_us(df, state_codes=state_codes):
        
        '''
        Descarga un geojson de los estados de USA y le añade informacion de Precio y Puntuación por estado
        '''
        
        geo_json_data = requests.get(
            "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
        ).json()
        
        # Pasamos el json a dataframe y le añadimos informacion de precio y puntuacion
        df_geo = pd.json_normalize(geo_json_data["features"])
        df_geo = df_geo.merge(df[['state','price','rating']], how="left", left_on="properties.name", right_on='state')
        
        # Renombramos columnas para que en el Popup aparezca como queremos
        alias_columns = {"price": "Precio", "rating": "Puntuacion", 'state':'Estado'}
        df_geo.rename(columns=alias_columns, inplace=True)
        
        # Volvemos a pasar a json con la estructura que tenía
        feature_collection = {'type': 'FeatureCollection', 'features': []}
        
        # Iteramos sobre las filas del DataFrame y agregamos cada Feature al diccionario
        for _, row in df_geo.iterrows():
            feature = {
                'type': row['type'],
                'id': row['id'],
                'properties': {
                    'name': row['properties.name'],
                    'Estado': row['Estado'],
                    'Precio': row['Precio'],
                    'Puntuacion': row['Puntuacion']
                },
                'geometry': {
                    'type': row['geometry.type'],
                    'coordinates': row['geometry.coordinates']
                }
            }
            feature_collection['features'].append(feature)
        
        # Ya podemos convertir el diccionario a un json
        json_result = json.dumps(feature_collection, indent=2)
        return json_result
    
    def plot_price_distribution(df):
        
        '''
        Crea un mapa con el precio medio de los alojamientos en USA por estado
        '''
        us_states_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
        price_map = folium.Map(location=[48, -102], zoom_start=3, 
                               tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                               attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                               )
        df['state_id'] = df['state'].map(state_codes)

        choropleth = folium.Choropleth(
            geo_data=us_states_url,
            name='choropleth',
            data=df,
            columns=['state_id', 'price'],
            key_on='feature.id',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Precio medio del alojamiento (€)'
        ).add_to(price_map)
        
        # Añadimos popup 
        popup = folium.GeoJsonPopup(fields=["Estado",'Precio','Puntuacion'])
        us_geojson_data = get_geojson_us(df) # Función definida abajo
        folium.GeoJson(
            us_geojson_data,
            popup=popup,
            style_function = lambda x: {
                'fillColor': 'transparent',
                'color': 'transparent',
            }
        ).add_to(price_map)
        folium_static(price_map)
        
    def plot_density_map(df):
        
        '''
        Crea un mapa de densidad de puntos para visualizar los alojamientos en USA
        '''
        
        col1, col2 = st.columns([11, 4])
        
        with col2:
            st.write('Filtro')
            wifi_filter = st.checkbox('Con wifi')
            gym_filter = st.checkbox('Con gimnasio')
            pool_filter = st.checkbox('Con piscina')
            breakfast_filter = st.checkbox('Con desayuno')
            price_selector = st.selectbox('', ['Rango completo de precios', 'Rango de precios acotado'])
            
            if price_selector == 'Rango completo de precios':
                min_price, max_price = st.slider('Rango de precios', int(df['price'].min()), int(df['price'].max()), (int(df['price'].min()), int(df['price'].max())))
            else:
                min_price, max_price = st.slider('Rango de precios', int(df['price'].min()), 1000, (int(df['price'].min()), 1000))
        
        filtered_data = df
        
        if wifi_filter:
            filtered_data = filtered_data[filtered_data['wifi'] == True]  
        
        if gym_filter:
            filtered_data = filtered_data[filtered_data['gym'] == True]
        
        if pool_filter:
            filtered_data = filtered_data[filtered_data['swimming_pool'] == True]
        
        if breakfast_filter:
            filtered_data = filtered_data[filtered_data['breakfast_included'] == True]
        
        # Aplicar filtro por rango de precios
        filtered_data = filtered_data[(filtered_data['price'] >= min_price) & (filtered_data['price'] <= max_price)]
        
        data = filtered_data[['lat', 'lon']]
        col2.write(f'{data.shape[0]} alojamientos')
            
        with col1:
            st.map(data, color='#ff5f75', size=10)
        
        st.subheader('Enlaces de los alojamientos')
        if filtered_data.shape[0] >= 1000:
            st.write('Cuando haya menos de 1000 alojamientos se verán sus enlaces')
        if filtered_data.shape[0] < 1000:
            with st.container():
                # Convertimos los enlaces a HTML con formato de hipervínculo azul y prefijo
                links_html = '<br>'.join([f'<b>Alojamiento {index + 1}:</b> <a href="{link}" target="_blank" style="color: blue;">{link}</a>' for index, link in enumerate(filtered_data['accomodation_link'])])
            
                # Mostramos los enlaces en un contenedor con desplazamiento
                st.markdown(f'<div style="height:300px; overflow-y: scroll;">{links_html}</div>', unsafe_allow_html=True)
    
    st.header('Mapas de alojamientos')
    map_selection = st.selectbox(
        'Elije un mapa',
        ['Mapa de densidad de puntos',
         'Distribución de precio por estado'])

    if map_selection == 'Mapa de densidad de puntos':
        st.write('Aplica los filtros para ver los lugares con mayor densidad de ofertas de alojamientos según varios criterios.')
        plot_density_map(df1)

    elif map_selection == 'Distribución de precio por estado':
        st.write('Pincha en cada estado para ver su información.')
        plot_price_distribution(df2)
        st.write('Se puede observar como las zonas Este y Noroeste tienen de media unos precios más elevados.')
        
