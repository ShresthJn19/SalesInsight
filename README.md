# Sales Data Analysis

This project is a **Sales Data Analysis** tool developed using **Streamlit** and **Python**, allowing users to upload their sales data, clean it, visualize it, and optionally detect anomalies in the sales trends.

## Features

- Upload CSV or Excel files with sales data.
- Data cleaning and preprocessing, including handling missing values and formatting.
- Interactive data visualization for:
  - Total Sales Over Time
  - Sales by Category
  - Sales by State
  - Order Status Summary
- Optional anomaly detection using **Isolation Forest** for identifying unusual sales behavior.
- Simple and interactive web interface built with **Streamlit**.

## Technologies Used

- **Python**: Core programming language.
- **Streamlit**: For building the web interface.
- **Pandas**: For data manipulation and cleaning.
- **Matplotlib & Seaborn**: For creating data visualizations.
- **Scikit-learn**: For anomaly detection using Isolation Forest.

## Getting Started

### Prerequisites

Make sure you have **Python 3.x** installed on your machine. You can download it from [here](https://www.python.org/downloads/).

### Installation

1. Clone this repository to your local machine:

   ```bash
     git clone https://github.com/yourusername/sales-data-analysis.git

2.	Navigate into the project directory:
   
     ```bash
      cd sales-data-analysis

3.	Set up a virtual environment (optional but recommended):

     ```bash
    python -m venv .venv
    source .venv/bin/activate  # For Linux/macOS
    .venv\Scripts\activate     # For Windows

4.	Install the required Python packages:

     ```bash
     pip install -r requirement.txt
     
### Running the App

1.	Start the Streamlit app:
   
     ```bash
      streamlit run streamlit_app.py
   
2.	Upload your sales dataset (CSV or Excel), select the desired visualization, and view the analysis results interactively.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
