import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file.
load_dotenv()

# --- Central Client ---
# This client object automatically finds and uses the GOOGLE_API_KEY.
client = genai.Client()

prompt = "do you remember what i asked you earlier?"

response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=prompt,
    config= {
        "thinking_config":-1,
        #"system_instruction": ""
        "temperature":0.7
    }
)





def restore_and_summarize_text(messy_text: str) -> str:
    """
    Takes messy OCR text, restores it, and then summarizes the result.
    
    Args:
        messy_text: A string containing the jumbled text from an OCR process.
        
    Returns:
        A string containing the cleaned and summarized text.
    """
    # Use the Pro model for its superior reasoning, which is needed for this complex task.
    model_name = "gemini-2.5-pro"
    
  

    # 2. User Prompt: The specific, immediate task for the AI to perform.
    prompt = f"""
    Please perform the following two actions in order:
    1.  **Restore:** The following text is messy and contains errors from OCR. Correct all spelling, grammar, and formatting mistakes to create a clean, readable version.
    2.  **Summarize:** After restoring the text, provide a high-quality summary of the content. Focus on the main ideas and key concepts, presenting them in structured bullet points.

    **Messy Text to Process:**
    ---
    {messy_text}
    ---
    """
    
    

    try:
        
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config={
                "system_instruction":"You are an expert academic assistant. Your primary function is to correct and refine messy text extracted by an OCR process and then provide a clear, concise summary for a college student.",
                "temperature":0.4,
                "max_output_tokens":3500
           }
        )
        
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        
    



