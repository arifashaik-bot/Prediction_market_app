import streamlit as st
import pandas as pd
import os

st.title("Prediction Market App")

# Automatically detect local parquet files
local_files = [f for f in os.listdir(".") if f.endswith(".parquet")]

if local_files:
    selected_file = st.sidebar.selectbox("Select Dataset", local_files)
    
    try:
        df = pd.read_parquet(selected_file)
        st.write(f"Displaying {selected_file}")
        st.dataframe(df)
        
        st.subheader("Data Summary")
        st.write(df.describe())
        
        st.subheader("Column Info")
        st.write(df.dtypes)
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.error("No parquet files found in the current directory.")
