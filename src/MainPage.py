import streamlit as st
from streamlit_option_menu import option_menu
from src.pages.Home import Home
from src.pages.Upload import Upload

class MainPage:
    def __init__(self):
        pass

    def MainPage():
        st.set_page_config(
            page_title='dataquality',
            layout='wide',            
        )
        st.markdown(""" 
        <h2 style="background-color: #112639; border: 1px solid black; color: #e8e7e7; font-family: 'Times New Roman', serif; text-align: center; padding: 10px; border-radius: 5px;">
            Qual-D
        </h2>
        """,unsafe_allow_html=True)

        selected = option_menu(None, ["What's New", "Upload","Contact Us"], 
            icons=['house', 'cloud-upload','chat-left'], 
            menu_icon="cast", default_index=0, orientation="horizontal",
            styles={
            "container": {"padding": "0!important", "background-color": "#d7d9de"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px","color": "black", "--hover-color": "#d1d1d1"},
            "nav-link-selected": {"background-color": "#FF5733","color":"white"},
            }
            
        )

        if selected=='Home':
            Home.Home()
        if selected=='Upload':
            Upload.Upload()
                   


