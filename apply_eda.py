import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime

# Function to load data from MySQL
def load_data_from_mysql():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='smart_parking_system'
        )
        query = "SELECT * FROM traffic"
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None
    
            

# Load the data
data = load_data_from_mysql()

# Prepare Data for Modeling
if data is not None:
    data['time'] = pd.to_datetime(data['time'])
    data['hour'] = data['time'].dt.hour
    data['day_of_week'] = data['time'].dt.dayofweek
    data = data.drop(columns=['time'])
    
    X = data[['available_in_parking_1', 'available_in_parking_2', 'hour', 'day_of_week']]
    y = data['nearest_in_parking_1']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    coef = model.coef_
    intercept = model.intercept_

    # Create a function to generate base64 encoded images
    def fig_to_base64(fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

    # Create EDA plots
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.histplot(data['available_in_parking_1'], kde=True, color='blue', label='Parking 1', ax=ax1)
    sns.histplot(data['available_in_parking_2'], kde=True, color='green', label='Parking 2', ax=ax1)
    ax1.set_title('Distribution of Available Parking Spaces')
    ax1.set_xlabel('Available Spaces')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    dist_plot = fig_to_base64(fig1)

    fig2, ax2 = plt.subplots(figsize=(10, 8))
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax2)
    ax2.set_title('Correlation Matrix')
    corr_plot = fig_to_base64(fig2)

    fig3, ax3 = plt.subplots(figsize=(14, 7))
    ax3.plot(data['time'], data['available_in_parking_1'], label='Parking 1')
    ax3.plot(data['time'], data['available_in_parking_2'], label='Parking 2')
    ax3.set_title('Time Series of Available Parking Spaces')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Available Spaces')
    ax3.legend()
    time_series_plot = fig_to_base64(fig3)

# Create a Dash application
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Smart Parking System Dashboard"),
    html.Div([
        html.H2("Exploratory Data Analysis (EDA)"),
        html.Div([
            html.Img(src=f'data:image/png;base64,{dist_plot}', style={'width': '100%', 'height': 'auto'}),
            html.Img(src=f'data:image/png;base64,{corr_plot}', style={'width': '100%', 'height': 'auto'}),
            html.Img(src=f'data:image/png;base64,{time_series_plot}', style={'width': '100%', 'height': 'auto'}),
        ])
    ]),
    html.Div([
        html.H2("Linear Regression Model Results"),
        html.P(f"Mean Squared Error: {mse:.2f}"),
        html.P(f"Coefficients: {', '.join([f'{coef:.2f}' for coef in coef])}"),
        html.P(f"Intercept: {intercept:.2f}")
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
