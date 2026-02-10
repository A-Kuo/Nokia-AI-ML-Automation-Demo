import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

class CongestionPredictor:
    def __init__(self):
        # RandomForest is robust against noise in telemetry data
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def generate_training_data(self, samples=2000):
        """
        Simulates 5G Network Metrics: 
        - RSRP (Signal Strength in dBm)
        - Connected Users
        - Hour of Day
        """
        np.random.seed(42)
        users = np.random.randint(50, 1000, samples)
        rsrp = np.random.normal(-90, 10, samples) # Normal dist centered at -90dBm
        hour = np.random.randint(0, 24, samples)
        
        # Target Variable: Load Factor (0.0 to 1.0)
        # Logic: High users + Peak hours = High Load. Strong signal mitigates load.
        load = (users / 1200) + (np.sin(hour / 24 * 2 * np.pi) * 0.1) - (rsrp * 0.001)
        load = np.clip(load, 0, 1) 
        
        X = pd.DataFrame({'users': users, 'rsrp': rsrp, 'hour': hour})
        y = load
        return X, y

    def train(self):
        print(">> [AI] Training Model on 5G Telemetry...")
        X, y = self.generate_training_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        print(f">> [AI] Model Trained. Accuracy (R2 Score): {score:.2f}")
        
        # Save model for the automation bot
        joblib.dump(self.model, '5g_brain.pkl')

if __name__ == "__main__":
    ai = CongestionPredictor()
    ai.train()
