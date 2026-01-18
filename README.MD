# 🎙️ PDF to Podcast Generator

Transform your PDF documents and books into engaging audio podcasts using AI!

## 🌟 Features

- **PDF Text Extraction**: Automatically extract text from PDF files
- **AI-Powered Summarization**: Generate concise summaries using GPT-4
- **Key Points Extraction**: Identify the most important points from your content
- **Script Generation**: Create engaging, conversational podcast scripts
- **Text-to-Speech**: Convert scripts to natural-sounding audio using OpenAI TTS
- **Interactive UI**: Beautiful Streamlit interface with real-time progress tracking

## 🛠️ Tech Stack

- **Backend**: LangChain, LangGraph
- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4 Turbo
- **TTS**: OpenAI Text-to-Speech
- **Language**: Python 3.10+

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Shahir-04/PDF-to-Podcast.git
cd pdf-to-podcast
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
```

## 🎯 Usage

1. **Start the Streamlit app**
```bash
streamlit run frontend/app.py
```

2. **Open your browser** to `http://localhost:8501`

3. **Upload a PDF** and click "Generate Podcast"

4. **Wait for processing** - the AI workflow will:
   - Extract text from your PDF
   - Summarize the content
   - Extract key points
   - Generate a podcast script
   - Convert to audio

5. **Listen and download** your podcast!

## 📁 Project Structure

```
pdf-to-podcast/
├── backend/
│   ├── graph/
│   │   ├── nodes.py          # LangGraph workflow nodes
│   │   ├── workflow.py       # Workflow orchestration
│   │   └── state.py          # State management
│   ├── utils/
│   │   ├── pdf_parser.py     # PDF text extraction
│   │   └── prompts.py        # LLM prompt templates
│   └── config.py             # Configuration
├── frontend/
│   └── app.py                # Streamlit UI
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Configuration

You can customize the following in `backend/config.py`:

- `MODEL_NAME`: GPT model to use (default: gpt-4-turbo-preview)
- `TTS_MODEL`: Text-to-speech model (default: tts-1)
- `TTS_VOICE`: Voice selection (alloy, echo, fable, onyx, nova, shimmer)
- `TEMPERATURE`: LLM creativity (0.0-1.0)
- `CHUNK_SIZE`: Text processing chunk size

## 🎨 Voice Options

Choose from 6 different voices:
- **alloy**: Neutral and balanced
- **echo**: Clear and articulate
- **fable**: Warm and engaging
- **onyx**: Deep and authoritative
- **nova**: Energetic and friendly
- **shimmer**: Soft and gentle

## 📊 Workflow

The application uses LangGraph to orchestrate a multi-step workflow:

1. **Summarize** → Extract core content
2. **Extract Key Points** → Identify main topics
3. **Generate Script** → Create conversational narrative
4. **Generate Audio** → Convert to speech

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use this project for your own purposes.

## ⚠️ Notes

- Processing time depends on PDF length and API response times
- Large PDFs may take several minutes to process
- Audio files are in MP3 format
- Ensure you have sufficient OpenAI API credits

## 🐛 Troubleshooting

**Issue**: "OpenAI API key not found"
- Solution: Check that your `.env` file exists and contains `OPENAI_API_KEY`

**Issue**: "Could not extract text from PDF"
- Solution: Ensure PDF contains selectable text (not scanned images)

**Issue**: API rate limits
- Solution: Add delays or upgrade your OpenAI plan

## 📧 Support

For issues and questions, please open an issue on GitHub.

---


Built with ❤️ using LangChain, LangGraph, OpenAI & Streamlit
