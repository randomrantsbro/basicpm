# gemini_client.py

import os
import google.generativeai as genai


class GeminiClient:
    def __init__(self):
        api_key = "AIzaSyBrwqKD1ZwvEcZrgN9YpsH1RCkC-kMNVyg"
        if not api_key:
            raise ValueError("GENAI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash',
                                           generation_config={"response_mime_type": "application/json"})

    def generate_content(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"Error occurred: {e}"
