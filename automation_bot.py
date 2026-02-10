import joblib
import json
import time
import pandas as pd
from colorama import Fore, Style, init

init(autoreset=True)

class NetworkAutomator:
    def __init__(self):
        try:
            self.model = joblib.load('5g_brain.pkl')
            print(Fore.GREEN + "[SYSTEM] AI Model Loaded.")
        except FileNotFoundError:
            print(Fore.RED + "[ERROR] Model not found. Run network_brain.py first.")

    def analyze_and_act(self, tower_metrics):
        """
        Closed-Loop Automation Logic:
        1. Predict Load
        2. IF Load > Threshold -> AUTOMATE CONFIG CHANGE
        """
        df = pd.DataFrame([tower_metrics])
        predicted_load = self.model.predict(df)[0]
        
        print(f"\n[ANALYSIS] Tower ID: {tower_metrics['tower_id']}")
        print(f"   Metrics: {tower_metrics['users']} Users, {tower_metrics['rsrp']:.1f} dBm")
        print(f"   Predicted Load: {predicted_load:.2%}")

        if predicted_load > 0.80:
            self.trigger_optimization(tower_metrics['tower_id'], predicted_load)
        else:
            print(Fore.CYAN + "   Status: Optimal. No action needed.")

    def trigger_optimization(self, tower_id, load):
        print(Fore.YELLOW + "   [ALERT] Congestion Detected! Initiating Automated Fix...")
        
        # Decision Logic: Adjust Antenna Tilt based on severity
        new_tilt = 6 if load > 0.9 else 3
        power_boost = 2 
        
        # Generate Configuration Payload (Simulating a NETCONF push)
        config_payload = {
            "target_node": f"gnb-{tower_id}",
            "timestamp": time.time(),
            "operations": [
                {"action": "SET_REMOTE_electrical_tilt", "value": f"-{new_tilt}"},
                {"action": "SET_transmission_power", "value": f"+{power_boost}dB"}
            ]
        }
        
        # Save payload to log (simulating the API call)
        filename = f"config_change_{tower_id}.json"
        with open(filename, 'w') as f:
            json.dump(config_payload, f, indent=2)
            
        print(Fore.GREEN + f"   [SUCCESS] Optimization Applied. Config saved to {filename}")

if __name__ == "__main__":
    bot = NetworkAutomator()
    
    # Test Scenario 1: Healthy Tower
    bot.analyze_and_act({'tower_id': 'T-101', 'users': 200, 'rsrp': -80, 'hour': 10})
    
    # Test Scenario 2: Congested Tower (Triggers Automation)
    bot.analyze_and_act({'tower_id': 'T-505', 'users': 980, 'rsrp': -110, 'hour': 18})
