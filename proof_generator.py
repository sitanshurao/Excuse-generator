from faker import Faker
from PIL import Image, ImageDraw, ImageFont
import random
import datetime

class ProofGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_document(self, excuse_type):
        # Generate fake document proof
        doc_type = random.choice(["Medical Certificate", "Official Letter", "Receipt"])
        content = {
            "title": doc_type,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "name": self.fake.name(),
            "details": f"This document certifies that the bearer was unable to attend due to {excuse_type}.",
            "signature": self.fake.name() + ", MD" if doc_type == "Medical Certificate" else self.fake.name()
        }
        return content

    def generate_chat_screenshot(self, excuse):
        # Create a simple image that looks like a chat screenshot
        img = Image.new('RGB', (400, 200), color=(229, 229, 229))
        d = ImageDraw.Draw(img)
        
        # Add some fake chat content
        font = ImageFont.load_default()
        d.text((10,10), "You: Hey, I can't make it today", fill=(0,0,0), font=font)
        d.text((10,40), "Friend: Why not?", fill=(0,0,0), font=font)
        d.text((10,70), f"You: {excuse}", fill=(0,0,0), font=font)
        d.text((10,100), "Friend: Oh no! Hope everything is OK", fill=(0,0,0), font=font)
        
        return img

    def generate_location_log(self):
        # Generate fake location data
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "latitude": self.fake.latitude(),
            "longitude": self.fake.longitude(),
            "address": self.fake.address()
        }