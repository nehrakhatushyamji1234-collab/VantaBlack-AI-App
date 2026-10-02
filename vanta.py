import streamlit as st
from google import genai
from PIL import Image
import time

# --- 1. पेज सेटअप (Page Configuration) ---
st.set_page_config(page_title="VantaBlack AI", page_icon="⚫", layout="wide")

# --- 2. आपकी चालू Gemini API Key ---
API_KEY = "AQ.Ab8RN6KohME3DpjSPkSYRyHlaYEEHlV20o3clOYMbgRsif4Cgw"

# --- 3. Gemini एआई क्लाइंट सेटअप ---
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)

# --- 4. चैट हिस्ट्री और पॉप-अप स्टेट चालू करना ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. प्रीमियम डार्क थीम (Custom CSS) ---
st.markdown("""
    <style>
        .stApp {
            background-color: #0b0b0f !important;
            color: #ffffff !important;
        }
        .stChatInputContainer textarea {
            background-color: #16161a !important;
            color: white !important;
            border: 1px solid #2a2a35 !important;
            border-radius: 12px !important;
        }
        [data-testid="stSidebar"] {
            background-color: #07070a !important;
            border-right: 1px solid #1a1a24;
        }
        .stButton>button {
            background-color: #16161a !important;
            color: white !important;
            border: 1px solid #2a2a35 !important;
            border-radius: 8px !important;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #24242c !important;
            border-color: #10a37f !important;
            color: #10a37f !important;
        }
        .stChatMessage {
            background-color: transparent !important;
            padding: 10px 0px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 6. लीगल डॉक्यूमेंट्स डेटा (ChatGPT/Gemini स्टाइल) ---
privacy_policy_text = """
### Privacy Policy for VantaBlack AI
*Last updated: September 2026*

Welcome to VantaBlack AI. We value your privacy and are committed to protecting your personal data in a manner consistent with industry leaders like OpenAI and Google.

#### 1. Information We Collect
- **User Content:** We process the text inputs, prompts, and images you upload to VantaBlack AI to generate responses.
- **Technical Data:** We automatically log your IP address, browser type, and basic usage statistics to maintain service stability and speed.

#### 2. How We Use Information
- To provide, maintain, and improve the core capabilities of VantaBlack AI.
- To diagnose technical issues and ensure the security of our application against abuse.

#### 3. Data Sharing & Retention
- Your inputs are processed directly via secure APIs powered by Google Gemini advanced infrastructure.
- We do not sell, rent, or trade your personal data to third parties for marketing purposes.
- Chat history is stored locally in your session state and vanishes upon closing or resetting the app unless explicitly saved.
"""

terms_conditions_text = """
### Terms of Service for VantaBlack AI
*Last updated: September 2026*

By accessing or using VantaBlack AI, you agree to comply with and be bound by these Terms of Service.

#### 1. Usage Requirements
- **Acceptable Use:** You agree not to generate harmful, illegal, abusive, or sexually explicit content, or content that violates intellectual property laws.
- **System Integrity:** You must not attempt to reverse engineer, disrupt, or bypass any security constraints of the VantaBlack AI interface or backend APIs.

#### 2. Content Ownership and AI Disclaimers
- **Your Input:** You retain ownership of all prompts and images you upload to VantaBlack AI.
- **AI Outputs:** Due to the nature of machine learning, outputs may occasionally contain errors or hallucinations. VantaBlack AI does not guarantee the absolute accuracy, completeness, or reliability of generated responses. Verify critical information independently.

#### 3. Limitation of Liability
VantaBlack AI is provided on an "as-is" and "as-available" basis. We shall not be liable for any indirect, incidental, or consequential damages resulting from your use or inability to use the platform.
"""

# --- 7. लेफ्ट साइडबार UI Layout ---
with st.sidebar:
    try:
        st.image("logo.png", width=55)
    except:
        pass
        
    st.markdown("<h2 style='color: white; margin-top: 5px; margin-bottom: 0;'>🖤 VantaBlack AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; margin-top: 0; font-size: 12px;'>VantaBlack 1.0 (Vision Pro)</p>", unsafe_allow_html=True)
    st.write("")
    
    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.write("---")
    st.markdown("<p style='color: #888; font-size: 14px; font-weight: bold; margin-bottom: 5px;'>Recent Chats</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #444; font-size: 13px; font-style: italic;'>No recent chats</p>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("<p style='color: #888; font-size: 14px; font-weight: bold; margin-bottom: 5px;'>Vision Pro Feature</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image to analyze", type=["png", "jpg", "jpeg"])
    
    st.write("---")
    
    # बटन्स पर क्लिक होने पर डायलॉग पॉप-अप दिखाना
    if st.button("🔒 Privacy Policy", use_container_width=True):
        st.dialog("Privacy Policy")(lambda: st.markdown(privacy_policy_text))()
        
    if st.button("📋 Terms & Conditions", use_container_width=True):
        st.dialog("Terms & Conditions")(lambda: st.markdown(terms_conditions_text))()

# --- 8. मुख्य स्क्रीन हेडर (Main Screen UI) ---
st.markdown("<h1 style='text-align: center; color: white; margin-top: 40px;'>VantaBlack 1.0 (Vision Pro)</h1>", unsafe_allow_html=True)
st.write("")

# पुरानी बातचीत को स्क्रीन पर लगातार दिखाते रहना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 9. चैट इनपुट और एआई रिस्पॉन्स लॉजिक (Core Logic) ---
if user_input := st.chat_input("Message VantaBlack AI..."):
    
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = st.session_state.client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=[user_input, img]
                )
            else:
                response = st.session_state.client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=user_input
                )
            
            for chunk in response.text.split(" "):
                full_response += chunk + " "
                time.sleep(0.04)
                message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"कनेक्शन एरर: कृपया इंटरनेट कनेक्शन या अपनी लाइब्रेरी चेक करें।\n\nविवरण: {str(e)}"
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
