import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters

# Function to create and display filtered dataframe
def display_filtered_dataframe(df: pd.DataFrame, title: str, filters: list[str]):
    # Initialize DynamicFilters
    dynamic_filters = DynamicFilters(df, filters=filters)

    # Display filters in the sidebar
    # with st.sidebar:
    st.subheader(f"Filters for {title}")
    dynamic_filters.display_filters(location='columns', num_columns=2, gap='large')

    # Apply dynamic filters to the DataFrame
    # filtered_df = dynamic_filters.filter_df()

    # # Free-text search input
    # search_term = st.text_input(f"Search {title}:")

    # # Apply free-text search filter
    # if search_term:
    #     mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
    #     filtered_df = filtered_df[mask]

    # Display the filtered DataFrame
    st.subheader(title)
    # st.dataframe(filtered_df)
    dynamic_filters.display_df()