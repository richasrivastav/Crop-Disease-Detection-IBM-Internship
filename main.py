import streamlit as st
from streamlit_option_menu import option_menu
import home, diseased, about, contact, blogs

# Initialize session state variables
if 'username' not in st.session_state:
    st.session_state.username = None  
if 'user_type' not in st.session_state:
    st.session_state.user_type = None  
if 'page' not in st.session_state:
    st.session_state.page = None
if 'selected_crop' not in st.session_state:
    st.session_state.selected_crop = None
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True

st.set_page_config(page_title="Sasyam", page_icon=":seedling:")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(#E8F6F3,#a9DFBF);
    color: Black; 
    font-size: 25px; 
}

[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0); 
    font-size: 18px; 
}

[data-testid="stSidebar"] {
    background-color: #17A589; 
    color: white; 
    font-size: 18px; 
}

[data-testid="stSidebar"] img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 10px; 
}

.sidebar .nav-link {
    color: white ;
    font-size: 18px;
    text-align: left ;
}

.sidebar .nav-link-selected {
    background-color: #66BB6A ;
}

.sidebar .nav-link:hover {
    background-color: #43A047;
}

button {
    background-color: #229954 ;
    color: #FFFFFF ;
    font-size: 18px ;
}

button:hover {
    background-color: #145A32 ;
}

footer {
    background-color: #2E7D32 ;
    color: #E8F5E9 !important; ;
    font-size: 18px; ;
}

#watson-chat {
    position: relative;
    right: 100px;
    bottom: 200px;
    width: 300px;
    z-index: 1000;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.sidebar.image('img/log.png', width=150)

st.sidebar.write("Welcome to Sasyam!", unsafe_allow_html=True)

def show_sidebar():
    if st.session_state.sidebar_visible:
        with st.sidebar:
            if 'username' in st.session_state and st.session_state.username:
                menu_title = f"{st.session_state.username}"
            else:
                menu_title = 'Sasyam'
            app = option_menu(
                menu_title=menu_title,
                options=['Home', 'Crop disease detection', 'Blogs', 'Contact us', 'About us'],
                icons=['house-fill', 'activity', 'book-fill', 'envelope-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                styles={
                    "container": {"padding": "5!important", "background-color": "#117864"},  
                    "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "--hover-color": "#145A32"},
                    "nav-link-selected": {"background-color": "#229954"}  
                })
            return app
    return None

def run():
    if 'sidebar_visible' in st.session_state and st.session_state.sidebar_visible:
        app = show_sidebar()
        if app == "Home":
            home.app()
        elif app == "Crop disease detection":
            diseased.app()
        elif app == "Blogs":
            blogs.app()
        elif app == 'About us':
            about.app()
        elif app == "Contact us":
            contact.app()
        # elif app == "Community Chat":
        #     community.app()
    else:
        home.app()

run()

st.components.v1.html("""
    <div id="watson-chat">
    <script>
      window.watsonAssistantChatOptions = {
        integrationID: "24febfc9-96d9-4da4-b53e-994b51cf73cf", // The ID of this integration.
        region: "au-syd", // The region your integration is hosted in.
        serviceInstanceID: "cc911430-552d-4ec6-a045-1960496264db", // The ID of your service instance.
        onLoad: async (instance) => { await instance.render(); }
      };
      setTimeout(function(){
        const t=document.createElement('script');
        t.src="https://web-chat.global.assistant.watson.appdomain.cloud/versions/" + (window.watsonAssistantChatOptions.clientVersion || 'latest') + "/WatsonAssistantChatEntry.js";
        document.head.appendChild(t);
      });
    </script>
    </div>
""", height=600)
