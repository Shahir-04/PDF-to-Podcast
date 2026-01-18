from langgraph.graph import StateGraph, END
from backend.graph.state import PodcastState
from backend.graph.nodes import (
    summarize_content,
    extract_key_points,
    generate_script,
    generate_audio
)

def create_podcast_workflow():
    """Create the LangGraph workflow for podcast generation"""
    
    # Initialize the graph
    workflow = StateGraph(PodcastState)
    
    # Add nodes
    workflow.add_node("summarize", summarize_content)
    workflow.add_node("extract_points", extract_key_points)
    workflow.add_node("generate_script", generate_script)
    workflow.add_node("generate_audio", generate_audio)
    
    # Define edges (workflow flow)
    workflow.set_entry_point("summarize")
    workflow.add_edge("summarize", "extract_points")
    workflow.add_edge("extract_points", "generate_script")
    workflow.add_edge("generate_script", "generate_audio")
    workflow.add_edge("generate_audio", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

def run_podcast_generation(pdf_text: str) -> PodcastState:
    """
    Run the complete podcast generation workflow
    
    Args:
        pdf_text: Extracted text from PDF
        
    Returns:
        Final state with generated podcast
    """
    # Initialize state
    initial_state: PodcastState = {
        "pdf_text": pdf_text,
        "summary": "",
        "key_points": [],
        "podcast_script": "",
        "audio_segments": [],
        "final_audio": None,
        "error": None,
        "current_step": "initialized"
    }
    
    # Create and run workflow
    app = create_podcast_workflow()
    final_state = app.invoke(initial_state)
    
    return final_state