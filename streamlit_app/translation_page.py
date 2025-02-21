import streamlit as st
from util import display_filtered_dataframe

       
if  ('translation_df' in st.session_state) and (st.session_state.translation_df is not None):
    display_filtered_dataframe(st.session_state.translation_df, "Translations", ['Translation_Language', 'Source_Language'])
    st.markdown("---")
    if st.button("Download Phrases"):
            # TODO: Implement download functionality
            st.text_input("Enter your email:", key="download_email")
else:
    st.write("No translations yet, go chat with your AI Assistant!")
