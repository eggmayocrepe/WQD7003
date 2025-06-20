import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA

# Load your pre-clustered data
# Ensure 'df_cluster.csv' contains 'Area' and 'Cluster' columns
try:
    df_cluster = pd.read_csv("df_cluster.csv")
except FileNotFoundError:
    st.error("Error: df_cluster.csv not found. Please make sure the file is in the same directory.")
    st.stop()

# --- Map cluster labels to create 'Cluster Label' column ---
# This ensures the 'Cluster Label' column exists even if not in the CSV
cluster_labels_map = {
    0: "Significant Food Insecure & Volatile",
    1: "Food Secure & Stable",
    2: "Food Secure but Volatile",
    3: "Food Insecure but Volatile"
}

# Ensure 'Cluster' column exists before mapping
if 'Cluster' in df_cluster.columns:
    df_cluster['Cluster Label'] = df_cluster['Cluster'].map(cluster_labels_map)
else:
    st.error("Error: 'Cluster' column not found in df_cluster.csv. This column is required to map cluster labels.")
    st.stop()

# --- Pre-calculated Clustering Information (from your Clustering.ipynb) ---
# IMPORTANT: Replace these with the actual values from when you generated df_cluster.csv
# If these values are different, please update them here or provide them.
silhouette_avg = 0.297
ch_score = 118.113
db_score = 1.059

food_security_vars_used = [
    'Prevalence of undernourishment (percent) (3-year average)',
    'Moderate+Severe Food Insecurity (percent)',
    'Severe Food Insecurity (percent)',
    'Percentage of children under 5 years affected by wasting (percent)',
    'Percentage of children under 5 years of age who are stunted (modelled estimates) (percent)',
    'Average dietary energy requirement (kcal/cap/day)',
    'Average protein supply (g/cap/day) (3-year average)',
    'Average supply of protein of animal origin (g/cap/day) (3-year average)',
    'Dietary energy supply used in the estimation of the prevalence of undernourishment (kcal/cap/day)',
    'Per capita food supply variability (kcal/cap/day)'
]
# -------------------------------------------------------------------------

st.set_page_config(page_title="Country Cluster Viewer", layout="centered")
st.title("🌍 Food Security Cluster Viewer")

# --- Cluster Viewer Section ---
st.header("1. Country Cluster Viewer")

# Display Clustering Metrics
st.subheader("Clustering Quality Metrics")
st.markdown(f"**Silhouette Score:** {silhouette_avg:.3f}")
st.markdown(f"**Calinski-Harabasz Index:** {ch_score:.3f}")
st.markdown(f"**Davies-Bouldin Index:** {db_score:.3f}")

# Display Food Security Variables Used
with st.expander("Show Food Security Variables Used for Clustering"):
    st.markdown("The following variables were used to cluster countries based on food security (based on the original clustering process that generated this data):")
    for var in food_security_vars_used:
        st.write(f"- {var}")

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

# --- ARIMA Model Section ---
st.header("2. Food Insecurity Time Series Forecast (ARIMA)")

try:
    # Load the time series data
    ts_data = pd.read_csv("food_insecurity_ts.csv")

    # Ensure 'Year' and 'Moderate+Severe Food Insecurity (percent)' columns exist
    if 'Year' not in ts_data.columns or 'Moderate+Severe Food Insecurity (percent)' not in ts_data.columns:
        st.error("Error: 'food_insecurity_ts.csv' must contain 'Year' and 'Moderate+Severe Food Insecurity (percent)' columns.")
        st.stop()

    # Prepare time series data
    ts_yearly = ts_data.groupby('Year')['Moderate+Severe Food Insecurity (percent)'].mean().to_frame()
    ts_yearly.index = pd.to_datetime(ts_yearly.index, format='%Y')
    ts_yearly.index.freq = 'YS' # Set frequency to Year Start

    with st.expander("📈 Show ARIMA Forecast"):
        st.subheader("Average Moderate+Severe Food Insecurity Over Years")

        # Plot historical time series
        fig_hist, ax_hist = plt.subplots(figsize=(10, 5))
        ax_hist.plot(ts_yearly, marker='o')
        ax_hist.set_title('Average Moderate+Severe Food Insecurity Over Years')
        ax_hist.set_ylabel('Percent')
        ax_hist.grid(True)
        st.pyplot(fig_hist) # Display plot in Streamlit

        st.subheader("ARIMA Model Fitting and Forecast")

        try:
            # Fiting ARIMA model
            model_arima = ARIMA(ts_yearly, order=(1, 1, 1))
            model_fit_arima = model_arima.fit()

            st.text("ARIMA Model Summary:")
            st.code(model_fit_arima.summary().as_text()) # Display model summary as text

            # Forecast next 5 years
            forecast_steps = 5
            forecast_arima = model_fit_arima.forecast(steps=forecast_steps)
            
            st.markdown(f"**Forecast for next {forecast_steps} years:**")
            st.write(forecast_arima.to_frame(name='Forecasted Moderate+Severe Food Insecurity (%)'))

            # Plot forecast
            forecast_index_arima = pd.date_range(start=ts_yearly.index[-1] + pd.DateOffset(years=1), periods=forecast_steps, freq='YS')
            
            fig_forecast, ax_forecast = plt.subplots(figsize=(10, 5))
            ax_forecast.plot(ts_yearly, label='Historical')
            ax_forecast.plot(forecast_index_arima, forecast_arima, label=f'Forecast (Next {forecast_steps} Years)', marker='o', linestyle='--')
            ax_forecast.set_title("ARIMA Forecast: Moderate+Severe Food Insecurity")
            ax_forecast.set_xlabel("Year")
            ax_forecast.set_ylabel("Percent")
            ax_forecast.legend()
            ax_forecast.grid(True)
            st.pyplot(fig_forecast) # Display forecast plot in Streamlit

        except Exception as e:
            st.error(f"ARIMA model fitting or forecasting failed: {e}. This often happens with short or non-stationary time series data.")
            st.info("Please ensure your 'food_insecurity_ts.csv' has sufficient historical data for the ARIMA model.")

except FileNotFoundError:
    st.error("Error: food_insecurity_ts.csv not found. Please provide this file with historical time series data.")
    st.info("The file should contain at least 'Year' and 'Moderate+Severe Food Insecurity (percent)' columns.")
except Exception as e:
    st.error(f"An error occurred loading or processing 'food_insecurity_ts.csv': {e}")