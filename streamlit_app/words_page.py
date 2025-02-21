import streamlit as st
from util import display_filtered_dataframe

if ('word_df' in st.session_state) and (st.session_state.word_df is not None):
    # Display both dataframes
    display_filtered_dataframe(st.session_state.word_df, "Words", ['Translation_Language', 'Source_Language'])
else:
    st.write("No words yet, go chat with your AI Assistant!")