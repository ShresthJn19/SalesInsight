import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
import streamlit as st

# Function to load the dataset
def load_data(file):
    try:
        df = pd.read_csv(file)
    except:
        df = pd.read_excel(file)
    return df

# Function to clean the dataset
def clean_data(df):
    # Drop unnecessary or unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Check for missing values and handle them
    df = df.dropna(subset=['Amount', 'Date', 'Qty'])  # Drop rows with essential missing values
    
    # Parse Date column
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Fill missing values (optional)
    df.fillna(method='ffill', inplace=True)  # Forward fill as an example
    
    # Ensure correct data types
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')
    
    return df

# Function to generate basic visualizations
def visualize_sales_over_time(df):
    plt.figure(figsize=(10, 5))
    df.groupby('Date')['Amount'].sum().plot(kind='line')
    plt.title('Total Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sales Amount')
    st.pyplot(plt)

def visualize_sales_by_category(df):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df['Category'].value_counts().index, y=df['Category'].value_counts().values)
    plt.title('Sales by Category')
    plt.xlabel('Category')
    plt.ylabel('Sales Count')
    plt.xticks(rotation=45)
    st.pyplot(plt)

def visualize_sales_by_state(df):
    plt.figure(figsize=(10, 8))  # Adjusted the figure size for better visualization
    sns.countplot(y=df['ship-state'], order=df['ship-state'].value_counts().index)
    plt.title('Sales by State')
    plt.xlabel('Count')
    plt.ylabel('State')
    plt.yticks(rotation=0, fontsize=10)  # Make sure y-axis labels are horizontal with proper font size
    plt.tight_layout()  # Ensures everything fits without overlap
    st.pyplot(plt)

def visualize_order_status(df):
    plt.figure(figsize=(10, 6))  # Increased figure size for better visualization
    sns.countplot(x=df['Status'])
    plt.title('Order Status Summary')
    plt.xlabel('Order Status')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels and align them to the right
    plt.tight_layout()  # Adjust layout to prevent overlap
    st.pyplot(plt)

# Function for anomaly detection using Isolation Forest (optional)
def detect_anomalies(df):
    model = IsolationForest(contamination=0.01)
    df['anomaly'] = model.fit_predict(df[['Amount']])
    
    anomalies = df[df['anomaly'] == -1]
    
    plt.figure(figsize=(10, 5))
    plt.scatter(df['Date'], df['Amount'], color='blue', label='Normal')
    plt.scatter(anomalies['Date'], anomalies['Amount'], color='red', label='Anomalies')
    plt.title('Anomaly Detection in Sales Amount')
    plt.xlabel('Date')
    plt.ylabel('Sales Amount')
    plt.legend()
    st.pyplot(plt)

    return anomalies

# Main function that ties everything together
def process_sales_data(file):
    # Load and clean the data
    df = load_data(file)
    df = clean_data(df)
    
    # Select a graph to visualize
    graph_option = st.selectbox(
        "Select a graph to visualize",
        ("Total Sales Over Time", "Sales by Category", "Sales by State", "Order Status Summary", "Anomaly Detection")
    )
    
    # Perform the visualizations based on user selection
    if graph_option == "Total Sales Over Time":
        visualize_sales_over_time(df)
    elif graph_option == "Sales by Category":
        visualize_sales_by_category(df)
    elif graph_option == "Sales by State":
        visualize_sales_by_state(df)
    elif graph_option == "Order Status Summary":
        visualize_order_status(df)
    elif graph_option == "Anomaly Detection":
        anomalies = detect_anomalies(df)
        return anomalies

    return pd.DataFrame()  # Return empty DataFrame if no anomalies detected