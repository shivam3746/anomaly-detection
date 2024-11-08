import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import numpy as np
import random
import time
import threading

# --- Custom Exception for Data Stream ---
class DataStreamException(Exception):
    """Custom exception to handle invalid data in the stream."""
    pass

# --- Data Validation ---
def validate_data(value):
    """
    Validating incoming data to ensure it is a numeric type.

    Args:
        value (float or int): The data value to validate.

    Returns:
        bool: True if valid, otherwise raises DataStreamException.

    Raises:
        DataStreamException: If value is not a number.
    """
    if not isinstance(value, (int, float)):
        raise DataStreamException(f"Invalid data: {value} is not a numeric type.")
    return True

# --- Data Stream Simulation ---
def data_stream_simulation():
    """
    Simulates a real-time data stream with seasonality, noise, and random anomalies.

    Yields:
        float: Simulated data stream value with seasonality, noise, and occasional anomalies.

    Raises:
        DataStreamException: If the generated value is invalid.
    """
    t = 0
    while True:
        try:
            # Generates sinusoidal seasonal pattern with added random noise
            seasonality = 10 * np.sin(2 * np.pi * t / 50)
            noise = np.random.normal(0, 2)
            value = 50 + seasonality + noise

            # Randomly injecting anomalies (5% chance)
            if random.random() < 0.05:
                value += np.random.normal(30, 10)  # Inject anomaly

            # Validating data to ensure correctness
            validate_data(value)

            t += 1
            yield value
            time.sleep(0.1)  # Simulate real-time delay
        except DataStreamException as e:
            print(f"Error in data stream: {e}")
            continue

# --- Rolling Z-Score Anomaly Detector ---
class RollingZScoreAnomalyDetector:
    """
    Anomaly detection using a Z-score-based approach with a rolling window.

    Attributes:
        window_size (int): Number of recent points considered in the rolling window.
        threshold (float): Z-score threshold for anomaly detection.
        window (deque): Rolling window of recent data points.
    """
    def __init__(self, window_size=30, threshold=3):
        """
        Initialization of the anomaly detector with a rolling window and Z-score threshold.

        Args:
            window_size (int): Size of the rolling window.
            threshold (float): Z-score threshold for detecting anomalies.
        """
        self.window = deque(maxlen=window_size)
        self.threshold = threshold

    def update_and_detect(self, value):
        """
        Updates the rolling window with a new value and detect anomalies.

        Args:
            value (float): The new data point to add to the rolling window.

        Returns:
            bool: True if the new value is an anomaly, False otherwise.
        """
        try:
            # Validation of value before processing
            validate_data(value)

            # Addition of the new value to the window
            self.window.append(value)

            # Ensuring we have enough data points to calculate Z-score
            if len(self.window) < 2:
                return False  # Not enough data for an anomaly check

            # Calculation of the rolling mean and standard deviation
            mean = np.mean(self.window)
            std_dev = np.std(self.window)

            # Handling of potential division by zero in standard deviation
            if std_dev == 0:
                std_dev = 1e-6

            # Computation of Z-score
            z_score = (value - mean) / std_dev

            # Returning True if the Z-score exceeds the anomaly threshold
            return abs(z_score) > self.threshold
        except DataStreamException as e:
            print(f"Error in anomaly detection: {e}")
            return False

# --- Initialization of Variables ---
data_x = deque(maxlen=200)
data_y = deque(maxlen=200)
anomaly_x = []
anomaly_y = []
detector = RollingZScoreAnomalyDetector(window_size=30, threshold=3)

# --- Dash App Setup ---
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Real-time Data Stream with Anomaly Detection"),
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(id='graph-update', interval=500, n_intervals=0)
])

# --- Callback for Real-time Graph Updates ---
@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
def update_graph(n):
    """
    Updates the graph in real time with data from the stream and detected anomalies.

    Args:
        n (int): The interval counter for updates.

    Returns:
        dict: The figure with updated traces for data stream and anomalies.
    """
    global data_x, data_y, anomaly_x, anomaly_y

    for _ in range(5):  # Update with multiple points per callback for smoother animation
        idx = len(data_x) + 1
        value = next(data_stream_simulation())

        # Data points Update
        data_x.append(idx)
        data_y.append(value)

        # Detecting anomalies for visualizing
        if detector.update_and_detect(value):
            anomaly_x.append(idx)
            anomaly_y.append(value)

    # Defining traces
    data_trace = go.Scatter(x=list(data_x), y=list(data_y), name="Data Stream", mode="lines")
    anomaly_trace = go.Scatter(x=anomaly_x, y=anomaly_y, name="Anomalies", mode="markers", marker=dict(color="red", size=10))

    return {
        'data': [data_trace, anomaly_trace],
        'layout': go.Layout(
            xaxis=dict(range=[max(0, len(data_x) - 200), len(data_x)]),
            yaxis=dict(range=[min(data_y) - 10, max(data_y) + 10]),
            title="Real-time Data Stream with Anomaly Detection"
        )
    }

# --- Running the Dash App in a Separate Thread ---
def run_dash_app():
    """
    Runs the Dash application in a separate thread to display real-time graph updates.

    Starts the Dash app server with debug mode disabled to prevent automatic reloading.
    """
    app.run_server(debug=True, use_reloader=False)

if __name__ == '__main__':
    # Starting the Dash app in a separate thread to keep it non-blocking(asynchronous)
    dash_thread = threading.Thread(target=run_dash_app)
    dash_thread.start()
