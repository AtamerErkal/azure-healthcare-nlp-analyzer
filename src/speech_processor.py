import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

class SpeechProcessor:
    """
    Azure Speech Service for medical audio transcription
    Speech-to-Text for doctor voice notes
    """
    
    def __init__(self):
        load_dotenv()
        key = os.getenv("SPEECH_KEY")
        region = os.getenv("SPEECH_REGION")
        
        if not key or not region:
            raise ValueError("SPEECH_KEY and SPEECH_REGION must be set")
        
        self.speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        # Set language (you can change to other languages)
        self.speech_config.speech_recognition_language = "en-US"
    
    def audio_to_text(self, audio_file_path: str) -> dict:
        """
        Convert audio file to text
        
        Args:
            audio_file_path: Path to WAV audio file
        
        Returns:
            {
                "text": "transcribed text",
                "success": True/False,
                "error": "error message if failed"
            }
        
        Example:
            processor = SpeechProcessor()
            result = processor.audio_to_text("doctor_notes.wav")
            print(result["text"])
        """
        try:
            audio_config = speechsdk.AudioConfig(filename=audio_file_path)
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return {
                    "text": result.text,
                    "success": True,
                    "error": None
                }
            elif result.reason == speechsdk.ResultReason.NoMatch:
                return {
                    "text": "",
                    "success": False,
                    "error": "No speech could be recognized"
                }
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                return {
                    "text": "",
                    "success": False,
                    "error": f"Speech recognition canceled: {cancellation.reason}"
                }
        
        except Exception as e:
            return {
                "text": "",
                "success": False,
                "error": str(e)
            }
    
    def microphone_to_text(self) -> dict:
        """
        Real-time microphone transcription
        
        Returns:
            {
                "text": "transcribed text",
                "success": True/False,
                "error": "error message if failed"
            }
        
        Example:
            processor = SpeechProcessor()
            print("🎤 Speak now...")
            result = processor.microphone_to_text()
            print(result["text"])
        """
        try:
            recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
            
            print("🎤 Speak now... (listening)")
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return {
                    "text": result.text,
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "text": "",
                    "success": False,
                    "error": "No speech recognized"
                }
        
        except Exception as e:
            return {
                "text": "",
                "success": False,
                "error": str(e)
            }
    
    def continuous_recognition(self, audio_file_path: str) -> list:
        """
        Continuous recognition for longer audio files
        
        Args:
            audio_file_path: Path to audio file
        
        Returns:
            List of recognized text segments
        """
        recognized_texts = []
        
        def recognized_handler(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                recognized_texts.append(evt.result.text)
        
        try:
            audio_config = speechsdk.AudioConfig(filename=audio_file_path)
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            recognizer.recognized.connect(recognized_handler)
            recognizer.start_continuous_recognition()
            
            import time
            time.sleep(10)  # Adjust based on audio length
            
            recognizer.stop_continuous_recognition()
            
            return recognized_texts
        
        except Exception as e:
            print(f"Error: {e}")
            return []


# Test
if __name__ == "__main__":
    processor = SpeechProcessor()
    
    print("=" * 70)
    print("AZURE SPEECH PROCESSOR")
    print("=" * 70)
    print("\n✅ Speech processor initialized successfully!")
    print("\n📋 Available methods:")
    print("  1. audio_to_text(file_path) → Transcribe audio file")
    print("  2. microphone_to_text() → Real-time microphone input")
    print("  3. continuous_recognition(file_path) → Long audio files")
    
    print("\n💡 Use case: Convert doctor voice notes to text for EHR")
    print("   Example: 'Patient complains of chest pain. BP 140/90. Prescribed aspirin.'")
    
    # Uncomment to test microphone (requires microphone access)
    # print("\n🎤 Testing microphone (say something):")
    # result = processor.microphone_to_text()
    # if result["success"]:
    #     print(f"✅ You said: {result['text']}")
    # else:
    #     print(f"❌ Error: {result['error']}")