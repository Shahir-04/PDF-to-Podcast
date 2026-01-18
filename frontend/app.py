import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.utils.pdf_parser import PDFParser
from backend.graph.workflow import run_podcast_generation
from backend.config import config
import time

# Page configuration
st.set_page_config(
    page_title="PDF to Podcast Generator",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .step-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎙️ PDF to Podcast Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform your documents into engaging audio podcasts using AI</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Check API key
    if not config.OPENAI_API_KEY:
        st.error("⚠️ OpenAI API key not found!")
        st.info("Please set your OPENAI_API_KEY in the .env file")
        st.stop()
    else:
        st.success("✅ API key configured")
    
    st.divider()
    
    st.subheader("Voice Settings")
    voice_option = st.selectbox(
        "Select voice:",
        ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    )
    
    st.divider()
    
    st.subheader("About")
    st.info("""
    This app uses:
    - **LangChain** for LLM orchestration
    - **LangGraph** for workflow management
    - **OpenAI GPT-4** for content processing
    - **OpenAI TTS** for audio generation
    """)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF document to convert into a podcast"
    )
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Show file info
        file_size = len(uploaded_file.getvalue()) / 1024  # KB
        st.caption(f"File size: {file_size:.2f} KB")

with col2:
    st.subheader("🎯 Generation Status")
    status_container = st.empty()
    
    if not uploaded_file:
        status_container.info("👈 Upload a PDF file to get started")

# Generate button
if uploaded_file:
    if st.button("🚀 Generate Podcast", type="primary", use_container_width=True):
        try:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Extract PDF text
            status_text.text("📖 Extracting text from PDF...")
            progress_bar.progress(10)
            pdf_text = PDFParser.extract_text(uploaded_file)
            
            if not pdf_text or len(pdf_text) < 100:
                st.error("❌ Could not extract enough text from PDF. Please check the file.")
                st.stop()
            
            st.success(f"✅ Extracted {len(pdf_text)} characters")
            progress_bar.progress(20)
            
            # Step 2: Run workflow
            status_text.text("🤖 Processing with AI workflow...")
            
            # Create tabs for real-time updates
            tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "🔑 Key Points", "📜 Script", "🎵 Audio"])
            
            with st.spinner("Running AI workflow..."):
                # Simulate progress updates
                progress_bar.progress(30)
                time.sleep(1)
                
                status_text.text("🧠 Summarizing content...")
                progress_bar.progress(40)
                
                status_text.text("🔍 Extracting key points...")
                progress_bar.progress(60)
                
                status_text.text("✍️ Generating script...")
                progress_bar.progress(70)
                
                # Run the workflow
                final_state = run_podcast_generation(pdf_text)
                
                if final_state.get("error"):
                    st.error(f"❌ Error: {final_state['error']}")
                    st.stop()
                
                progress_bar.progress(85)
                status_text.text("🎙️ Converting to audio...")
                time.sleep(1)
                
                progress_bar.progress(100)
                status_text.text("✅ Podcast generation complete!")
            
            # Display results
            with tab1:
                st.markdown("### 📝 Summary")
                st.write(final_state["summary"])
            
            with tab2:
                st.markdown("### 🔑 Key Points")
                for i, point in enumerate(final_state["key_points"], 1):
                    st.markdown(f"{i}. {point}")
            
            with tab3:
                st.markdown("### 📜 Podcast Script")
                st.text_area("Script", final_state["podcast_script"], height=400)
                
                # Download script
                st.download_button(
                    label="📥 Download Script",
                    data=final_state["podcast_script"],
                    file_name="podcast_script.txt",
                    mime="text/plain"
                )
            
            with tab4:
                st.markdown("### 🎵 Generated Podcast")
                
                if final_state["final_audio"]:
                    st.audio(final_state["final_audio"], format="audio/mp3")
                    
                    # Download audio
                    st.download_button(
                        label="📥 Download Podcast (MP3)",
                        data=final_state["final_audio"],
                        file_name="podcast.mp3",
                        mime="audio/mp3"
                    )
                    
                    st.success("✅ Your podcast is ready! Listen above or download it.")
                else:
                    st.error("❌ Audio generation failed")
            
            # Cleanup
            progress_bar.empty()
            status_text.empty()
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        Built with ❤️ using LangChain, LangGraph, OpenAI & Streamlit
    </div>
""", unsafe_allow_html=True)