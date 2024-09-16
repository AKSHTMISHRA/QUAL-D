import pandas as pd
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_gsheets import GSheetsConnection
import os

class ContactMe:
    def __init__(self):
        pass
    def ContactMePage():
        st.header(":mailbox: Get In Touch With Me!")
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
                conn=st.connection("gsheets",type=GSheetsConnection)
                st.write("""<h3> We Welcome All Feedbacks and Suggestions!</h3>""",unsafe_allow_html=True)
                # Streamlit form for user inputs
                with st.form("Contact Us"):
                    name = st.text_input(label="Please Enter your Name", max_chars=15, placeholder="Name")
                    email = st.text_input(label="Please Enter your Email", max_chars=35, placeholder="Email")
                    Feedback = st.text_area(label="Any Suggestions/Feedbacks?", max_chars=250, placeholder="Suggestion/Feedback")

                    # Submit button in Streamlit form
                    submitted = st.form_submit_button("Submit", use_container_width=True)

                    if submitted:
                        if not name or not email or not Feedback:
                            st.error("Please fill all the fields before submitting!")
                        else:
                            UserData=pd.DataFrame({
                                'Name': [name],
                                'Email': [email],
                                'Feedback' : [Feedback],
                            })
                            
                            # Fetch existing data from the Google Sheet
                            sheet_data = conn.query('SELECT * FROM SuggestionsFeedbacks')

                            # Append new data to the existing data
                            updated_data = pd.concat([sheet_data, UserData], ignore_index=True)

                            # Update the sheet with the new data
                            conn.update(worksheet='SuggestionsFeedbacks', data=updated_data)
                            # Success message
                            st.success("Thank you for your feedback! Your message has been sent.")
                                   

                