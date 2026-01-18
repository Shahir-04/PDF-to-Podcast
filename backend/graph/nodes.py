from langchain_openai import ChatOpenAI
from backend.config import config
from backend.utils.prompts import SUMMARIZE_PROMPT, KEY_POINTS_PROMPT, PODCAST_SCRIPT_PROMPT
from backend.graph.state import PodcastState
from openai import OpenAI
import io

# Initialize ChatOpenAI
llm = ChatOpenAI(
    model=config.MODEL_NAME,
    temperature=config.TEMPERATURE,
    openai_api_key=config.OPENAI_API_KEY
)

# Initialize OpenAI client for TTS
openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

def summarize_content(state: PodcastState) -> PodcastState:
    """Summarize the PDF content"""
    print("Step 1: Summarizing content...")
    
    try:
        prompt = SUMMARIZE_PROMPT.format(text=state["pdf_text"][:10000])  # Limit for token management
        response = llm.invoke(prompt)
        state["summary"] = response.content
        state["current_step"] = "summarize_complete"
        print("Summary complete!")
    except Exception as e:
        state["error"] = f"Summarization error: {str(e)}"
    
    return state

def extract_key_points(state: PodcastState) -> PodcastState:
    """Extract key points from the content"""
    print("Step 2: Extracting key points...")
    
    try:
        prompt = KEY_POINTS_PROMPT.format(text=state["summary"])
        response = llm.invoke(prompt)
        
        # Parse key points into a list
        key_points_text = response.content
        key_points = [point.strip() for point in key_points_text.split('\n') if point.strip()]
        
        state["key_points"] = key_points
        state["current_step"] = "key_points_complete"
        print(f"Extracted {len(key_points)} key points!")
    except Exception as e:
        state["error"] = f"Key points extraction error: {str(e)}"
    
    return state

def generate_script(state: PodcastState) -> PodcastState:
    """Generate podcast script"""
    print("Step 3: Generating podcast script...")
    
    try:
        key_points_str = "\n".join(state["key_points"])
        prompt = PODCAST_SCRIPT_PROMPT.format(
            summary=state["summary"],
            key_points=key_points_str
        )
        response = llm.invoke(prompt)
        state["podcast_script"] = response.content
        state["current_step"] = "script_complete"
        print("Script generation complete!")
    except Exception as e:
        state["error"] = f"Script generation error: {str(e)}"
    
    return state

def generate_audio(state: PodcastState) -> PodcastState:
    """Convert script to audio using OpenAI TTS"""
    print("Step 4: Generating audio...")
    
    try:
        script = state["podcast_script"]
        
        # Split script into smaller chunks if needed (TTS has limits)
        max_chars = 4000
        script_chunks = []
        
        if len(script) > max_chars:
            # Split by sentences
            sentences = script.split('. ')
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < max_chars:
                    current_chunk += sentence + '. '
                else:
                    script_chunks.append(current_chunk.strip())
                    current_chunk = sentence + '. '
            
            if current_chunk:
                script_chunks.append(current_chunk.strip())
        else:
            script_chunks = [script]
        
        # Generate audio for each chunk
        audio_segments = []
        for i, chunk in enumerate(script_chunks):
            print(f"Generating audio segment {i+1}/{len(script_chunks)}...")
            response = openai_client.audio.speech.create(
                model=config.TTS_MODEL,
                voice=config.TTS_VOICE,
                input=chunk
            )
            audio_segments.append(response.content)
        
        state["audio_segments"] = audio_segments
        
        # Combine all segments
        if len(audio_segments) == 1:
            state["final_audio"] = audio_segments[0]
        else:
            # Simple concatenation (for MP3)
            combined = b''.join(audio_segments)
            state["final_audio"] = combined
        
        state["current_step"] = "audio_complete"
        print("Audio generation complete!")
    except Exception as e:
        state["error"] = f"Audio generation error: {str(e)}"
    
    return state