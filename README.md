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

