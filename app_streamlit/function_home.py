import streamlit as st
import pandas as pd
import base64

def rules():
    st.write("# Welcome to Taxi Application 👋")
    st.markdown(
        """
        Aplikasi taksi ini merupakan aplikasi berbasis website yang bertujuan untuk
        mengidentifikasi area dan waktu penjemputan taksi sebagai sarana rekomendasi
        keputusan untuk meningkatkan layanan taksi dengan cara melakukan proses modeling clustering,
        dan mengidentifikasi pola dan karakteristik dari hasil pemodelan serta pengetahuan yang ditampilkan pada dashboard.
        """
    )
    st.markdown(
        """
        ### Aturan untuk File Dataset
         Sebelum masuk untuk proses modeling, perlu diketahui beberapa aturan file yang dapat digunakan. 
         Berikut aturan yang dapat diikuti :
        - Tipe file yang bisa diupload hanya **bertipe csv**
        - **Limit** size untuk file dataset sebesar **200MB**
        - Dari file dataset **setidaknya** memiliki **6 kolom** yang terdiri dari **pickup_datetime, 
        pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude dan trip_duration**
        - Kolom **pickup_datetime** harus memiliki format **tanggal dan waktu seperti yyyy-MM-dd HH:mm:ss:**
        - Kolom **pickup_longitude, pickup_latitude, dropoff_longitude, dan dropoff_latitude** harus memiliki format **decimal degree**
        - Kolom **trip_duration** harus memiliki format dalam hitungan **detik** 

        ### Data Sample
        Tabel di bawah merupakan contoh dari dataset yang bisa digunakan. Silahkan cermati, dan diikuti sesuai aturan yang ada\n
        **Note**: Perhatikan nama kolom yaitu dengan huruf kecil semua
        """
        
    )

    df = pd.DataFrame({
        "pickup_datetime": ['2016-01-19 11:35:24', '2016-01-03 03:33:21', '2016-01-30 22:42:51', '2016-01-28 15:31:01', '2016-01-14 09:24:37'],
        "pickup_longitude": [-73.979027, -73.984848, -73.786217, -73.885223, -74.016640],
        "pickup_latitude" : [40.763939, 40.724335, 40.645287,40.772728, 40.709858],
        "dropoff_longitude": [-74.005333, -73.884117, -73.993073, -73.980583, -73.785713],
        "dropoff_latitude": [40.710087, 40.71671, 40.729729, 40.781666, 40.712227],
        "trip_duration": [2124, 2159, 2453, 2629, 2124]
    })

    st.dataframe(df)

# Fungsi untuk mengambil data dari URL
url = 'https://drive.google.com/uc?export=download&id=1S0P3qrlze57nUJOZJC6GoqjXOqoJJaMw'
def get_data():
    df = pd.read_csv(url)

    return df


def export_csv(df):
    st.write('Jika masih kurang jelas silahkan download file csv dibawah untuk melihat contoh file dataset yang bisa digunakan')
    csv=df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download File Dataset</a>'
    st.markdown(href, unsafe_allow_html=True)
