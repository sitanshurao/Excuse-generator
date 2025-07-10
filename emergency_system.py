import time
from faker import Faker

class EmergencySystem:
    def __init__(self):
        self.fake = Faker()

    def simulate_emergency_call(self, contact_name):
        print(f"Simulating emergency call from {contact_name}...")
        time.sleep(2)
        print("Ring... Ring...")
        time.sleep(2)
        print(f"{contact_name}: Hello? I need help with an emergency!")
        time.sleep(1)
        print("Call ended.")

    def send_emergency_text(self, contact_name, excuse):
        message = f"URGENT from {contact_name}: {excuse} Can you help?"
        print(f"Sending emergency text: {message}")
        return message