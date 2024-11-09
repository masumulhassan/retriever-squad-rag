
import streamlit as st
import logging
import os

from utils.tracing import start_tracing
from json import JSONDecodeError
from utils.haystack import start_document_store, start_haystack_rag, query, start_haystack_rag_data_embedding
from utils.ui import reset_results, set_initial_state

try:
    start_tracing()
    document_store = start_document_store()
    start_haystack_rag_data_embedding(document_store)
    pipeline = start_haystack_rag(document_store)

    set_initial_state()

    # RAG title
    st.write('# The Retriever Squad RAG')

    # Search bar
    question = st.text_input("Question", value=st.session_state.question, max_chars=1000, on_change=reset_results)

    run_pressed = st.button("Run")

    run_query = (
        run_pressed or question != st.session_state.question
    )

    # Get results for query
    if run_query and question:
        reset_results()
        st.session_state.question = question
        with st.spinner("🔎 &nbsp;&nbsp; Running your pipeline"):
            try:
                st.session_state.results = query(pipeline, question)
            except JSONDecodeError as je:
                st.error(
                    "👓 &nbsp;&nbsp; An error occurred reading the results. Is the document store working?"
                )
            except Exception as e:
                logging.exception(e)
                st.error("🐞 &nbsp;&nbsp; An error occurred during the request.")

    if st.session_state.results:
        results = st.session_state.results
        st.write(results["llm"]["replies"][0])


except SystemExit as e:
    os._exit(e.code)
