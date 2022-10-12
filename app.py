
import pandas as pd
import streamlit as st
import plotly.express as px
import json
from urllib.request import urlopen

# On charge les données 
df = pd.read_csv('./data/data_tuto_streamlit.csv', sep = ';')
with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as f : 
    geo_dep = json.load(f)

# On s'embête pas avec ça, retenir que c'est primordial c'est déjà bien.
state_id_map = {}
for feature in geo_dep['features']:
 feature['id'] = feature['properties']['code']
 state_id_map[feature['properties']['nom']] = feature['id']


t1, t2 = st.columns((0.05,0.2)) 


t1.image('./data/iiidata.png', width = 120)
t2.title('Tutoriel Streamlit')

st.header('Dashboard de visualisations spatiales')
viz, comparatif = st.tabs(['Visualiser les indicateurs', 'Comparer les indicateurs entre départements'])
with viz : 
    # La selectbox prend en paramètres des Dataframe alors ne nous privons pas ! 
    # Je crée un sous dataframe qui contient seulement les colonnes d'indicateurs
    list_indicateurs = df.columns[2:]
    # J'ajoute une colonne qui sera celle par défaut : celle qui n'affiche rien
    list_indicateurs = list_indicateurs.insert(0, "Aucun")
    # Je crée la selectbox ET je stocke la valeur dans une variable (important pour la suite)
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
with comparatif : 
    #On stocke sous forme de liste autant de départements que l'utilisateur a choisi 
    options = st.multiselect('Choisissez des départements à comparer', df['Nom'])
    # On met cette condition pour rester dans une logique de comparaison
    if len(options) >= 2 : 
        # Création d'une table avec nos 6 indicateurs et autant de lignes qu'il y a de departements choisis
        st.table(df.loc[df['Nom'].isin(options)])
    @st.cache
    def convert_df(df):
        # on rajoute le st.cache pour éviter la computation de la fonction à chaque run de l'app
        return df.to_csv().encode('utf-8')
    # Le principe est simplement d'utiliser la list "options" générée grâce au multiselect 
    csv = convert_df(df.loc[df['Nom'].isin(options)])
    st.download_button(
    label="Télecharger le tableau des données comparatives au format CSV",
    data=csv,
    file_name='comparatif_indic_dep.csv',
    mime='text/csv')






