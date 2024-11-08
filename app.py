import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import numpy as np
import random
import time
import threading
import queue


class DataStreamException(Exception):
    """Custom exception to handle invalid data in the stream."""
    pass


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
def data_stream_simulation(data_queue):
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
            # Generation of sinusoidal seasonal pattern with added random noise
            seasonality = 10 * np.sin(2 * np.pi * t / 50)
            noise = np.random.normal(0, 2)
            value = 50 + seasonality + noise

            # Randomly injecting anomalies (5% chance)
            if random.random() < 0.05:
                value += np.random.normal(30, 10)
          
            validate_data(value)

            data_queue.put(value)

            t += 1
            # NOTE-: Here simulating real-time delay
            time.sleep(0.1)
        except DataStreamException as e:
            print(f"Error in data stream: {e}")
            continue

class RollingZScoreAnomalyDetector:
    """
    Anomaly detection using a Z-score-based approach with a rolling window.

    Attributes:
        window_size (int): Number of recent points considered in the rolling window.
        threshold (float): Z-score threshold for anomaly detection.
        window (deque): Rolling window of recent data points.
    """
    def __init__(self, window_size=30, threshold=3.5):
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

            self.window.append(value)

            # Ensuring we have enough data points to calculate Z-score
            if len(self.window) < 2:
                return False

            # Calculation of the rolling mean and standard deviation
            mean = np.mean(self.window)
            std_dev = np.std(self.window)

            if std_dev == 0:
                std_dev = 1e-6

            z_score = (value - mean) / std_dev

            return abs(z_score) > self.threshold
        except DataStreamException as e:
            print(f"Error in anomaly detection: {e}")
            return False

# --- Initialization of Variables ---
data_queue = queue.Queue()
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


# --- Callback function for Real-time Graph Updates ---
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

    for _ in range(5):  
        if not data_queue.empty():

            value = data_queue.get()
            idx = len(data_x) + 1

            # Updated data points
            data_x.append(idx)
            data_y.append(value)

            # Responsible for detection of anomalies
            if detector.update_and_detect(value):
                anomaly_x.append(idx)
                anomaly_y.append(value)

    # Keeping anomaly lists within recent bounds
    if len(anomaly_x) > 200:
        anomaly_x = anomaly_x[-200:]
        anomaly_y = anomaly_y[-200:]

    # NOTE-: Defining the traces here
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

# --- Starting the Data Stream Simulation in a Separate Thread ---
def start_data_stream():
    data_stream_simulation(data_queue)


def run_dash_app():
    """
    Runs the Dash application in a separate thread to display real-time graph updates.

    Starts the Dash app server with debug mode disabled to prevent automatic reloading.
    """
    app.run_server(debug=True, use_reloader=False)

if __name__ == '__main__':

    data_thread = threading.Thread(target=start_data_stream)
    data_thread.daemon = True
    data_thread.start()

    # Starting the Dash app in a separate thread to keep it non-blocking(asynchronous)
    dash_thread = threading.Thread(target=run_dash_app)
    dash_thread.daemon = True
    dash_thread.start()

    while True:
        time.sleep(1)