from langchain_core.prompts import PromptTemplate

SUMMARIZE_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""You are an expert at summarizing content for podcast creation.
    
    Analyze the following text and provide a comprehensive summary that captures:
    - Main themes and topics
    - Key arguments or points
    - Important details and examples
    
    Text:
    {text}
    
    Summary:"""
)

KEY_POINTS_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Extract the 5-7 most important key points from this text that would be interesting 
    for a podcast audience. Make them engaging and conversational.
    
    Text:
    {text}
    
    Key Points (numbered list):"""
)

PODCAST_SCRIPT_PROMPT = PromptTemplate(
    input_variables=["summary", "key_points"],
    template="""You are a professional podcast scriptwriter. Create an engaging, conversational 
    podcast script based on the summary and key points below.
    
    Guidelines:
    - Write in a warm, conversational tone
    - Use storytelling techniques
    - Include smooth transitions between topics
    - Add rhetorical questions to engage listeners
    - Make it sound natural when spoken aloud
    - Length: approximately 3-5 minutes when read
    - Start with a hook and end with a memorable conclusion
    
    Summary:
    {summary}
    
    Key Points:
    {key_points}
    
    Podcast Script:"""
)