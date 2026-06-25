import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import time
from streamlit_autorefresh import st_autorefresh  

st_autorefresh(interval=60000, key="dashboardrefresh")

# Streamlit page config
st.set_page_config(page_title="📦 Order Tracking Dashboard", layout="wide")

st.title("📦 Real-Time Order Tracking Dashboard")
st.caption("Monitor live orders from Google Form submissions")

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSIio1cEFrxUbJEpg4SzgUnxKEiBH4e_r2GNDi4haOsMxXLrN4quMssNn8dAaIOUoZJuoMHL9MIeItY/pub?output=csv"

df = pd.read_csv(sheet_url)

# Clean and preprocess
df.columns = df.columns.str.strip()
df = df.dropna(subset=["City", "Order Status"])
df["City"] = df["City"].str.strip().str.title()
df["Order Status"] = df["Order Status"].str.strip().str.title()

# Extract order date from timestamp if available
if 'Timestamp' in df.columns:
    df['Order Date'] = pd.to_datetime(df['Timestamp']).dt.date

# Sidebar filters
st.sidebar.header("🔍 Filter Orders")

status_options = df["Order Status"].unique().tolist()
selected_status = st.sidebar.multiselect(
    "📦 Select Order Status:",
    options=status_options,
    default=status_options,
    format_func=lambda x: f"✅ {x}" if x == "Delivered" else f"🚚 {x}" if x == "Shipped" else f"⏳ {x}"
)

city_options = df["City"].unique().tolist()
selected_cities = st.sidebar.multiselect(
    "🌍 Select City:",
    options=city_options,
    default=city_options
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔎 Advanced Search")
search_field = st.sidebar.selectbox("Search by:", options=["Customer Name", "Email"])
search_keyword = st.sidebar.text_input(f"Enter {search_field} (optional)")

filtered_df = df[
    (df["Order Status"].isin(selected_status)) &
    (df["City"].isin(selected_cities))
]

if search_keyword:
    search_keyword = search_keyword.lower()
    if search_field in df.columns:
        filtered_df = filtered_df[
            filtered_df[search_field].str.lower().str.contains(search_keyword, na=False)
        ]
    else:
        st.sidebar.warning(f"⚠ '{search_field}' column not found in the sheet!")

# Order Summary
st.subheader("📊 Order Summary")
summary = filtered_df["Order Status"].value_counts()
st.write(summary)

# Daily trends and forecast
if 'Order Date' in df.columns:
    st.subheader("📅 Daily Orders Trend")
    daily_count = df.groupby("Order Date").size()
    st.line_chart(daily_count)

    daily_avg = daily_count[-7:].mean()
    predicted_30_days = int(daily_avg * 30)
    st.metric("Predicted Monthly Orders", predicted_30_days)

    st.subheader("🔮 Category-wise Forecast")
    status_daily = df.groupby(['Order Date', 'Order Status']).size().unstack().fillna(0)
    status_avg = status_daily[-7:].mean()

    for status in status_avg.index:
        st.write(f"📦 {status}: Expected in next 30 days → {int(status_avg[status] * 30)}")

# Geocoding cities
geolocator = Nominatim(user_agent="order-tracker")

@st.cache_data(show_spinner=False)
def get_lat_lon(city):
    try:
        location = geolocator.geocode(city)
        if location:
            return pd.Series([location.latitude, location.longitude])
    except:
        pass
    return pd.Series([None, None])

filtered_df[["Latitude", "Longitude"]] = filtered_df["City"].apply(get_lat_lon)

# Map display
st.subheader("🗽 Order Locations on Map")
map_df = filtered_df.dropna(subset=["Latitude", "Longitude"]).copy()
map_df.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}, inplace=True)

if not map_df.empty:
    st.map(map_df[["latitude", "longitude"]])
else:
    st.warning("No valid city locations to display on map.")

# Data table
st.subheader("📋 Order Details")
st.dataframe(filtered_df, use_container_width=True)

# Footer
st.caption(f"⏱ Last updated: {time.strftime('%d-%b-%Y %I:%M:%S %p')}")
st.markdown("---")
st.markdown("Created by Khadija Ejaz and Warda Shahid | BSCS Project")