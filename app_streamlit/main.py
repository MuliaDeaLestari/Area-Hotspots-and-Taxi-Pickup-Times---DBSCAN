import streamlit as st
from streamlit_option_menu import option_menu
from persist import persist, load_widget_state
from function_home import rules, export_csv, get_data
from function_upload import load_data
from function_processing import filter_day, cluster_pickup, maps, create_fitur, data_cleaning, data_cleaning2
from function_dashboard import pie_cluster, bar_distance, count_pickup_hour, speed_vs_pickuph, bar_duration_min, maps_cluster


st.set_page_config(layout="wide")

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    """

st.markdown(hide_st_style, unsafe_allow_html=True)
with st.sidebar:
    selected = option_menu(
        menu_title = None, #"Menu",
        options=["Home", "Upload", "Processing", "Dashboard"],
        default_index=0,
        icons=["house", "cloud-plus", "arrow-repeat", "bar-chart"],
    )

def main():
    if 'data_path' not in st.session_state:
        st.session_state['data_path'] = None

    if 'cluster' not in st.session_state:
        st.session_state['cluster'] = None 
    
    if selected == 'Home':
        rules()  
        data = get_data()
        export_csv(data)
      
    if selected == 'Upload':
        menu_2 = '<p style="font-family:Georgia; color:Black; text-align:center; font-size: 50px;">Upload File Dataset</p>'
        st.write(menu_2, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose file dataset (with type csv)", type=['csv'])

        if uploaded_file is not None:
            uploaded_data = load_data(uploaded_file)
            st.session_state['data_path'] = uploaded_data
            
        elif hasattr(st.session_state, 'data_path'):
            if st.session_state['data_path'] is not None:
                st.write(st.session_state['data_path'])
                st.markdown(f':red[{st.session_state["data_path"].shape[0]} rows], :red[{st.session_state["data_path"].shape[1]} columns]')


    if selected == 'Processing':
        menu_2 = '<p style="font-family:Georgia; color:Black; text-align:center; font-size: 50px;">Processing</p>'
        st.write(menu_2, unsafe_allow_html=True)
        # try:
        if st.session_state['data_path'] is None:
            st.info("Please Input data first in upload section")
    
        else:
            st.session_state['new_fitur'] = create_fitur(st.session_state['data_path'].copy())
            
            st.session_state['data_clean'] = data_cleaning(st.session_state['new_fitur'])

            data = data_cleaning2(st.session_state['data_clean'])

            title_pre = '<p style="font-family:Courier; color:Blue; font-size: 24px;"><b>Table of Result Pre-processing</b></p>'
            st.write(title_pre, unsafe_allow_html=True)

            data_filter = filter_day(data)

            if 'eps_slider' not in st.session_state:
                st.session_state['eps_slider'] = 0.5

            if 'eps_slider' in st.session_state:
                st.sidebar.slider('Epsilon', 0.05, 2.0, key=persist("eps_slider"))
            
            if 'minpts_slider' not in st.session_state:
                st.session_state['minpts_slider'] = 16

            if 'minpts_slider' in st.session_state:
                st.sidebar.slider('MinPts', 1, 25, key=persist('minpts_slider'))


            if data_filter.shape[0] !=0:
                st.session_state['cluster'] = cluster_pickup(st.session_state["eps_slider"], st.session_state['minpts_slider'], data_filter)
                
                title = '<p style="font-family:Courier; color:Blue; font-size: 24px;"><b>Table of Result Clustering</b></p>'
                st.write(title, unsafe_allow_html=True)
                st.dataframe(st.session_state['cluster'])
        
                st.markdown(f':red[{st.session_state["cluster"].shape[0]} rows], :red[{st.session_state["cluster"].shape[1]} columns]')

                title = '<p style="font-family:Courier; color:Blue; font-size: 24px;"><b>Maps of Clustering</b></p>'
                st.write(title, unsafe_allow_html=True)

                map = maps(st.session_state['cluster'])

            else:
                st.warning("Please select filter at sidebar", icon="⚠️")
    

    if selected == 'Dashboard':
        menu_3 = '<p style="font-family:Georgia; color:Black; text-align:center; font-size: 50px;">Dashboard</p>'
        st.write(menu_3, unsafe_allow_html=True)
        # try:
        if st.session_state['cluster'] is None:
            st.info("Please Input data first in upload section")
        else:
            cluster = st.session_state['cluster']
            st.sidebar.radio('Select cluster', cluster['cluster_pickup'].unique(), key=persist('cluster_f'))

            left_column, right_column = st.columns(2)
            with left_column:
                pie = pie_cluster(cluster)
                title = '<p style="font-family:Courier; color:Blue; text-align:center; font-size: 24px;"><b>Number of Each Cluster</b></p>'
                st.write(title, unsafe_allow_html=True)
                left_column.plotly_chart(pie, use_container_width=True)

            with right_column:
                title = '<p style="font-family:Courier; color:Blue; text-align:center; font-size: 24px;"><b>Maps of Cluster</b></p>'
                st.write(title, unsafe_allow_html=True)
                queens_map = maps_cluster(cluster, st.session_state['cluster_f'])
                
            bar_1, bar_2 = st.columns(2)
            with bar_1:
                bar = bar_distance(cluster, st.session_state['cluster_f'])
                title = '<p style="font-family:Courier; color:Blue; text-align:center; font-size: 24px;"><b>Average Distance by Time (Hours)</b></p>'
                st.write(title, unsafe_allow_html=True)
                bar_1.plotly_chart(bar, use_container_width=True)
                
                
            with bar_2:
                title = '<p style="font-family:Courier; color:Blue; text-align:center; font-size: 24px;"><b>Average Duration (Minutes) by Time (Hours)</b></p>'
                st.write(title, unsafe_allow_html=True)
                bar_minutes = bar_duration_min(cluster, st.session_state['cluster_f'])
                bar_2.plotly_chart(bar_minutes, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                title = '<p style="font-family:Courier; color:Blue; text-align:center; font-size: 24px;"><b>Number of Pickup Day by Time (Hours)</b></p>'
                st.write(title, unsafe_allow_html=True)
                ph = count_pickup_hour(cluster, st.session_state['cluster_f'])
                col1.plotly_chart(ph, use_container_width=True)
       
            with col2:
                title = '<p style="font-family:Courier; color:Blue; text-align:center; font-size: 24px;"><b>Average Speed by Time (Hours)</b></p>'
                st.write(title, unsafe_allow_html=True)
                speed_ph = speed_vs_pickuph(cluster, st.session_state['cluster_f'])
                col2.plotly_chart(speed_ph, use_container_width=True)
           

if __name__ == "__main__":
    load_widget_state()
    main()