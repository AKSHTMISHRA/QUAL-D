import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from streamlit_extras.stylable_container import stylable_container
from streamlit_option_menu import option_menu
from scipy import stats

##########################################################################################################

class Upload:
    def __init__(self):
        pass

    def Upload():
        with stylable_container(key='Upload file',
        css_styles="""
        background-color: light grey;
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 0.5rem;
        padding: calc(1em - 1px)
        """,
        ):
            st.subheader("Please Upload your dataset")
            st.markdown("""
            <b style="color: red;">( .csv , .xlsx, .xls, .json, .txt  file types allowed only)</b>
            """,unsafe_allow_html=True)
            df=st.file_uploader("",type=['csv', 'xlsx', 'xls', 'json','txt'], accept_multiple_files=False,label_visibility= "hidden")
            
            if df is not None:
                
                file_extension = df.name.split('.')[-1].lower()
                st.write(f"You have selected a {file_extension} file.")

                 # Read the uploaded file into a DataFrame
                if file_extension == 'csv':
                    df = pd.read_csv(df)
                elif file_extension in ['xls', 'xlsx']:
                    df = pd.read_excel(df)
                elif file_extension == 'json':
                    df = pd.read_json(df)
                elif file_extension == 'txt':
                    df = pd.read_csv(df, delimiter='\t')

                with st.container(border=True):
                    st.subheader("Your data")
                    with st.expander("Dataset",expanded=False):
                        st.dataframe(data=df,use_container_width=True)
                    st.divider()
                    # Call the Check class and generate the report
                    check_instance = Check(data=df)
                    check_instance.Report()


            else:
                st.write("No file selected.")
                return None

##########################################################################################################

