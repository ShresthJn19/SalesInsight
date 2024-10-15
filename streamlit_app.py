import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from database import validate_user, register_user, log_analysis

# Custom styling
def add_custom_style():
    st.markdown("""
        <style>
        .main {background-color: #f0f2f6; font-family: 'Roboto', sans-serif;}
        h1, h2, h3 {color: #4B7BEC;}
        .stButton button {background-color: #4B7BEC; color: white;}
        </style>
        """, unsafe_allow_html=True)

# Register new user
def register():
    add_custom_style()
    st.title('🔑 Register a New Account')
    username = st.text_input('Choose a Username')
    password = st.text_input('Choose a Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    if st.button('Register'):
        if password == confirm_password:
            if register_user(username, password):
                st.success('Account created successfully! You can now log in.')
                st.session_state['page'] = 'login'
            else:
                st.error('Username already exists. Please choose a different username.')
        else:
            st.error('Passwords do not match.')

# Login form and authentication
def login():
    add_custom_style()
    st.title('🔒 Login to Access the Dashboard')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if validate_user(username, password):  # Using validate_user from database.py
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['page'] = 'upload'
        else:
            st.error('Invalid username or password')

    # Link to registration page
    if st.button('Create a New Account'):
        st.session_state['page'] = 'register'

# Logout function
def logout():
    if st.button('Logout'):
        st.session_state['logged_in'] = False
        st.session_state['page'] = 'login'

# Upload instructions
def upload_instructions():
    st.write("### Instructions for Uploading Data")
    st.info("""
        Your dataset should contain the following columns:
        - **Order ID**
        - **Date** (in YYYY-MM-DD format)
        - **Status**
        - **Category**
        - **Amount** (numeric)
        - **Qty** (numeric)
        - **ship-state** (state name)
        - **ship-city**
    """)

# Function to load and clean data
def load_data(file):
    df = pd.read_csv(file)
    df = df.dropna(subset=['Amount', 'Date', 'Qty'])
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')
    return df

# Display KPIs
def display_kpis(df):
    st.write("### Key Performance Indicators (KPIs)")
    total_rows = df.shape[0]
    num_products = df['Category'].nunique()
    num_states = df['ship-state'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", total_rows)
    col2.metric("Number of Products", num_products)
    col3.metric("Number of States", num_states)

    # Log analysis to the database
    log_analysis(st.session_state['username'], total_rows, num_products, num_states)

# Function to visualize the data
def visualize_data(df):
    st.write("## Sales Data Analysis")
    # Total Sales Over Time
    plt.figure(figsize=(10, 5))
    df.groupby('Date')['Amount'].sum().plot(kind='line')
    plt.title('Total Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sales Amount')
    st.pyplot(plt)

    # Sales by Category
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df['Category'].value_counts().index, y=df['Category'].value_counts().values)
    plt.title('Sales by Category')
    plt.xlabel('Category')
    plt.ylabel('Sales Count')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Sales by State
    plt.figure(figsize=(10, 8))
    sns.countplot(y=df['ship-state'], order=df['ship-state'].value_counts().index)
    plt.title('Sales by State')
    plt.xlabel('Count')
    plt.ylabel('State')
    st.pyplot(plt)

# Upload and analysis page
def upload_page():
    st.title('📊 Upload Sales Data for Analysis')
    upload_instructions()
    uploaded_file = st.file_uploader("Upload your sales data (CSV)", type=["csv"])

    if uploaded_file:
        df = load_data(uploaded_file)
        st.session_state['df'] = df
        st.session_state['page'] = 'dashboard'

# Dashboard page
def dashboard_page():
    st.title('📊 Dashboard')
    if 'df' in st.session_state:
        df = st.session_state['df']
        display_kpis(df)
        visualize_data(df)
    logout()

# Main app function
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        if st.session_state['page'] == 'upload':
            upload_page()
        elif st.session_state['page'] == 'dashboard':
            dashboard_page()
    elif st.session_state['page'] == 'register':
        register()
    else:
        login()

if __name__ == '__main__':
    main()
