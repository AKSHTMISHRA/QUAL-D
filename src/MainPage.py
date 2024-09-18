import streamlit as st
from streamlit_option_menu import option_menu
from src.pages.Home import Home
from src.pages.Upload import Upload
from src.pages.ContactUs import ContactMe
from src.pages.Filter import Filter

class MainPage:
    def __init__(self):
        pass

    def MainPage():
        st.set_page_config(
            page_title='dataquality',
            layout='wide',            
        )
        col1,col2=st.columns([2.5,1.5   ])
        with col1:
            st.markdown(""" 
            <h1 style="background-color: #112639; border: 1px solid black; color: white; font-family: 'Times New Roman', serif; text-align: center; padding: 9px; border-radius: 8px;">
                Qual-D
            </h1>
            """,unsafe_allow_html=True)

        with col2:
            selected = option_menu(None, ["What's New", "Upload","Filters", "Contact Us"],  
                icons=['house', 'speedometer','table' ,'chat-left'], 
                menu_icon="cast", default_index=0, orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#d7d9de"},
                    "icon": {"color": "white", "font-size": "25px", "display": "block", "text-align": "center"},
                    "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "color": "black", "--hover-color": "rgba(255, 87, 51,0.5)","padding":"6px"},
                    "nav-link-selected": {"background-color": "#FF5733", "color": "white", "display": "block"},
                    "nav-link-icon": {"display": "block", "text-align": "center"}
                }
            )

        if selected=='Home':
            Home.Home()
        if selected=='Upload':
            Upload.Upload()
        if selected=='Contact Us':
            ContactMe.ContactMePage()
        if selected=='Filters':
            Filter.FilterPage()    