class Check:
    def __init__(self,data):
        self.data=data
    
    def correlation_matrix(self):
        plt.figure(figsize=(10, 8))
        sb.heatmap(self.data.corr(), annot=True, cmap='YlGnBu', center=0)
        st.pyplot(plt)

    def check_date_range(self, date_column):
        min_date = self.data[date_column].min()
        max_date = self.data[date_column].max()
        return min_date, max_date

    def last_updated(self, date_column):
        return self.data[date_column].max()

    def days_since_last_update(self, date_column):
        last_date = self.data[date_column].max()
        today = pd.Timestamp.now()
        return (today - last_date).days

    def ZScore(self,data,column):
        z_scores = stats.zscore(data[column])
        outliers = data[(z_scores > 3) | (z_scores < -3)]
        return outliers

    def IQR(self,data,column):
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        outliers = data[(data[column] < (Q1 - 1.5 * IQR)) | (data[column] > (Q3 + 1.5 * IQR))]
        return outliers

    def FlooringCapping(self,data,column):
        lower_bound = data[column].quantile(0.01)
        upper_bound = data[column].quantile(0.99)
        outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
        return outliers
    
    def FrequencyAnalysis(self,data,column,threshold=0.05):
        frequency = self.data[column].value_counts(normalize=True)
        rare_categories = frequency[frequency < threshold]
        rare_categories_df = pd.DataFrame({
            'Category': rare_categories.index,
            'Frequency': self.data[column].value_counts().loc[rare_categories.index],
            'Percentage': rare_categories.values * 100
        }).reset_index(drop=True)

        return rare_categories_df
    
    def gap_analysis(self, date_column, threshold='1D'):
        self.data = self.data.sort_values(by=date_column)
        self.data['Previous_Date'] = self.data[date_column].shift(1)
        self.data['Gap'] = self.data[date_column] - self.data['Previous_Date']
        gaps = self.data[self.data['Gap'] > pd.Timedelta(threshold)]
        return gaps[['Previous_Date', date_column, 'Gap']]

    def frequency_consistency(self, date_column, expected_frequency='D'):
        self.data = self.data.sort_values(by=date_column)
        self.data.set_index(date_column, inplace=True)
        freq = pd.infer_freq(self.data.index)
        return freq == expected_frequency
    
    def ModeDeviation(self,data,column,threshold=0.05):
        if column not in data.columns:
            st.write(f"Column '{column}' not found in DataFrame.")

        col1,col2=st.columns([1,1])
        # Get frequency of each category
        frequency = data[column].value_counts()
        
        # Get the mode and its frequency
        mode_value = frequency.idxmax()
       
        mode_freq = frequency.max()
        

        # Define the threshold as a percentage of the mode frequency
        threshold_value = mode_freq * threshold
        

        # Filter out the categories with frequencies below the threshold
        outliers = frequency[frequency < threshold_value]  # Updated condition

        with col1:
                 st.write(f"<h4>Mode:</h4> <h5 style='color: green'>{mode_value}</h5>",unsafe_allow_html=True)
                 st.write(f"<h4>Mode Frequency:</h4> <h5 style='color: blue'>{mode_freq}</h5>",unsafe_allow_html=True)
                 st.write(f"<h4>Threshold Value:</h4> <h5 style='color: #FF5733'>{threshold_value}</h5>",unsafe_allow_html=True)
        with col2:
            st.write("Outliers:")
            st.dataframe(outliers,use_container_width=True)

        
  
        
    
    def Report(self):
        st.subheader("DATA INSIGHTS")
        
        ##########################################################################################################
        ##missing  value
        st.subheader("1. Missing Values and Duplicates")
        missing =self.data.isnull().sum()
        missing=missing[missing > 0]
        missing=missing.reset_index()
        missing.columns=['Column Names','Total Nulls']
        st.dataframe(missing,use_container_width=True,hide_index=True)
        value=missing['Total Nulls'].sum()
        st.markdown(f"""
        <h5>Total Nulls in the Dataset: <b style='color:Red'>{value}</b></h5>
        """,unsafe_allow_html=True)
        
        ########################################################
        duplicates= self.data.duplicated().sum()
        duplicatesDF=self.data[self.data.duplicated()]
        if duplicates<=0:
            st.markdown("""
            <h5>Total Duplicates in the Dataset: <b style='color:Red'>None</b></h5>
            """,unsafe_allow_html=True)
        else: 
            st.markdown(f"""
            <h5>Total Duplicates in the Dataset: <b style='color:Red'>{duplicates}</b></h5>
            """,unsafe_allow_html=True)
            st.dataframe(duplicatesDF,hide_index=True)

        st.divider()
        ##
        ##########################################################################################################
        ## Empty columns
        st.subheader("2. Null Columns")
        EmptyColumns= [col for col in self.data.columns if self.data[col].isnull().all()]
        if len(EmptyColumns)<=0:
            st.markdown("""
            <h5>Total Null columns in the Dataset: <b style='color: Red'>None</b></h5>
            """,unsafe_allow_html=True)
        else: 
            st.markdown(f"""
            <h5>Total Null columns in the Dataset: <b style='color:Red'>{EmptyColumns}</b></h5>
            """,unsafe_allow_html=True)
        st.divider()
        ##
        ##########################################################################################################
        ## 
        st.subheader("3. Data types")
        DataTypes=self.data.dtypes
        DataTypes=DataTypes.reset_index()
        DataTypes.columns=['Columns','Datatype']
        st.dataframe(DataTypes,use_container_width=True,hide_index=True)
        
        CategoricalData=[]
        NumericalData=[]

        NumericalData = self.data.select_dtypes(include=['number'])
        CategoricalData = self.data.select_dtypes(include=['object', 'category', 'bool'])
        DateTimeData=self.data.select_dtypes(include=['datetime'])
        

        st.write("""<h5>Categorical columns:</h5>""",unsafe_allow_html=True)
        if len(CategoricalData.columns)==0:
            st.write("""<h6 style="color:red;">No Categorical Columns</h6>""",unsafe_allow_html=True)
        else:    
            st.dataframe(CategoricalData,use_container_width=True,hide_index=True)

        st.write("""<h5>Numerical columns:</h5>""",unsafe_allow_html=True)
        if len(NumericalData.columns)==0:
            st.write("""<h6 style="color:red;">No Numerical Columns</h6>""",unsafe_allow_html=True)
        else: 
            st.dataframe(NumericalData,use_container_width=True,hide_index=True)

        st.write("""<h5>Datetime columns:</h5>""",unsafe_allow_html=True)
        if len(DateTimeData.columns)==0:
            st.write("""<h6 style="color:red;">No DateTime Columns</h6>""",unsafe_allow_html=True)
        else: 
            st.dataframe(DateTimeData,use_container_width=True,hide_index=True)
        st.divider()
        ##
        ##########################################################################################################
        ##
        st.subheader("4. Unique Column Values")
        
        # Create a multiselect widget for selecting columns
        options = st.multiselect(
            "Select Columns",
            self.data.columns
        )

        # Display unique values for the selected columns
        if options:
            for col in options:
                unique_values = self.data[col].unique()
                st.write(f"Unique values in column '{col}':")
                st.write(unique_values)
        else:
            st.write("No columns selected.")

        st.divider()
        ##
        ##########################################################################################################
        ##
        st.subheader("5. Outliers")
        SelectedColumn=option_menu(None,
                ["CATEGORICAL COLUMNS","NUMERICAL COLUMNS"],
                default_index=0, orientation="horizontal"
                )

        if SelectedColumn=="CATEGORICAL COLUMNS" or SelectedColumn=="NUMERICAL COLUMNS":
            
            if SelectedColumn=='CATEGORICAL COLUMNS':
                #numeric values
                CategoricalCol = self.data.select_dtypes(include=['object', 'category', 'bool'],exclude=['datetime']).columns.tolist()
                # st.write(CategoricalCol)
                CategoricOutliers=st.selectbox(
                    "Select Columns",
                    CategoricalCol
                )
                if CategoricOutliers:
                    SelectedNum=option_menu(None,["Frequency Analysis","Mode Deviation"],default_index=0, orientation="horizontal")
                    if SelectedNum=="Frequency Analysis":
                            Outliers = self.FrequencyAnalysis(self.data, CategoricOutliers)

                            col1, col2 = st.columns([1, 1])

                            with col2:
                                if not Outliers.empty:
                                    st.markdown(f"**Rare Categories (Frequency Analysis):**")
                                    # Display the DataFrame with rare categories and their metrics
                                    st.dataframe(Outliers, hide_index=True,use_container_width=True)
                                else:
                                    st.markdown("**No rare categories found (Frequency Analysis).**")
                            
                            # Additional metrics (Optional)
                            with col1:
                                total_categories = len(self.data[CategoricOutliers].unique())
                                rare_count = len(Outliers)
                                rare_percentage = (rare_count / total_categories) * 100

                                st.markdown(f"<h4>Total Categories:</h4> <h5 style='color: green'>{total_categories}</h5>",unsafe_allow_html=True)
                                st.markdown(f"<h4>Rare Categories Count:</h4> <h5 style='color: blue'>{rare_count}</h5>",unsafe_allow_html=True)
                                st.markdown(f"<h4>Percentage of Rare Categories:</h4> <h5 style='color: #FF5733'>{rare_percentage:.2f}%</h5>",unsafe_allow_html=True)

                    elif SelectedNum=="Mode Deviation":
                            self.ModeDeviation(self.data, CategoricOutliers)
                            
                        
            
            
            #######################################
            
            if SelectedColumn=='NUMERICAL COLUMNS':
                #numeric values
                NumericalCol = self.data.select_dtypes(include=['number']).columns.tolist()
                NumericOutliers=st.selectbox(
                    "Select Columns",
                    NumericalCol
                )
                if NumericOutliers:
                    SelectedNum=option_menu(None,
                        ["Z-Score", "IQR", "Flooring and capping"],
                        default_index=0, orientation="horizontal"
                    )

                    if SelectedNum=="Z-Score":
                        outliers = self.ZScore(self.data,NumericOutliers)
                    elif SelectedNum== "IQR":
                        outliers = self.IQR(self.data,NumericOutliers)
                    elif SelectedNum== "Flooring and capping":
                        outliers = self.FlooringCapping(self.data,NumericOutliers)       
                        
                        
                    if not outliers.empty:
                        col1,col2=st.columns([1,1])
                        with col1:
                            st.markdown(f"""<h5>The column '{NumericOutliers}' has the following outliers:</h5>""", unsafe_allow_html=True)
                            st.write(outliers)
                        with col2:
                            fig, ax = plt.subplots()
                            ax.boxplot(self.data[NumericOutliers])
                            st.markdown(f"""<h5>Boxplot for {NumericOutliers} column</h5>""",unsafe_allow_html=True)

                            # Display the plot in Streamlit
                            st.pyplot(fig)    
                    else:
                        st.markdown(f"""<h5>The column '{NumericOutliers}' has no outliers.</h5>""", unsafe_allow_html=True)

                #######################################
        
        st.divider()
        ##
        ##########################################################################################################
        ##
        st.subheader("6. Timeliness")
        st.markdown("""
        <b>Data Freshness:</b> Determine how up-to-date the data is.<br>
        <b>Time Gaps:</b> Identify any unexpected gaps in time-series data.""",unsafe_allow_html=True)

        DateTimeCol = self.data.select_dtypes(include=['datetime']).columns.tolist()
        # st.write(DateTimeCol)

        if len(DateTimeCol)==0:
            st.write("<h5 style='color: Red '>No Column of Datetime is present </h5>",unsafe_allow_html=True)
        else:
            for col in DateTimeCol:
                st.subheader(f" Column {col}:")
                min_date, max_date = self.check_date_range(col)
                st.write(f"Date range: {min_date} to {max_date}")
                
                last_updated = self.last_updated(col)
                st.write(f"Last updated date: {last_updated}")
                
                days_since_update = self.days_since_last_update(col)
                st.write(f"Days since last update: {days_since_update} days")

                # Time Gaps
                gaps = self.gap_analysis(col)
                if not gaps.empty:
                    st.write("Time gaps identified:")
                    st.dataframe(gaps)
                else:
                    st.write("No significant time gaps found.")

                # Frequency Consistency
                is_consistent = self.frequency_consistency(col)
                st.caption(f"Frequency consistency: {'Consistent' if is_consistent else 'Inconsistent'}")

        st.divider()
        ##
        ##########################################################################################################
        ##
        st.subheader("7. Descriptive Statistics(Only Numeric Columns)")

        # Select columns to display descriptive statistics
        selected_columns = st.multiselect("Select Columns", self.data.select_dtypes(include=['number']).columns.tolist())

        if selected_columns:
            # Calculate Mean
            mean_values = self.data[selected_columns].mean()

            # Calculate Median
            median_values = self.data[selected_columns].median()

            # Calculate Mode (mode() returns a DataFrame)
            mode_values = self.data[selected_columns].mode().iloc[0]

            # Calculate Standard Deviation
            std_values = self.data[selected_columns].std()

            # Calculate Variance
            variance_values = self.data[selected_columns].var()

            # Create a summary DataFrame
            summary_df = pd.DataFrame({
                'Mean': mean_values,
                'Median': median_values,
                'Mode': mode_values,
                'Standard Deviation': std_values,
                'Variance': variance_values
            })

            st.dataframe(summary_df)
        else:
            st.write("Please select columns to display descriptive statistics.")

        st.divider()
        ##
        ##########################################################################################################


