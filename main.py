import streamlit as st
from streamlit_option_menu import option_menu
import diseased, home, about, contact, blogs

st.set_page_config(page_title="Sasyam", page_icon=":seedling:")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:linear-gradient(#718760,#AECE90);}
[data-testid="stHeader"]{
background-color:rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Display the logo in the sidebar
st.sidebar.image('log.png', width=150)

def run():
    with st.sidebar:
        app = option_menu(
            menu_title='Sasyam',
            options=['Home', 'Disease detection', 'Blogs', 'Contact us', 'About us'],
            icons=['house-fill', 'activity', 'book-fill', 'envelope-fill', 'info-circle-fill'],
            menu_icon='chat-text-fill',
            styles={
                "container": {"padding": "5!important", "background-color": "#718760"},
                "nav-link": {"color": "white", "font-size": "15px", "text-align": "left", "--hover-color": "#4B5A31"},
                "nav-link-selected": {"background-color": "#7B9F3E"}
            })
    
    if app == "Home":
        home.app()
    if app == "Disease detection":
        diseased.app()
    if app == "Blogs":
        blogs.app()
    if app == 'About us':
        about.app()
    if app == "Contact us":
        contact.app()

run()
