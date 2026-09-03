import os
import streamlit as st
from google import genai

# --- Configuration & Constants ---
MODEL_NAME = "gemini-3.5-flash-lite"
PAGE_TITLE = "📚 AI Study Assistant"

def build_prompt(topic: str, option: str) -> str:
    """
    Business Logic: Generates the correct prompt based on user selection.
    This is separated from the UI so it can be tested independently.
    """
    if option == "Explanation":
        return f"Explain {topic} in simple language for a beginner."
    elif option == "Study Notes":
        return f"Create short and easy-to-understand study notes about {topic}."
    elif option == "Practice Questions":
        return f"Create 5 practice questions about {topic} with answers."
    elif option == "Key Points":
        return f"Give 8 important key points about {topic}."
    else:
        # Always have a fallback for unexpected inputs
        return f"Tell me about {topic}."

def main():
    # --- Page Configuration ---
    st.set_page_config(page_title=PAGE_TITLE, page_icon="📚", layout="centered")
    st.title(PAGE_TITLE)
    st.write("Learn any topic with the help of AI.")

    # --- Authentication Check ---
    # Pro practice: Check the environment directly rather than guessing via exceptions
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
        st.stop()
        
    client = genai.Client()

    # --- User Interface ---
    topic = st.text_input("Enter a topic you want to learn:", placeholder="Example: Machine Learning")
    
    option = st.selectbox(
        "What do you want to generate?",
        ["Explanation", "Study Notes", "Practice Questions", "Key Points"]
    )

    # --- Action / Event Handling ---
    if st.button("🤖 Generate"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
            return # Exit the button logic early (Guard Clause)

        prompt = build_prompt(topic, option)

        with st.spinner("AI is generating your response..."):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )
                st.subheader("🤖 AI Response")
                st.write(response.text)
                
            except Exception as e:
                # Here, a broad exception is okay to prevent app crashes, 
                # but we print the actual error 'e' so we can debug it.
                st.error("Something went wrong while contacting the AI.")
                st.exception(e) # Streamlit's built-in way to format errors

# Standard Python idiom to run the app
if __name__ == "__main__":
    main()