
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

    # Make sure column exists
    if "Base Price" not in df.columns:
        st.error("Your file must include a 'Base Price' column.")
    else:
        try:
            # Clean and convert the Base Price column
            df["Base Price"] = df["Base Price"].astype(str)
            df["Base Price"] = df["Base Price"].str.replace("$", "", regex=False)
            df["Base Price"] = pd.to_numeric(df["Base Price"], errors="coerce")
            df = df.dropna(subset=["Base Price"])

            # Calculate prices
            for platform in platforms:
                df[f"{platform} Price"] = (df["Base Price"] * (1 + markup_dict[platform] / 100)).round(2)

            st.write(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Adjusted CSV", data=csv, file_name="adjusted_prices.csv", mime="text/csv")

        except Exception as e:
            st.error(f"Error processing 'Base Price': {e}")
