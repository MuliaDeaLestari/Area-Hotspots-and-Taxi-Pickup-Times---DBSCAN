import streamlit as st
import pandas as pd

@st.cache_data()
def load_data(data):
    df = pd.read_csv(data)

    if 'pickup_datetime' not in df.columns:
       st.warning("kolom pickup_datetime tidak ada dalam file dataset, silahkan perbarui data!")

    if 'pickup_longitude' not in df.columns:
       st.warning("kolom pickup_longitude tidak ada dalam file dataset, silahkan perbarui data!")

    if 'pickup_latitude' not in df.columns:
       st.warning("kolom pickup_latitude tidak ada dalam file dataset, silahkan perbarui data!")

    if 'dropoff_longitude' not in df.columns:
       st.warning("kolom dropoff_longitude tidak ada dalam file dataset, silahkan perbarui data!")

    if 'dropoff_latitude' not in df.columns:
       st.warning("kolom dropoff_latitude tidak ada dalam file dataset, silahkan perbarui data!")

    if 'trip_duration' not in df.columns:
       st.warning("kolom trip_duration tidak ada dalam file dataset, silahkan perbarui data!")

    if 'pickup_datetime' in df.columns and 'pickup_longitude' in df.columns and 'pickup_latitude' in df.columns and 'dropoff_longitude' in df.columns and 'dropoff_latitude' in df.columns and 'trip_duration' in df.columns:
        st.write(df)
        st.markdown(f':red[{df.shape[0]} rows], :red[{df.shape[1]} columns]')

        return df

      

   

    

    


