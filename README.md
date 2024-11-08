# Real-Time Anomaly Detection and Visualization

This project implements a real-time anomaly detection and visualization system in Python 3.x. It simulates a data stream, identifies anomalies based on a rolling Z-score algorithm, and displays the results using a Dash-based web interface. The system is designed for ease of testing, demonstration, and future adaptation to various data sources.

---

## Table of Contents

- [Overview](#overview)
- [Algorithm](#algorithm)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Program](#running-the-program)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contact](#contact)

---

## Overview

This project detects anomalies in a data stream using a rolling Z-score-based approach. It visualizes the data stream in real-time using a Dash web app, where anomalies are highlighted in red on a line plot. 

The simulated data stream includes seasonal patterns, random noise, and occasional anomalies, mimicking real-world scenarios.

---

## Algorithm

The **Rolling Z-Score Anomaly Detector** calculates the Z-score for each incoming data point based on a rolling window of past values. When the absolute Z-score exceeds a set threshold, the data point is flagged as an anomaly.

### Why Z-Score?
The Z-score approach effectively normalizes data, allowing the system to adapt to various types of data streams. This algorithm performs well in real-time scenarios as it minimizes false positives while detecting significant deviations.

---

## Features

- **Data Simulation**: Generates a sinusoidal seasonal pattern with noise and occasional anomalies.
- **Real-Time Detection**: Uses a rolling Z-score algorithm to identify anomalies.
- **Interactive Visualization**: Displays data in real-time using Dash and Plotly, marking anomalies in red.
- **Customizable Thresholds**: Adjust the rolling window and Z-score threshold to refine detection.

---

## Requirements

- Python 3.x
- Libraries:
  - Dash
  - Plotly
  - NumPy

See [Installation](#installation) for setup details.

---

## Installation

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Dependencies**:
    Run the following command to install required libraries:
    ```bash
    pip install -r requirements.txt
    ```

---

## Running the Program

After installing the dependencies, start the application by running:

```bash
python app.py

## How to View the Visualization

1. Open your browser.
2. Go to `http://127.0.0.1:8050` to view the real-time visualization.

---

## Project Structure

- **app.py**: Main application script containing data stream simulation, anomaly detection, and real-time visualization.
- **requirements.txt**: Lists all the dependencies required to run the project.

---

## Code Overview

### Key Sections of the Code

- **Data Stream Simulation**: Generates synthetic data with seasonal, random noise, and anomalies. The function `data_stream_simulation` iterates through data points, introducing a 0.1-second delay to simulate real-time data.
  
- **Anomaly Detection**: Uses the `RollingZScoreAnomalyDetector` class, which maintains a rolling window of recent data points to calculate mean and standard deviation. An anomaly is flagged when the Z-score exceeds a specified threshold.

- **Real-Time Visualization**: Implemented with Dash, using a `dcc.Graph` component to display data and detected anomalies in real time. Data is updated every 500ms via `dcc.Interval`.

---

## Customization

- **Adjusting Detection Sensitivity**:
  - Modify `window_size` and `threshold` in `RollingZScoreAnomalyDetector` for tuning detection sensitivity.

- **Changing Visualization Update Frequency**:
  - Adjust the `dcc.Interval` property in the Dash app layout to control how frequently the graph updates.

---

## Troubleshooting

- **"Error displaying widget"**: Ensure all dependencies are correctly installed, especially `dash` and `plotly`.
  
- **No Visualization on Terminal**: This code is designed for a web browser. Please ensure you are viewing `http://127.0.0.1:8050` in a supported browser.

---

## License

This project is licensed under the MIT License.

---

## Contact

For any issues or questions, feel free to open an issue on this repository.


