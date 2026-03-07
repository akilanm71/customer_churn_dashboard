import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

st.title(" Telecom Customer Churn Analysis Dashboard")

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("Data/telco.csv")

# -------------------------
# KPI Metrics
# -------------------------
total_customers = df.shape[0]
churned = df[df["Churn Label"] == "Yes"].shape[0]
churn_rate = round((churned / total_customers) * 100, 2)
avg_monthly = round(df["Monthly Charge"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", churned)
col3.metric("Churn Rate %", churn_rate)
col4.metric("Avg Monthly Charge", avg_monthly)

st.divider()

# -------------------------
# Row 1 (Pie Charts)
# -------------------------
col1, col2 = st.columns(2)

with col1:
    fig_pie1 = px.pie(
        df,
        names="Churn Label",
        title="Churn Distribution",
        hole=0.4
    )
    st.plotly_chart(fig_pie1, use_container_width=True)

with col2:
    fig_pie2 = px.pie(
        df,
        names="Contract",
        title="Contract Type Distribution",
        hole=0.4
    )
    st.plotly_chart(fig_pie2, use_container_width=True)

st.divider()

# -------------------------
# Row 2
# -------------------------
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(
        df,
        x="Churn Label",
        title="Customer Churn Distribution",
        color="Churn Label"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(
        df,
        x="Contract",
        color="Churn Label",
        title="Contract Type vs Churn"
    )
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Row 3
# -------------------------
col3, col4 = st.columns(2)

with col3:
    fig3 = px.box(
        df,
        x="Churn Label",
        y="Monthly Charge",
        title="Monthly Charge vs Churn"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.box(
        df,
        x="Churn Label",
        y="Tenure in Months",
        title="Tenure vs Churn"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# -------------------------
# Row 4
# -------------------------
col5, col6 = st.columns(2)

with col5:
    fig5 = px.histogram(
        df,
        x="Internet Service",
        color="Churn Label",
        title="Internet Service vs Churn"
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    fig6 = px.histogram(
        df,
        x="Payment Method",
        color="Churn Label",
        title="Payment Method vs Churn"
    )
    st.plotly_chart(fig6, use_container_width=True)

st.divider()

# -------------------------
# Row 5 (Satisfaction)
# -------------------------
st.subheader("Customer Satisfaction Analysis")

reason_sat = df[df["Churn Label"] == "Yes"].groupby(
    "Churn Reason"
)["Satisfaction Score"].mean().reset_index()

fig7 = px.bar(
    reason_sat,
    x="Churn Reason",
    y="Satisfaction Score",
    title="Average Satisfaction Score by Churn Reason",
    color="Satisfaction Score"
)

st.plotly_chart(fig7, use_container_width=True)

# -------------------------
# Row 6 (Map)
# -------------------------
st.subheader("Customer Location Distribution")

fig8 = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color="Churn Label",
    zoom=3,
    title="Customer Locations and Churn"
)

fig8.update_layout(mapbox_style="open-street-map")

st.plotly_chart(fig8, use_container_width=True)

# -------------------------
# Raw Data
# -------------------------
st.subheader("Dataset Preview")
st.dataframe(df)