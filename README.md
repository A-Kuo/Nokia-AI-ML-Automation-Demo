# NetOps-AI: Closed-Loop 5G Automation Suite

![Python](https://img.shields.io/badge/Python-Automation-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-Vanilla-blue)
![Status](https://img.shields.io/badge/Status-Prototype-green)

### 🚀 Overview
**NetOps-AI** is a self-healing network prototype designed to automate 5G cell tower optimization. It uses Machine Learning to predict congestion events and an automation bot to apply configuration changes in real-time.

**Design Philosophy:** The frontend is built with **Vanilla TypeScript** (no heavy frameworks) to ensure the internal tooling remains lightweight, fast, and dependency-free.

### 🛠 Tech Stack
* **Automation:** Python (Custom scripting for config generation)
* **Machine Learning:** Scikit-Learn (Random Forest for load prediction)
* **Frontend:** TypeScript & HTML5 (Lightweight Dashboard)
* **Data:** NumPy & Pandas (Telemetry simulation)

### 📂 Project Structure
* `network_brain.py`: Trains the AI model on synthetic 5G telemetry data.
* `automation_bot.py`: The core automation engine that acts on AI predictions.
* `dashboard.ts`: Type-safe logic for the audit dashboard.

### ⚡ Usage
1.  **Install Python requirements:** `pip install -r requirements.txt`
2.  **Train the Brain:** `python network_brain.py`
3.  **Run Automation:** `python automation_bot.py`
4.  **View Dashboard:** Compile the TS (`tsc dashboard.ts`) and open `index.html`.
