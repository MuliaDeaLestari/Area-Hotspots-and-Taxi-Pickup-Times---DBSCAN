import streamlit as st
import plotly.express as px


@st.cache_data
def pie_cluster(cluster):
    cluster_count = cluster.groupby(by=['cluster_pickup']).count()[['pickup_day']].rename(columns = {'pickup_day':'Total'})
    fig = px.pie(cluster_count, values='Total', names=cluster_count.index)

    return fig

@st.cache_resource
def maps_cluster(cluster, filter_cluster):
    cluster_i = cluster[cluster['cluster_pickup'] == filter_cluster].reset_index(drop=True)

    fig = px.scatter_mapbox(cluster_i, lat="pickup_latitude", lon="pickup_longitude", color="cluster_pickup", 
                            zoom=10, height=600, width=800, color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(mapbox_style="open-street-map")

    queens_maps = st.plotly_chart(fig)

    return queens_maps


@st.cache_data
def bar_distance(cluster, filter_cluster):
    cluster_i = cluster[cluster['cluster_pickup'] == filter_cluster]
    avg_dist = cluster_i.groupby(by=['pickup_hour', 'pickup_groupofday']).mean()
    fig = px.line(avg_dist, x=avg_dist.index.get_level_values(0), y='distance', color=avg_dist.index.get_level_values(1), markers=True)
    fig.update_layout(yaxis=(dict(showgrid=False)), xaxis_title='Pickup Time (Hour)', yaxis_title='distance (km)')
    x_uniq = avg_dist.index.get_level_values(0).unique()
    fig.update_xaxes(tickvals = x_uniq, ticktext=x_uniq)

    return fig

@st.cache_data
def bar_duration_min(cluster, filter_cluster):
    cluster_ = cluster[cluster['cluster_pickup'] == filter_cluster]
    avg_dur = cluster_.groupby(by=['pickup_hour', 'pickup_groupofday']).mean()
    fig = px.line(avg_dur, x=avg_dur.index.get_level_values(0), y='duration_min', color=avg_dur.index.get_level_values(1), markers=True)
    fig.update_layout(yaxis=(dict(showgrid=False)), xaxis_title='Pickup Time (Hour)', yaxis_title='duration (minutes)')
    x_uniq = avg_dur.index.get_level_values(0).unique()
    fig.update_xaxes(tickvals = x_uniq, ticktext=x_uniq)

    return fig

@st.cache_data
def count_pickup_hour(cluster, filter_cluster):
    cluster_i = cluster[cluster['cluster_pickup'] == filter_cluster]
    count_pickup = cluster_i.groupby(by=['pickup_hour', 'pickup_groupofday']).count()
    fig = px.line(count_pickup, x=count_pickup.index.get_level_values(0), y='pickup_datetime', color=count_pickup.index.get_level_values(1), markers=True)
    fig.update_layout(xaxis_title='Pickup Time (Hour)', yaxis_title='Number of Pickup')

    x_uniq = count_pickup.index.get_level_values(0).unique()
    fig.update_xaxes(tickvals = x_uniq, ticktext=x_uniq)

    return fig

@st.cache_data
def speed_vs_pickuph(cluster, filter_cluster):
    cluster_x = cluster[cluster['cluster_pickup'] == filter_cluster]
    mean_pickup = cluster_x.groupby(by=['pickup_hour', 'pickup_groupofday']).mean()
    fig = px.line(mean_pickup, x=mean_pickup.index.get_level_values(0), y='average_speed', color=mean_pickup.index.get_level_values(1), markers=True)
    fig.update_layout(xaxis_title='Pickup Time (Hour)', yaxis_title='Average Speed')

    x_uniq = mean_pickup.index.get_level_values(0).unique()
    fig.update_xaxes(tickvals = x_uniq, ticktext=x_uniq)

    return fig
