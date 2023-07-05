import streamlit as st
from persist import persist
import numpy as np
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import plotly.express as px


def groupDay(x):
  if x in range(0,5):
    return 'Weekday'
  else:
    return 'Weekend'

##function create column time to day
def time(x):
  if x in range(4,6):
    return 'Dawn'
  elif x in range(6,12):
    return 'Morning'
  elif x in range(12,17):
    return 'Afternoon'
  elif x in range(17,23):
    return 'Evening'
  else:
    return 'Late night'

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def create_fitur(df):
    
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

    if 'pickup_dayname' not in df.columns and 'pickup_monthname' not in df.columns:
        df["pickup_dayname"] = df['pickup_datetime'].dt.day_name()
        df["pickup_monthname"] = df['pickup_datetime'].dt.month_name()

    if 'pickup_groupofday' not in df.columns and 'pickup_timeofday' not in df.columns:
        df["pickup_day"] = df['pickup_datetime'].dt.weekday
        df['pickup_groupofday'] = df['pickup_day'].apply(groupDay)
        df["pickup_hour"] = df['pickup_datetime'].dt.hour
        df['pickup_timeofday'] = df['pickup_hour'].apply(time)

    if 'distance' not in df.columns:
       df['distance'] = df.apply(lambda x: haversine(x['pickup_latitude'],x['pickup_longitude'],x['dropoff_latitude'],x['dropoff_longitude'] ), axis=1)

    if 'average_speed' not in df.columns:
       df['average_speed'] = df['distance']/(df['trip_duration']/3600)
    
    if 'duration_min' not in df.columns:
       df['duration_min'] = np.round(df['trip_duration'] / 60)
    
    return df


def data_cleaning(df):
    #drop column
    selected_column =['pickup_datetime', 'pickup_longitude', 'pickup_latitude',
                      'pickup_dayname', 'pickup_monthname', 'pickup_day', 'pickup_groupofday',
                      'pickup_hour', 'pickup_timeofday', 'distance', 'average_speed', 'duration_min']

    df = df.drop(columns=[col for col in df.columns if col not in selected_column])
    data_summary(df)
    
    return df

def data_cleaning2(df):
    #Handling data duplicate
    df.drop_duplicates(inplace=True)

    #Handling Missing values
    df.dropna(axis=0, inplace=True)

    df = df.reset_index(drop=True)

    return df

def data_summary(df):
   col1, col2 = st.columns([2, 1])
   with col1:
      title_mv = '<p style="font-family:Courier; color:Blue; font-size: 24px;"><b>Number of missing value each column</b></p>'
      st.write(title_mv, unsafe_allow_html=True)
      # st.write('#### Number of missing value each column')
      st.write(df.isna().sum())
   with col2:
      title_mv = '<p style="font-family:Courier; color:Blue; font-size: 24px;"><b>Number of duplicate data</b></p>'
      st.write(title_mv, unsafe_allow_html=True)
      # st.write(f'#### Number of duplicate data : {df.duplicated().sum()}')
      st.write(df.duplicated().sum())

def filter_day(df): #saat pindah section setelah difilter tetap balik keawal default
    st.sidebar.header("Please Select Filter in Here:")
    # state = st.session_state.get(day_group=df['pickup_groupofday'].unique())
    if 'day_group' not in st.session_state:
       st.session_state['day_group'] = ['Weekday', 'Weekend']

    if 'day_group' in st.session_state :
      day = st.sidebar.multiselect(
          "Select the group of day:",
          options=df['pickup_groupofday'].unique(),
          key=persist("day_group"),
      )

    if 'time_group' not in st.session_state:
       st.session_state['time_group'] = ['Morning', 'Afternoon', 'Evening', 'Late night', 'Dawn']

    if 'time_group' in st.session_state :
      time = st.sidebar.multiselect(
        "Select the time:",
        options=df['pickup_timeofday'].unique(),
        key=persist('time_group')
      )
    
    df_selection = df.query(
        "pickup_groupofday == @day & pickup_timeofday == @time"
    )

    st.dataframe(df_selection)
    st.markdown(f':red[{df_selection.shape[0]} rows], :red[{df_selection.shape[1]} columns]')

    return df_selection


@st.cache_resource
def cluster_pickup(eps, minpts, df):
    # st.write("berhasil masuk")
    df_pickup = df[['pickup_latitude', 'pickup_longitude']]
    df_pickup = np.radians(df_pickup)
    df_pickup.astype('float32')
    

    kms_per_radian = 6371
    epsilon = eps / kms_per_radian
    clusters = DBSCAN(eps=epsilon, min_samples=minpts, algorithm='ball_tree', metric='haversine').fit(df_pickup)

    label = clusters.labels_

    title = '<p style="font-family:Courier; color:Blue; font-size: 24px;"><b>Information of Result Clustering</b></p>'
    st.write(title, unsafe_allow_html=True)
    st.write(f'Number of Hotspot: {len(np.unique(label[label!=-1]))}')
    st.write(f'Number of Outliers: {len(label[label==-1])}')
    
    acc = silhouette_score(df_pickup, label, metric="haversine")
    st.write(f'Accuracy Measurement: {round(acc, 4)}')
    
    df_pickup['cluster_pickup'] = label
    df_pickup[['pickup_latitude', 'pickup_longitude']] = df[['pickup_latitude', 'pickup_longitude']]

    merge_cluster = pd.concat([df, df_pickup['cluster_pickup']], axis=1)
    merge_cluster_clean = merge_cluster[merge_cluster['cluster_pickup']!=-1]
    
    st.session_state['cluster'] = merge_cluster_clean    
   
    return st.session_state['cluster']


@st.cache_resource
def maps(df_cluster):
    fig = px.scatter_mapbox(df_cluster, lat="pickup_latitude", lon="pickup_longitude", color="cluster_pickup", 
                            zoom=10, height=600, width=1100, color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(mapbox_style="open-street-map")

    maps = st.plotly_chart(fig)

    # display map
    return maps
