
########## PACKAGES ##########

# cd documents/python/streamlit
# streamlit run learn_st.py

import streamlit as st
import pandas as pd
import numpy as np

########## DISCOVERY ##########

st.title('Just have fun with python')

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [1, 4, 9, 49]
})

st.dataframe(df) # afficher le dataframe
st.line_chart(df)


st.text('This is some text just not for fun')

st.write("SQUARED")
x = st.slider('Ici un slider de 0 à 100')
st.write(x, 'squared is', x * x) # carré du slider



########## CACHE STREAMLIT ##########
# """
# quand on marque une fonction avec @st.cache à chaque fois qu'elle est appelée on vérifie :
# - le corps de la fonction
# - les éléments dont dépend la fonction
# - les paramètres entrés lors des appels
#
# Si c'est la première fois qu'on l'appelle avec ces valeurs exactes il exécute la fonction et stocke le résultat dans un cache local
# La prochaine fois que la fonction est appelée, si les trois valeurs n'ont pas changé, alors Streamlit ignore complètement l'exécution de la fonction et lit la sortie du cache local
# """

DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


# df.columns=["colon1","colon2"]

# permet de charger nrows ligne du dataframe
@st.cache # cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    # transformer en minuscule tous les noms de colonne
    data.rename(lowercase, axis='columns', inplace=True)

    # date sous format yyyy-mm-jj hh-mm-ss.ttttttttt
    data['date/time'] = pd.to_datetime(data['date/time'])
    return data


########## INSPECTER LES DONNÉES ##########


# title
st.title('Uber pickups in NYC \n')

# entête
st.subheader('LIGNES DE DONNÉES')

# indiquer le chargement des données
data_load_state = st.text('Loading data...')

# charger 1000 lignes de données
data = load_data(1000)

# indiquer la fin du chargement
data_load_state.text('Loading data...done!')


########## FILTRER AVEC CHECKBOX ##########


if st.checkbox('Show all data'):
    st.write(data) # ou st.dataframe(data)


########## HISTOGRAMME ET MAP ##########


# entête
st.subheader('Number of all pickups by hour')

# sépare en 24 heures
histo = np.histogram(data['date/time'].dt.hour, bins=24, range=(0,24))

# histo
hist_values = histo[0]
st.bar_chart(hist_values)

# Map
st.subheader('Map of all pickups')
st.map(data)


########## MOMENT LE PLUS AFFLUENT ##########


# filtrage
h = 10
data_h = data[data['date/time'].dt.hour==h]

# entête
st.subheader(f'Number of pickups by minutes at {h}:00')

# histogramme
histo_h = np.histogram(data_h['date/time'].dt.minute, bins=60, range=(0,60))

hist_h_values = histo_h[0]
st.bar_chart(hist_h_values)

# map
st.subheader(f'Map of all at {h}:00')
st.map(data_h)


########## FILTRER AVEC LE SLIDER ##########


# filtrage
filter = st.slider('choose hour', 0, 23, 17)  # de 0 à 23, défaut = 17
data_filter = data[data['date/time'].dt.hour==filter]

# entête
st.subheader(f'Number of pickups by minutes at {filter}:00')


# histogramme
histo_filter = np.histogram(data_filter['date/time'].dt.hour, bins=24, range=(0,24))

hist_filter_values = histo_filter[0]
st.bar_chart(hist_filter_values)

# map
st.subheader(f'Map of all at {filter}:00')
st.map(data_filter)



########## DEPLOYER L'APP AVEC STREAMLIT CLOUD ##########

# mettre sur un repo public github

# s'inscrire à share.streamlit.io

# Cliquer 'Deploy an app' puis coller l'url du repo