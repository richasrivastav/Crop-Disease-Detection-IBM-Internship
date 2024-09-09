import streamlit as st

def app():
    # st.set_page_config(page_title="Home - Sasyam", layout="wide")

    # Custom CSS for styling
    st.markdown("""
        <style>
            .stButton>button {
                background-color: #95BF44;
                color: white;
                border-radius: 25px;
                font-size: 18px;
                padding: 12px;
                width: 100%;
                border: none;
                margin: 10px;
                transition: background-color 0.3s ease, transform 0.2s ease;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #4B5A31; /* Darker green on hover */
                transform: scale(1.05);
            }
            .stButton>button:active {
                background-color: #1e7e34; /* Even darker green on click */
                transform: scale(0.95);
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Welcome to Sasyam")

    # Introduction section
    st.markdown("""
        ### How It Works
        Sasyam helps you detect crop diseases using advanced image processing techniques. 
        Follow the steps below to learn how to use the platform effectively:
        1. **Upload an Image**: Go to the **Disease Detection** page and upload an image of the crop leaf.
        2. **Enhance Image**: Use the **Enhance Image** button to improve image clarity and highlight details.
        3. **Segment Image**: Click the **Segment Image** button to highlight areas of interest and disease on the leaf.
        4. **Get Diagnosis**: The system will analyze the image and provide a diagnosis along with recommendations for treatment.
    """)

    # Start Demo button
    # st.write("Ready to see it in action?")
    # if st.button("Start Demo"):
    #     st.session_state['show_demo'] = True
    #     st.write("Redirecting to Disease Detection page for demo...")
    #     st.session_state['page'] = 'Disease detection'

    # Redirect to appropriate page based on session state
   
