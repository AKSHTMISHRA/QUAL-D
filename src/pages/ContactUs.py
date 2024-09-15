import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import os

class ContactMe:
    def __init__(self):
        pass
    def ContactMePage():
        
        with stylable_container(key=None,
            css_styles="""
                                    {
                                        background-color: rgba(220,220,220,0.1);
                                        border-radius: 20px;    
                                        border: 1px solid rgba(49, 51, 63, 0.2);
                                        border-radius: 0.5rem;
                                        color: black;
                                        padding: calc(1em - 1px)
                                    }
                                    """,
            ):
            col1,col2=st.columns([1.5,3.5])
            with col1:
                ImagePath=os.path.join('src','pictures','Man.png')
                st.image(ImagePath,use_column_width=True)
            with col2:
                st.write("""<h3> We Welcome All Feedbacks and Suggestions!</h3>""",unsafe_allow_html=True)
                with st.form("Contact Us"):
                    st.text_input(label="Please Enter your Name",max_chars=15,placeholder="Name")
                    st.text_input(label="Please Enter your Email",max_chars=35,placeholder="Email")
                    st.text_input(label="Any Suggestions/Feedbacks?",max_chars=250,placeholder="Suggestion/Feedback")

                    submitted = st.form_submit_button("Submit",use_container_width=True)
                    if submitted:
                        st.write("slider", slider_val, "checkbox", checkbox_val)