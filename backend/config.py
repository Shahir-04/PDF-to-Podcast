import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-4-turbo-preview"
    TTS_MODEL = "tts-1"
    TTS_VOICE = "alloy"  # Options: alloy, echo, fable, onyx, nova, shimmer
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7
    CHUNK_SIZE = 2000  # Characters per chunk for processing
    
config = Config()