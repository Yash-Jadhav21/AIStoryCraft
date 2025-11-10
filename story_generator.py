from gtts import gTTS
from dotenv import load_dotenv
import os
from io import BytesIO
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found in .env file")

genai.configure(api_key=api_key)

# ----------------------- PROMPT CREATION -----------------------
def create_advanced_prompt(style):
    base_prompt = f"""
    **Your Persona:** You are a creative Indian storyteller.
    **Your Main Goal:** Write a single story based on the uploaded images.
    **Style Requirement:** The story must fit the '{style}' genre.
    **Core Instructions:**
    1. Use all provided images in the story sequence.
    2. Write in modern, clear English with Indian names and places.
    3. Create a complete story — beginning, middle, and end.
    4. Add creativity, emotion, and smooth flow.
    5. Keep it around 4-5 paragraphs.
    """

    # Add style-specific endings
    style_instruction = ""
    if style == "Morale":
        style_instruction = "\n**After the story**, add a [MORAL]: line with a single moral sentence."
    elif style == "Mystery":
        style_instruction = "\n**After the story**, add a [SOLUTION]: line revealing the culprit or secret."
    elif style == "Thriller":
        style_instruction = "\n**After the story**, add a [TWIST]: line revealing the shocking ending."

    return base_prompt + style_instruction

# ----------------------- STORY GENERATION -----------------------
def generate_story_from_images(images, style):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = model.generate_content(
            [create_advanced_prompt(style), *images]
        )
        return response.text
    except Exception as e:
        return f"Error generating story: {e}"

# ----------------------- AUDIO NARRATION -----------------------
def narrate_story(story_text, slow=False):
    try:
        tts = gTTS(text=story_text, lang="en", slow=slow)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        return None
