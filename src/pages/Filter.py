import streamlit as st
from src.pages.Upload import Upload

class Filter:
    def __init__(self):
        pass

    def FilterPage():
        col1,col2=st.columns([1,3])

        with col2:
            if 'UploadedDf' in st.session_state:
                df=st.session_state.UploadedDf
                st.subheader('DATA:')
                st.dataframe(df,hide_index=True)
            else: 
                st.subheader("You have not Uploaded any File yet")
        with col1:
            None            

