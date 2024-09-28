from src.pages.Upload import Upload
import streamlit as st
import pandas as pd
from typing import Any, Dict
from pandas.api.types import is_categorical_dtype, is_numeric_dtype, is_datetime64_any_dtype, is_object_dtype

class Filter:
    @staticmethod
    def dataframe_explorer(df: pd.DataFrame, case: bool = True) -> pd.DataFrame:
        """
        Adds a UI on top of a dataframe to let viewers filter columns.

        Args:
            df (pd.DataFrame): Original dataframe
            case (bool, optional): If True, text inputs will be case sensitive. Defaults to True.

        Returns:
            pd.DataFrame: Filtered dataframe
        """

        random_key_base = pd.util.hash_pandas_object(df)

        df = df.copy()

        # Try to convert datetimes into standard format (datetime, no timezone)
        for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass

            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

        modification_container = st.container()

        with modification_container:
            to_filter_columns = st.multiselect(
                "Filter dataframe on",
                df.columns,
                key=f"{random_key_base}_multiselect",
            )
            filters: Dict[str, Any] = dict()
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                # Treat columns with < 40 unique values as categorical
                if is_categorical_dtype(df[column]) or df[column].nunique() < 40:
                    filters[column] = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                        key=f"{random_key_base}_{column}",
                    )
                    df = df[df[column].isin(filters[column])]
                elif is_numeric_dtype(df[column]):
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 100
                    filters[column] = right.slider(
                        f"Values for {column}",
                        _min,
                        _max,
                        (_min, _max),
                        step=step,
                        key=f"{random_key_base}_{column}",
                    )
                    df = df[df[column].between(*filters[column])]
                elif is_datetime64_any_dtype(df[column]):
                    filters[column] = right.date_input(
                        f"Values for {column}",
                        value=(
                            df[column].min(),
                            df[column].max(),
                        ),
                        key=f"{random_key_base}_{column}",
                    )
                    if len(filters[column]) == 2:
                        filters[column] = tuple(map(pd.to_datetime, filters[column]))
                        start_date, end_date = filters[column]
                        df = df.loc[df[column].between(start_date, end_date)]
                else:
                    filters[column] = right.text_input(
                        f"Pattern in {column}",
                        key=f"{random_key_base}_{column}",
                    )
                    if filters[column]:
                        df = df[df[column].str.contains(filters[column], case=case)]

        return df

    @staticmethod
    def FilterPage():
        col1, col2, col3 = st.columns([0.5, 3, 0.5])

        with col2:
            if 'UploadedDf' in st.session_state:
                df = st.session_state.UploadedDf
                st.subheader('Filters:')
                filtered_df = Filter.dataframe_explorer(df, case=False)  # No 'self' needed
                st.dataframe(filtered_df, use_container_width=True)
            else: 
                st.subheader("You have not Uploaded any File yet")
        with col1:
            pass
        with col3:
            pass
