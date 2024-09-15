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
        rare_categories = frequency[frequency < threshold].index.tolist()
        return rare_categories
    
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
            return pd.DataFrame()  # Return an empty DataFrame or handle as appropriate

        frequency = data[column].value_counts()
        st.write(frequency)
        # mode_value = frequency.idxmax()
        # mode_freq = frequency.max()
        # outliers = frequency[frequency < threshold]
        # outliers_df = pd.DataFrame(outliers, columns=['Frequency'])
        # outliers_df['Deviation from Mode'] = mode_freq - outliers_df['Frequency']
        # return outliers_df
  
        
    
    def Report(self):
        st.subheader("DATA INSIGHTS")
        
        ##########################################################################################################
        ##missing  value
        st.text("1. Missing Values")
        missing =self.data.isnull().sum()
        missing=missing[missing > 0]
        missing=missing.reset_index()
        missing.columns=['Column Names','Total Nulls']
        st.dataframe(missing,use_container_width=True)
        value=missing['Total Nulls'].sum()
        st.markdown(f"""
        <h5>Total Nulls in the Dataset: {value}</h5>
        """,unsafe_allow_html=True)
        ########################################################
        duplicates= self.data.duplicated().sum()
        if duplicates<=0:
            st.markdown("""
            <h5>Total Duplicates in the Dataset: None</h5>
            """,unsafe_allow_html=True)
        else: 
            st.markdown(f"""
            <h5>Total Duplicates in the Dataset: {duplicates}</h5>
            """,unsafe_allow_html=True)

        ##
        ##########################################################################################################
        ## Empty columns
        st.text("2. Null Columns")
        EmptyColumns= [col for col in self.data.columns if self.data[col].isnull().all()]
        if len(EmptyColumns)<=0:
            st.markdown("""
            <h5>Total Null columns in the Dataset: None</h5>
            """,unsafe_allow_html=True)
        else: 
            st.markdown(f"""
            <h5>Total Null columns in the Dataset: {EmptyColumns}</h5>
            """,unsafe_allow_html=True)
        ##
        ##########################################################################################################
        ## 
        st.text("3. Data types")
        DataTypes=self.data.dtypes
        DataTypes=DataTypes.reset_index()
        DataTypes.columns=['Columns','Datatype']
        st.dataframe(DataTypes,use_container_width=True)
        
        CategoricalData=[]
        NumericalData=[]

        # for col in self.data.columns:
        #     if pd.api.types.is_categorical_dtype(self.data[col]):
        #         CategoricalData.append(col)
        #     if pd.api.types.is_numeric_dtype(self.data[col]):
        #         NumericalData.append(col)
        
        NumericalData = self.data.select_dtypes(include=['number'])
        CategoricalData = self.data.select_dtypes(include=['object', 'category', 'bool'])

        st.write("Categorical columns:")
        st.write(CategoricalData)
        st.write("Numerical columns:")
        st.write(NumericalData)
        
        ##
        ##########################################################################################################
        ##
        st.text("4. Unique Column Values")
        
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

        ##
        ##########################################################################################################
        ##
        st.text("5. Outliers")
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
                            outliers=self.FrequencyAnalysis(self.data, CategoricOutliers)
                            col1,col2=st.columns([1,1])
                            with col1:
                                if outliers:
                                    st.markdown(f"**Rare Categories (Frequency Analysis):**")
                                    st.dataframe(outliers,use_container_width=True)
                                else:
                                    st.markdown("**No rare categories found (Frequency Analysis).**")
                            
                            with col2:
                                None

                    elif SelectedNum=="Mode Deviation":
                            outliers = self.ModeDeviation(self.data, CategoricOutliers)
                            # col1, col2 = st.columns([1, 1])
                            # with col1:                                
                            #     if outliers is not None and not outliers.empty:
                            #         st.markdown(f"**Outliers based on Mode Deviation:**")
                            #         st.write(outliers)
                            #     else:
                            #         st.markdown("**No outliers found (Mode Deviation).**")

                            with col2:
                                None                            
                        
                        
            
            
            #######################################
            
            if SelectedColumn=='NUMERICAL COLUMNS':
                #numeric values
                NumericalCol = self.data.select_dtypes(include=['number']).columns.tolist()
                NumericOutliers=st.multiselect(
                    "Select Columns",
                    NumericalCol
                )
                if NumericOutliers:
                    for col in NumericOutliers:
                        SelectedNum=option_menu("Numericcolumns",
                        ["Z-Score", "IQR", "Flooring and capping"],
                        default_index=0, orientation="horizontal"
                        )

                        if SelectedNum=="Z-Score":
                            outliers = self.ZScore(self.data,col)
                        elif SelectedNum== "IQR":
                            outliers = self.IQR(self.data,col)
                        elif SelectedNum== "Flooring and capping":
                            outliers = self.FlooringCapping(self.data,col)       
                        
                        
                        if not outliers.empty:
                                col1,col2=st.columns([1,1])
                                with col1:
                                    st.markdown(f"""<h5>The column '{col}' has the following outliers:</h5>""", unsafe_allow_html=True)
                                    st.write(outliers)
                                with col2:
                                    fig, ax = plt.subplots()
                                    ax.boxplot(self.data[col])
                                    st.markdown(f"""<h5>Boxplot for {col} column</h5>""",unsafe_allow_html=True)

                                    # Display the plot in Streamlit
                                    st.pyplot(fig)    
                        else:
                            st.markdown(f"""<h5>The column '{col}' has no outliers.</h5>""", unsafe_allow_html=True)
                #######################################
        

        ##
        ##########################################################################################################
        ##
        st.markdown("""6. Timeliness
        Data Freshness: Determine how up-to-date the data is.
        Time Gaps: Identify any unexpected gaps in time-series data.""")

        DateTimeCol = self.data.select_dtypes(include=['datetime']).columns.tolist()
        # st.write(DateTimeCol)

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



        ##
        ##########################################################################################################
        ##
        st.text("7. Descriptive Statistics(Only Numeric Columns)")

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

        ##
        ##########################################################################################################


