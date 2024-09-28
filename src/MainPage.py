import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container
from src.pages.Home import Home
from src.pages.Upload import Upload
from src.pages.ContactUs import ContactMe
from src.pages.Filter import Filter

class MainPage:
    def __init__(self):
        pass

    def MainPage():
        st.set_page_config(
            page_title='Qual-D',
            layout='wide',            
        )
        with stylable_container(
        key="header_classic",
        css_styles="""{
        background-color: #112639;
        color: white;
        font-family:roboto;
        padding: 10px;
        border-bottom: 2px solid #007bff;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        position: fixed;
        top : 60px;
        left:0;
        width: 100%;    
        z-index: 10000;
        }""",):
            col1,col2=st.columns([2,3])
            with col1:
                st.write("""<b style="color: white; font-size: 42px">Qual-D</b>""",unsafe_allow_html=True)
            
            with col2:
                selected = option_menu(None, ["What's New", "Upload","Filters", "Contact Us"],  
                icons=['house', 'speedometer','table' ,'chat-left'], 
               menu_icon="cast", default_index=0, orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#112639","border-radius": "0px","box-shadow": "none" ,"margin": "0px","border": "none","overflow": "hidden","padding-top":"50px"},
                    "icon": {"color": "white", "display": "block", "text-align": "center","border": "none","padding": "0px","font-size":"30px"},
                    "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "color": "white", "--hover-color": "rgba(255, 87, 51,0.5)","padding": "0px","border": "none"},
                    "nav-link-selected": {"background-color": "#ff6804", "color": "white", "display": "block"},
                    "nav-link-icon": {"display": "block", "text-align": "center"}
                }
            )

        with stylable_container(
        key="body",
        css_styles="""{
        position : relative;
        top: 60px;
        left: 0;
        width: 100%;
        
        z-index: 100;
        }""",):
            if selected=="What's New":
                Home.Home()
            if selected=='Upload':
                Upload.Upload()
            if selected=='Contact Us':
                ContactMe.ContactMePage()
            if selected=='Filters':
                Filter.FilterPage() 
        

           


