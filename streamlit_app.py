import streamlit as st
from sales_data_analysis import process_sales_data

# Streamlit App
def main():
    st.title('Sales Data Analysis')

    # Step 1: File Upload
    uploaded_file = st.file_uploader("Choose a file (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        # Process the uploaded file using backend function
        anomalies = process_sales_data(uploaded_file)

        # Display anomalies detected if any
        st.write("Anomalies detected in the dataset:")
        st.write(anomalies)

if __name__ == '__main__':
    main()