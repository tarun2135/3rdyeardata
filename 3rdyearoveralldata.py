import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import os

# Function to clean the data by removing commas and converting to float
def clean_data(column):
    return column.astype(str).str.replace(',', '').astype(float)

# Set Streamlit page to wide mode
st.set_page_config(layout="wide")

# Read the Excel files
file_path_academic = "All3yr.xlsx"
file_path_transportation = "All3yr.xlsx"

# Check if files exist
if not os.path.exists(file_path_academic):
    st.error(f"File not found: {file_path_academic}")
    st.stop()

if not os.path.exists(file_path_transportation):
    st.error(f"File not found: {file_path_transportation}")
    st.stop()

try:
    # Read the specific columns from the Excel file for Academic Fees
    df_academic = pd.read_excel(file_path_academic, usecols=["Academic Fees Paid", "Academic Due Fees"])
    
    # Clean the data for Academic Fees
    df_academic["Academic Fees Paid"] = clean_data(df_academic["Academic Fees Paid"])
    df_academic["Academic Due Fees"] = clean_data(df_academic["Academic Due Fees"])
    
    # Read both columns for Transportation Fees
    df_transportation = pd.read_excel(file_path_transportation)
    df_transportation["Transportation Fees Paid"] = clean_data(df_transportation["Transportation Fees Paid"])

    # Create a layout for side-by-side charts
    col1, col2 = st.columns(2)

    # Pie chart for Academic Fees
    with col1:
        
        
        total_fees_paid_academic = df_academic["Academic Fees Paid"].sum()
        total_due_fees_academic = df_academic["Academic Due Fees"].sum()
        
        labels_academic = ["Academic Fees Paid", "Academic Due Fees"]
        sizes_academic = [total_fees_paid_academic, total_due_fees_academic]
        
        fig, ax = plt.subplots(figsize=(6, 6))
        patches, texts, autotexts = ax.pie(sizes_academic, labels=labels_academic, autopct='%1.1f%%', startangle=140, 
                                            textprops=dict(color="w"))
        
        for i, (text, autotext) in enumerate(zip(texts, autotexts)):
            text.set_text(f"{labels_academic[i]}: ${sizes_academic[i]:,.2f}")
            autotext.set_text(f"{sizes_academic[i]:,.2f} ({autotext.get_text()})")
        
        ax.legend(loc="upper right", title="Categories")
        ax.axis('equal')
        st.pyplot(fig)
        
    # Histograms for Transportation Fees
    with col2:
        
        
        hist_paid = alt.Chart(df_transportation).mark_bar().encode(
            alt.X('Transportation Fees Paid', bin=True),
            y='count()'
        ).properties(
            width=600,  # Increased width
            height=400  # Increased height
        )
        
        st.altair_chart(hist_paid)

except Exception as e:
    st.error(f"An error occurred: {e}")
