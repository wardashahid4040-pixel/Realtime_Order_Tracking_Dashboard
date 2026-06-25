# 📦 Real-Time Order Tracking Dashboard

A real-time, interactive web application built with Streamlit to monitor and track live orders directly from Google Form submissions via Google Sheets. 

This project was developed as a BSCS academic project to demonstrate data visualization, real-time data fetching, and geospatial mapping.

## ✨ Features

* **Real-Time Updates:** Automatically refreshes every 60 seconds to fetch the latest order data.
* **Smart Filtering:** Filter orders by "Order Status" and "City".
* **Advanced Search:** Search for specific orders using Customer Name or Email.
* **Predictive Forecasting:** Analyzes the last 7 days of data to predict expected orders for the next 30 days.
* **Geospatial Mapping:** Automatically geocodes cities using `geopy` and plots order locations on an interactive map.
* **Summary & Analytics:** Visualizes daily order trends and status breakdowns.

## 🛠️ Tech Stack

* **Language:** Python
* **Framework:** Streamlit
* **Data Manipulation:** Pandas
* **Geocoding:** Geopy (Nominatim)
* **Auto-Refresh:** `streamlit-autorefresh`
* **Database:** Google Sheets (Published as CSV)



