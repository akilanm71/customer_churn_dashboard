import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

st.title("📊 Telecom Customer Churn Analysis Dashboard")

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("Data/telco.csv")

model = joblib.load("churn_randfor_model.pkl")
model_cols = joblib.load("features.pkl")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔎 Filter Customers")

contract_filter = st.sidebar.multiselect(
    "Select Contract Type",
    options=df["Contract"].unique(),
    default=df["Contract"].unique()
)

internet_filter = st.sidebar.multiselect(
    "Select Internet Service",
    options=df["Internet Service"].unique(),
    default=df["Internet Service"].unique()
)

tenure_range = st.sidebar.slider(
    "Tenure (Months)",
    int(df["Tenure in Months"].min()),
    int(df["Tenure in Months"].max()),
    (int(df["Tenure in Months"].min()), int(df["Tenure in Months"].max()))
)

charge_range = st.sidebar.slider(
    "Monthly Charge",
    float(df["Monthly Charge"].min()),
    float(df["Monthly Charge"].max()),
    (float(df["Monthly Charge"].min()), float(df["Monthly Charge"].max()))
)

# -------------------------
# Apply Filters
# -------------------------
filtered_df = df[
    (df["Contract"].isin(contract_filter)) &
    (df["Internet Service"].isin(internet_filter)) &
    (df["Tenure in Months"].between(tenure_range[0], tenure_range[1])) &
    (df["Monthly Charge"].between(charge_range[0], charge_range[1]))
]

# -------------------------
# KPI Metrics
# -------------------------
total_customers = filtered_df.shape[0]
churned = filtered_df[filtered_df["Churn Label"] == "Yes"].shape[0]
churn_rate = round((churned / total_customers) * 100, 2) if total_customers > 0 else 0
avg_monthly = round(filtered_df["Monthly Charge"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", churned)
col3.metric("Churn Rate (%)", churn_rate)
col4.metric("Avg Monthly Charge", avg_monthly)

st.divider()

# -------------------------
# Row 1
# -------------------------
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(
        filtered_df,
        names="Churn Label",
        title="Customer Churn Distribution",
        hole=0.4
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(
        filtered_df,
        names="Contract",
        title="Contract Type Distribution",
        hole=0.4
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -------------------------
# Row 2
# -------------------------
col3, col4 = st.columns(2)

with col3:
    fig3 = px.histogram(
        filtered_df,
        x="Churn Label",
        color="Churn Label",
        title="Customer Churn Count"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.histogram(
        filtered_df,
        x="Contract",
        color="Churn Label",
        title="Contract Type vs Churn"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# -------------------------
# Row 3
# -------------------------
col5, col6 = st.columns(2)

with col5:
    fig5 = px.box(
        filtered_df,
        x="Churn Label",
        y="Monthly Charge",
        title="Monthly Charge vs Churn"
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    fig6 = px.box(
        filtered_df,
        x="Churn Label",
        y="Tenure in Months",
        title="Tenure vs Churn"
    )
    st.plotly_chart(fig6, use_container_width=True)

st.divider()

# -------------------------
# Row 4
# -------------------------
col7, col8 = st.columns(2)

with col7:
    fig7 = px.histogram(
        filtered_df,
        x="Internet Service",
        color="Churn Label",
        title="Internet Service vs Churn"
    )
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    fig8 = px.histogram(
        filtered_df,
        x="Payment Method",
        color="Churn Label",
        title="Payment Method vs Churn"
    )
    st.plotly_chart(fig8, use_container_width=True)

st.divider()

# -------------------------
# Satisfaction Analysis
# -------------------------
st.subheader("Customer Satisfaction Analysis")

reason_sat = filtered_df[filtered_df["Churn Label"] == "Yes"].groupby(
    "Churn Reason"
)["Satisfaction Score"].mean().reset_index()

fig9 = px.bar(
    reason_sat,
    x="Churn Reason",
    y="Satisfaction Score",
    color="Satisfaction Score",
    title="Average Satisfaction Score by Churn Reason"
)

st.plotly_chart(fig9, use_container_width=True)

# -------------------------
# Map
# -------------------------
st.subheader("Customer Location Distribution")

fig10 = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    color="Churn Label",
    zoom=3
)

fig10.update_layout(mapbox_style="open-street-map")

st.plotly_chart(fig10, use_container_width=True)

st.divider()

# -------------------------
# Feature Importance
# -------------------------
st.subheader("Top Features Driving Customer Churn")

importances = model.feature_importances_

feature_df = pd.DataFrame({
    "Feature": model_cols,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

top_features = feature_df.head(10)

fig11 = px.bar(
    top_features,
    x="Importance",
    y="Feature",
    orientation="h",
    color="Importance",
    title="Top 10 Important Features"
)

fig11.update_layout(yaxis=dict(autorange="reversed"))

st.plotly_chart(fig11, use_container_width=True)

# -------------------------
# Raw Data
# -------------------------
st.subheader("Filtered Dataset")
st.dataframe(filtered_df)