from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph

class PodcastState(TypedDict):
    """State for the podcast generation workflow"""
    pdf_text: str
    summary: str
    key_points: List[str]
    podcast_script: str
    audio_segments: List[bytes]
    final_audio: Optional[bytes]
    error: Optional[str]
    current_step: str