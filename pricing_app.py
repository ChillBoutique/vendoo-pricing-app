
import streamlit as st
import pandas as pd

st.title("Marketplace Pricing Adjuster (10 Marketplaces)")

uploaded_file = st.file_uploader("Upload your inventory CSV", type="csv")

st.sidebar.header("Markup Rates")

# Define platform markups interactively
markup_dict = {}
platforms = [
    "Poshmark", "eBay", "Mercari", "Etsy", "Depop", "Grailed",
    "Kiddizen", "Shopify", "Facebook Marketplace", "Tradesy (legacy)"
]

default_markups = [15, 10, 5, 10, 0, 9, 12, 0, 5, 19]

for platform, default in zip(platforms, default_markups):
    markup_dict[platform] = st.sidebar.number_input(f"{platform} (%)", 0, 100, default)

# Process file
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "Base Price" in df.columns:
        for platform in platforms:
            df[f"{platform} Price"] = (df["Base Price"] * (1 + markup_dict[platform] / 100)).round(2)
        st.write(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Adjusted CSV", data=csv, file_name="adjusted_prices.csv", mime="text/csv")
    else:
        st.error("Your CSV must include a 'Base Price' column.")
