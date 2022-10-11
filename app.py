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


st.title('Tutoriel Streamlit')
st.header('Créer un dashboard de visualisations spatiales avec Streamlit et Plotly ')

#list_indicateurs = list(df.columns[2:])
#indicateur = st.sidebar.selectbox("Selectionner un indicateur :", list_indicateurs)

list_indicateurs = df.columns[2:]
list_indicateurs = list_indicateurs.insert(0, "Aucun")
indicateur = st.selectbox('Choisissez un indicateur à visualiser', list_indicateurs)
if indicateur != "Aucun" : 

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




options = st.multiselect('Choisissez des départements à comparer', df['Nom'])
if len(options) >= 2 : 
    st.table(df.loc[df['Nom'].isin(options)])
    


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df.loc[df['Nom'].isin(options)])

st.download_button(
label="Télecharger le tableau des données comparatives au format CSV",
data=csv,
file_name='large_df.csv',
mime='text/csv')






