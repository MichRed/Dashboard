import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Wczytanie danych
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
sports_df = pd.read_csv(os.path.join(desktop_path, 'sports.csv'))
orders_df = pd.read_csv(os.path.join(desktop_path, 'orders.csv'))
customer_orders_df = pd.read_csv(os.path.join(desktop_path, 'customer_orders.csv'))

# Przygotowanie danych
orders_df['value'] = orders_df['value'].astype(str).str.replace(r'[^\d,.-]', '', regex=True).str.replace(',', '.')
orders_df['value'] = pd.to_numeric(orders_df['value'], errors='coerce')
orders_df.dropna(subset=['value'], inplace=True)

# Statystyki ogólne
total_customers = customer_orders_df['customer_id'].nunique()
total_orders = orders_df['order_id'].nunique()
average_order_value = orders_df['value'].mean()
multi_order_customers = customer_orders_df.groupby("customer_id")["order_id"].nunique()
percent_multi_orders = (multi_order_customers[multi_order_customers > 1].count() / total_customers) * 100

# Sporty
sports_count = sports_df['sport'].value_counts()
avg_sports_per_customer = sports_df.groupby("customer_id")['sport'].nunique().mean()

# Streamlit layout
st.title("Dashboard Decathlon - Profil Klienta")

st.header("Statystyki ogólne")
st.metric("Liczba klientów", total_customers)
st.metric("Liczba zamówień", total_orders)
st.metric("Średnia wartość zamówienia (zł)", f"{average_order_value:.2f}")
st.metric("% klientów z >1 zamówieniem", f"{percent_multi_orders:.2f}%")

st.header("Sporty uprawiane przez klientów")
st.write(f"Średnia liczba sportów na klienta: {avg_sports_per_customer:.2f}")
st.plotly_chart(px.bar(sports_count.head(10), title="Top 10 najpopularniejszych sportów"))

st.header("Rozkład wartości zamówień")

# Kategoryzacja zamówień wg przedziałów wartości
bins = [0, 50, 100, 150, 200, float('inf')]
labels = ['0-50 zł', '51-100 zł', '101-150 zł', '151-200 zł', '200+ zł']
orders_df['value_range'] = pd.cut(orders_df['value'], bins=bins, labels=labels, right=True)

# Zliczanie liczby zamówień w każdym przedziale
order_bins_count = orders_df['value_range'].value_counts().sort_index()

# Wykres
fig = px.bar(
    order_bins_count,
    x=order_bins_count.index,
    y=order_bins_count.values,
    labels={'x': 'Przedział wartości zamówienia', 'y': 'Liczba zamówień'},
    title='Liczba zamówień wg przedziału wartości',
    text=order_bins_count.values
)
fig.update_traces(textposition='outside')

st.plotly_chart(fig)
