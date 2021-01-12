import numpy as np
import pandas as pd
import streamlit as st
import csv
import altair as alt
import pydeck as pdk
from PIL import Image 
import bs4 as bs
import urllib.request

st.set_page_config(layout="wide")


add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

col_title, col_dv = st.beta_columns(2)

with col_title:
    st.title('Art Classifier')
    st.subheader('An art classifier using data from the Kaggle dataset')
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("</br>", unsafe_allow_html=True)
    st.write('By Jeb Williams')



with col_dv:
    
    image_dv = Image.open('./Artworks/images/images/Diego_Velazquez/Diego_Velazquez_51.jpg')
    st.image(image_dv, use_column_width=True)


st.markdown("---", unsafe_allow_html=True)


with st.beta_expander("1. Import Libraries"):
    st.write(f'Numpy version: {np.__version__}')
    st.write(f'Pandas version: {pd.__version__}')
    st.write(f'Streamlit version: {st.__version__}')
    st.write(f'CSV version: {csv.__version__}')
    st.write(f'Altair version: {alt.__version__}')

st.markdown("</br>", unsafe_allow_html=True)

with st.beta_expander("2. Import data"):

    df = pd.read_csv('./Artworks/artists.csv')
    st.dataframe(df, 1000, 400)

    st.markdown("---", unsafe_allow_html=True)

    paintings_per_artist = df[['name', 'paintings']]

    paintings_per_artist_chart = alt.Chart(paintings_per_artist).mark_bar().encode(
        x='name',
        y='paintings',
        tooltip=['name','paintings'],
    ).properties(
        width=700,
        height=500
    )
    st.altair_chart(paintings_per_artist_chart)

st.markdown("</br>", unsafe_allow_html=True)

with st.beta_expander("4. Genre of Painters"):
    df_genre = pd.DataFrame(df['genre'].str.get_dummies(',').sum())
    df_genre.reset_index(level=0, inplace=True)
    df_genre = df_genre.rename({'index': 'genre', 0: 'count'}, axis=1)
    

    genre_chart = alt.Chart(df_genre).mark_bar().encode(
        x='genre',
        y='count',
        tooltip=['genre','count'],
    ).properties(height=500, width=700)

    col_genre_chart, col_genre = st.beta_columns([2,1])
    
    with col_genre_chart:
        st.altair_chart(genre_chart)
    with col_genre:
        df_genre

st.markdown("</br>", unsafe_allow_html=True)

with st.beta_expander("5. Nationality of Painters"):

    df_nationality = pd.DataFrame(df['nationality'].str.split(',').str[0])
    df_nationality = df_nationality.replace('Flemish', 'Belgian')

    df_latlong = pd.read_csv('./Artworks/world_country_and_usa_states_latitude_and_longitude_values.csv')
    df_latlong = df_latlong.drop(columns=['country_code','usa_state_code', 'usa_state_latitude', 'usa_state_longitude', 'usa_state'])

    # source = urllib.request.urlopen('https://www.englishclub.com/vocabulary/world-countries-nationality.php').read()
    # soup = bs.BeautifulSoup(source,'lxml')

    # table = soup.find( "table", {"class":"ec-table"} )
    # df_nat_adj = pd.read_html(str(table))[0]
    # df_nat_adj.to_csv(r'./Artworks/nation_adj.csv')
    
    df_nat_adj = pd.read_csv('./Artworks/nation_adj.csv')
    df_nat_adj = df_nat_adj.drop(columns=['Unnamed: 0','person']).rename(columns={"adjective": "nationality"})

    df_nat_adj = df_nat_adj.replace('United Kingdom (UK)', 'United Kingdom')
    df_nat_adj = df_nat_adj.replace('UK (used attributively only, as in UK time but not He is UK) or British', 'British')
    df_nat_adj = df_nat_adj.replace('United States of America (USA)', 'United States')
    df_nat_adj = df_nat_adj.replace('US (used attributively only, as in US aggression but not He is US)', 'American')
    df_nat_adj = df_nat_adj.replace('Netherlands, the (see Holland)', 'Netherlands')
    
    df_position = pd.merge(df_latlong, df_nat_adj, how='inner')
    df_position = pd.merge(df_position, df_nationality, how='inner')
    df_position

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v9',
        initial_view_state=pdk.ViewState(
            latitude=50,
            longitude=-20,
            zoom=1,
            pitch=50,
        ),
        layers=[
            pdk.Layer(

                'HexagonLayer',
                data=df_position,
                get_position='[longitude, latitude]',
                radius=100000,
                elevation_scale=2000,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df_position,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
        tooltip = {
            "html": "<b>Number of Painters: {elevationValue}</b>",
            "style": {"background": "steelblue", "color": "white", "size": 5,  "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
        },
    ))
    

st.markdown("</br>", unsafe_allow_html=True)

with st.beta_expander("6. Timeline of Painters"):

    df['years_split'] = pd.DataFrame(df['years'].str.split(' - '))
    df

    df['years_split'] = pd.DataFrame(df['years'].str.split(' '))
    df

    source = pd.DataFrame([
        {"task": "A", "start": 1, "end": 3},
        {"task": "B", "start": 3, "end": 8},
        {"task": "C", "start": 8, "end": 10}
    ])

    timeline_artists = alt.Chart(source).mark_bar().encode(
        x='start',
        x2='end',
        y='task'
    )



    st.altair_chart(timeline_artists)