
import streamlit as st
import pandas as pd
import plotly.express as px



# Load your real data
df_cluster = pd.read_csv("df_cluster.csv")

# Map cluster labels
cluster_labels = {
    0: "Significant Food Insecure & Volatile",
    1: "Food Secure & Stable",
    2: "Food Secure but Volatile",
    3: "Food Insecure but Volatile"
}

df_cluster['Cluster Label'] = df_cluster['Cluster'].map(cluster_labels)

st.set_page_config(page_title="Country Cluster Viewer", layout="centered")
st.title("🌍 Food Security Cluster Viewer")

country = st.selectbox("Select a country to see its cluster status:", df_cluster['Area'].unique())

if country:
    row = df_cluster[df_cluster['Area'] == country].iloc[0]
    st.subheader(f"📍 {country}")
    st.markdown(f"**Cluster:** {row['Cluster']}")
    st.markdown(f"**Situation:** {row['Cluster Label']}")

with st.expander("🌐 Show Global Choropleth Map"):
    fig = px.choropleth(
        df_cluster,
        locations="Area",
        locationmode="country names",
        color="Cluster",
        hover_name="Area",
        hover_data=["Cluster Label"],
        color_continuous_scale="viridis",
        title="Global Food Security Clusters"
    )
    fig.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='natural earth'))
    st.plotly_chart(fig, use_container_width=True)
