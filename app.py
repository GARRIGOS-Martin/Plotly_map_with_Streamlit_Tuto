import pandas as pd
import streamlit as st
import plotly.express as px
import json
from urllib.request import urlopen

# On charge les données 

df = pd.read_csv('./data/data_tuto_streamlit.csv', sep = ';')
with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as f : 
    geo_dep = json.load(f)

# On ???
state_id_map = {}
for feature in geo_dep['features']:
 feature['id'] = feature['properties']['code']
 state_id_map[feature['properties']['nom']] = feature['id']


st.title('Tuto Streamlit')

list_indicateurs = list(df.columns[2:])
indicateur = st.sidebar.selectbox("Selectionner un indicateur :", list_indicateurs)

fig = px.choropleth(df, geojson=geo_dep, locations='Code_Dep', color=df[indicateur],
                            hover_name= 'Nom',
                            title = str(indicateur),
                            color_continuous_scale="Viridis",
                            range_color=(min(df[indicateur]),max(df[indicateur])),
                            scope = 'europe',
                            center = { 'lat' : 48, 'lon' : 2}
                            )
fig.update_geos(visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)


comparaison = ['Non', 'Oui']
comparatif = st.sidebar.selectbox("Voulez-vous comparer deux indicateurs entre eux ? ", comparaison)
if comparatif == 'Oui':
    indicateur1 = st.sidebar.selectbox("Indicateur 1 ", list_indicateurs)
    indicateur2 = st.sidebar.selectbox("Indicateur 2 ", list_indicateurs)
    st.header('Cartes comparatives entre deux indicateurs')
    i1, i2 = st.columns(2)
    fig = px.choropleth(df, geojson=geo_dep, locations='Code_Dep', color=df[indicateur1],
                            hover_name= 'Nom',
                            title = str(indicateur1),
                            color_continuous_scale="Viridis",
                            range_color=(min(df[indicateur1]),max(df[indicateur1])),
                            scope = 'europe',
                            center = { 'lat' : 48.864716, 'lon' : 2.349014},
                            width = 400, 
                            height = 400 
                            )
    fig.update_geos(visible=False)
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    i1.plotly_chart(fig)
    
    fig = px.choropleth(df, geojson=geo_dep, locations='Code_Dep', color=df[indicateur2],
                            hover_name= 'Nom',
                            title = str(indicateur2),
                            color_continuous_scale="Viridis",
                            range_color=(min(df[indicateur2]),max(df[indicateur2])),
                            scope = 'europe',
                            center = { 'lat' : 48, 'lon' : 2},
                            width = 400, 
                            height = 400 
                            )
    fig.update_geos(visible=False)
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    i2.plotly_chart(fig)

    @st.cache
    def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df[['Nom', indicateur1, indicateur2]])

    st.download_button(
    label="Télecharger le tableau des données comparatives au format CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
    )
    



