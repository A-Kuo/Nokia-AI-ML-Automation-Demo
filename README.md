# NetOps-AI: Closed-Loop 5G Automation Suite

![Python](https://img.shields.io/badge/Python-Automation-blue)
![ML](https://img.shields.io/badge/AI-ScikitLearn-orange)
![Status](https://img.shields.io/badge/Status-Prototype-green)

### 🚀 Overview
**NetOps-AI** is a self-healing network prototype designed to automate 5G cell tower optimization. It uses Machine Learning to predict congestion events and an automation bot to apply configuration changes (antenna tilt/power) in real-time, reducing the need for manual intervention.

### 🛠 Key Features
* **AI-Driven Prediction:** Random Forest model predicts load factor based on RSRP and user density.
* **Closed-Loop Automation:** Python bot automatically generates and "pushes" JSON config patches when anomalies are detected.
* **Audit Dashboard:** React/TypeScript interface for monitoring automated actions.

### 📂 Project Structure
* `network_brain.py`: Trains the AI model on synthetic 5G telemetry data.
* `automation_bot.py`: The core automation engine that acts on AI predictions.
* `dashboard.tsx`: Frontend component for visualization.

### ⚡ Usage
1.  **Install requirements:** `pip install -r requirements.txt`
2.  **Train the Brain:** `python network_brain.py`
3.  **Run Automation:** `python automation_bot.py`
