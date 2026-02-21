import os
import requests
import uuid
from dotenv import load_dotenv

class MedicalTranslator:
    """
    Azure Translator for medical text translation
    Supports 100+ languages
    """
    
    def __init__(self):
        load_dotenv()
        self.key = os.getenv("TRANSLATOR_KEY")
        self.endpoint = os.getenv("TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
        self.region = os.getenv("TRANSLATOR_REGION", "global")
    
    def translate(self, text: str, from_lang: str = "en", to_lang: str = "tr") -> str:
        """
        Translate medical text
        
        Args:
            text: Text to translate
            from_lang: Source language code (e.g., 'en')
            to_lang: Target language code (e.g., 'tr', 'de', 'fr')
        
        Returns:
            Translated text
        
        Example:
            translator = MedicalTranslator()
            turkish = translator.translate("Patient has diabetes", "en", "tr")
        """
        path = '/translate'
        url = self.endpoint + path
        
        params = {
            'api-version': '3.0',
            'from': from_lang,
            'to': to_lang
        }
        
        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        
        body = [{'text': text}]
        
        try:
            response = requests.post(url, params=params, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()
            return result[0]['translations'][0]['text']
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        path = '/detect'
        url = self.endpoint + path
        
        params = {'api-version': '3.0'}
        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json'
        }
        body = [{'text': text}]
        
        try:
            response = requests.post(url, params=params, headers=headers, json=body)
            result = response.json()
            return result[0]['language']
        except Exception as e:
            return f"Detection error: {str(e)}"


# Test
if __name__ == "__main__":
    translator = MedicalTranslator()
    
    # Medical text examples
    examples = [
        "Patient has Type 2 Diabetes and hypertension.",
        "Prescribed Metformin 500mg twice daily.",
        "Blood pressure: 140/90 mmHg. Heart rate: 82 bpm."
    ]
    
    print("=" * 70)
    print("MEDICAL TEXT TRANSLATION")
    print("=" * 70)
    
    for text in examples:
        print(f"\n📝 Original (EN): {text}")
        print(f"🇹🇷 Turkish: {translator.translate(text, 'en', 'tr')}")
        print(f"🇩🇪 German: {translator.translate(text, 'en', 'de')}")