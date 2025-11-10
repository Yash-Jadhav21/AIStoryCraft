import streamlit as st
from story_generator import generate_story_from_images, narrate_story
from PIL import Image

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(page_title="AI Story Generator", page_icon="📖", layout="wide")

# ----------------------- CUSTOM STYLING -----------------------
st.markdown("""
    <style>
    .stButton>button {
        background-color: #6c63ff;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #5145cd;
    }
    .stMarkdown {
        font-size: 1.1rem;
    }
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------- HEADER -----------------------
st.title("📖 AI Story Generator from Images")
st.markdown(
    "Upload 1 to 10 images, choose your favorite story style, and let **Gemini AI** craft and narrate your magical story! ✨"
)

# ----------------------- SIDEBAR -----------------------
with st.sidebar:
    st.header("🧩 Controls")

    uploaded_files = st.file_uploader(
        "Upload your images...",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    story_style = st.selectbox(
        "Choose a story style",
        ("Comedy", "Thriller", "Fairy Tale", "Sci-Fi", "Mystery", "Adventure", "Morale")
    )

    voice_speed = st.radio("Narration Speed", ["Normal", "Slow"], index=0)

    generate_button = st.button("✨ Generate Story & Narration", type="primary")

# ----------------------- MAIN LOGIC -----------------------
if generate_button:
    if not uploaded_files:
        st.warning("⚠️ Please upload at least 1 image.")
    elif len(uploaded_files) > 10:
        st.warning("⚠️ Please upload a maximum of 10 images.")
    else:
        with st.spinner("🪄 Gemini is creating your story... Please wait..."):
            try:
                pil_images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]

                # -------- DISPLAY IMAGES --------
                st.subheader("🖼️ Your Visual Inspiration:")
                cols = st.columns(len(pil_images))
                for i, img in enumerate(pil_images):
                    with cols[i]:
                        st.image(img, width="stretch")

                # -------- GENERATE STORY --------
                generated_story = generate_story_from_images(pil_images, story_style)

                if "Error" in generated_story or "failed" in generated_story or "API key" in generated_story:
                    st.error(generated_story)
                else:
                    st.subheader(f"📚 Your {story_style} Story:")
                    st.success(generated_story)

                    # -------- DOWNLOAD STORY FILE --------
                    st.download_button(
                        label="📩 Download Story as Text",
                        data=generated_story,
                        file_name="ai_story.txt",
                        mime="text/plain"
                    )

                    # -------- NARRATION SECTION --------
                    st.subheader("🎧 Listen to Your Story:")
                    audio_file = narrate_story(
                        generated_story,
                        slow=True if voice_speed == "Slow" else False
                    )
                    if audio_file:
                        st.audio(audio_file, format="audio/mp3")
                        st.download_button(
                            label="⬇️ Download Narration",
                            data=audio_file,
                            file_name="story_audio.mp3",
                            mime="audio/mp3"
                        )
                    else:
                        st.warning("⚠️ Could not generate narration.")

            except Exception as e:
                st.error(f"❌ Application error occurred: {e}")

# ----------------------- FINAL TOUCH / FOOTER -----------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center;'>
        <h4>🪄 Made with ❤️ by <b>Yash</b></h4>
        <p>Powered by <b>Google Gemini</b> & <b>Streamlit</b></p>
        <p style='color:gray;font-size:14px;'>Version 2.0 — Final Polished Edition</p>
    </div>
    """,
    unsafe_allow_html=True
)
