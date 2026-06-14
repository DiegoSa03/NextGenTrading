# NextGen Trading Simulator

A professional, interactive paper trading simulator web application built with Python (Flask) that utilizes real-time market data from Yahoo Finance. This project was developed as the final submission for Stanford's Code in Place program.

## Key Features

- Real-Time Market Data: Leverages the yfinance library to fetch accurate, up-to-date stock pricing directly from the stock market.
- Interactive Dashboard: Features a modern glassmorphism UI, a dark theme, and dynamic doughnut charts powered by Chart.js for portfolio visualization.
- Time Machine Simulator: Allows users to input a past investment amount on a specific ticker over a designated number of years to calculate hypothetical current profits or losses based on historical market data.
- Local Persistence: Automatically saves portfolio holdings and available cash balance to a local portfolio.json file, ensuring user progress is preserved across different sessions.

## Installation and Setup Instructions

Follow these detailed steps to configure and run the application on your local machine:

### 1. Download the Repository
Clone the repository using Git by running the following command in your terminal:
```bash
git clone https://github.com/DiegoSa03/NextGenTrading.git
```
Alternatively, click the Code button on the GitHub page and select Download ZIP. Extract the folder to your preferred location.

### 2. Verify Python Installation
Ensure that Python 3 is installed on your system. Open your terminal or command prompt and verify by running:
```bash
python --version
```

### 3. Navigate to the Project Directory
Change your current working directory to the location where you downloaded the project:
```bash
cd NextGenTrading
```
(Make sure you are inside the folder that contains the app.py file).

### 4. Install Dependencies
The application requires specific external libraries (Flask and yfinance) to function. Install them using the provided requirements file:
```bash
pip install -r requirements.txt
```

### 5. Run the Application Server
Start the backend Python Flask server by executing the main script:
```bash
python app.py
```

### 6. Access the Web Application
Once the terminal indicates that the server is running, open your preferred web browser and navigate to the local host address provided:
http://127.0.0.1:5000/

The dashboard will load, and you can begin executing simulated trades immediately.
