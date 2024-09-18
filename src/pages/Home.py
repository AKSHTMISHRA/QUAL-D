import streamlit as st
from streamlit_extras.stylable_container import stylable_container

class Home:
    def __init__(self):
        pass

    def Home():
        # st.header("HOMEPAGE")
        style="""
                <style>
                .text-container {
                    position: relative;
                    display: inline-block;
                    white-space: nowrap;   
                }

                .back-text {
                    font-size: 40px;
                    color: lightgray;
                    position: absolute;
                    top: 0;
                    left: 0;
                    z-index: 1;
                    white-space: nowrap;   
                }

                .front-text {
                    font-size: 30px;
                    color: black;
                    position: absolute;
                    top: 0;
                    left: 0;
                    z-index: 2;
                    white-space: nowrap;   
                }
                </style>
            """
        col1,col2=st.columns([1,1])
        with col1:
            with stylable_container(key="Versioning",
            css_styles="""
                {
            background-color: light grey;
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px)
                }
            """,):
                st.subheader("WHAT I AM? :wink:")
                st.markdown("""<h5>Hi!</h5><h6> I'm here to provide you with an interactive data analysis experience. You can easily upload datasets in various formats and instantly generate detailed reports. I’ll help you ensure data quality by checking for missing values, detecting duplicates, and identifying outliers using advanced techniques like Z-score, IQR, and Mode Deviation.
                    <br><br>Additionally, I'll guide you through understanding your dataset’s structure by highlighting unique values, data types,view summary statistics and even running timeliness checks for time-series data!.</h6>""",unsafe_allow_html=True)
        with col2:
            # Inject custom CSS for overlapping text
            st.markdown(style, unsafe_allow_html=True)

            st.markdown("""
            <div class="text-container">
                <span class="back-text">WHAT's NEW?</span>
                <span class="front-text">WHAT's NEW?</span>
            </div>
            """,unsafe_allow_html=True)
            st.divider()
            
            with stylable_container(key="Versioning",
            css_styles="""
                {background-color: light grey;
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px)
                }
            """,):        
                st.markdown("""
                <h4 style="color: rgba(255, 87, 51,0.9);">Version 1.0.0</h4>
                """,unsafe_allow_html=True)
                st.markdown("""
                ##### **File Upload**  
                - Supports: `.csv`, `.xlsx`, `.xls`, `.json`, `.txt`  
                - Automatic handling & data preview  

                ##### **Data Quality Checks**  
                - **Missing Values & Duplicates**: Count & summary  
                - **Null Columns**: Detect empty columns  
                - **Data Types**: Grouped as numerical & categorical  
                - **Unique Values**: View by column  

                ##### **Outlier Detection**  
                - **Categorical**: Mode Deviation / Frequency Analysis  
                - **Numerical**: Z-Score, IQR, Flooring & Capping (with Boxplot)  

                ##### **Timeliness Check**  
                - Detects time-series gaps & checks date consistency  

                ##### **Descriptive Stats**  
                - Mean, Median, Mode, Standard Deviation  
                """)