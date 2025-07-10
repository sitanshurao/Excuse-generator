import google.generativeai as genai
from config import GEMINI_API_KEY, DEFAULT_LANGUAGE

class ExcuseGenerator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.language = DEFAULT_LANGUAGE

    def generate_excuse(self, scenario, urgency="medium", tone="professional"):
        prompt = f"""
        Generate a {tone}-tone excuse for a {scenario} scenario. 
        The urgency level is {urgency}. 
        The excuse should sound natural and believable.
        Respond in {self.language} language.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating excuse: {str(e)}"

    def set_language(self, language_code):
        self.language = language_code