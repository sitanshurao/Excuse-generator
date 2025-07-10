import google.generativeai as genai
from config import GEMINI_API_KEY

class ApologyGenerator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_apology(self, situation, tone="professional"):
        prompt = f"""
        Generate a {tone} apology for the following situation: {situation}.
        The apology should sound sincere and include elements that would make the recipient more likely to forgive.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating apology: {str(e)}"