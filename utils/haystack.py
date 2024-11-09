import streamlit as st
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.joiners import DocumentJoiner
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.writers import DocumentWriter
from haystack_integrations.components.embedders.ollama import OllamaDocumentEmbedder, OllamaTextEmbedder
from pathlib import Path
from haystack.components.converters import PDFMinerToDocument
from haystack_integrations.components.generators.ollama import OllamaGenerator

from utils.config import document_store_configs, model_configs, dataset_configs
from milvus_haystack import MilvusDocumentStore, MilvusEmbeddingRetriever

from utils.promptTemplate import prompt_template, test_prompt


@st.cache_resource(show_spinner=False)
def start_document_store():
    document_store = MilvusDocumentStore(
        connection_args={
            "uri": document_store_configs['MILVUS_URI']
        },
        drop_old=True
    )

    return document_store


@st.cache_resource(show_spinner=False)
def start_haystack_rag_data_embedding(_document_store: MilvusDocumentStore):
    pdf_converter = PDFMinerToDocument()
    document_joiner = DocumentJoiner()
    document_cleaner = DocumentCleaner()
    document_splitter = DocumentSplitter(split_by="sentence", split_length=5)
    document_embedder = OllamaDocumentEmbedder(
        model=model_configs['EMBEDDING_MODEL'],
        url=model_configs['LLM_URI']
    )
    document_writer = DocumentWriter(_document_store)

    preprocessing_pipeline = Pipeline()
    preprocessing_pipeline.add_component(instance=pdf_converter, name="pypdf_converter")
    preprocessing_pipeline.add_component(instance=document_joiner, name="document_joiner")
    preprocessing_pipeline.add_component(instance=document_cleaner, name="document_cleaner")
    preprocessing_pipeline.add_component(instance=document_splitter, name="document_splitter")
    preprocessing_pipeline.add_component(instance=document_embedder, name="document_embedder")
    preprocessing_pipeline.add_component(instance=document_writer, name="document_writer")
    preprocessing_pipeline.connect("pypdf_converter", "document_joiner")
    preprocessing_pipeline.connect("document_joiner", "document_cleaner")
    preprocessing_pipeline.connect("document_cleaner", "document_splitter")
    preprocessing_pipeline.connect("document_splitter", "document_embedder")
    preprocessing_pipeline.connect("document_embedder", "document_writer")

    preprocessing_pipeline.run({"sources": list(Path(dataset_configs['DATA_PATH']).glob("**/*"))})


@st.cache_resource(show_spinner=False)
def start_haystack_rag(_document_store: MilvusDocumentStore):
    text_embedder = OllamaTextEmbedder(
        model=model_configs['EMBEDDING_MODEL'],
        url=model_configs['LLM_URI'],
    )

    retriever = MilvusEmbeddingRetriever(
        document_store=_document_store,
        top_k=5
    )

    prompt_builder = PromptBuilder(template=prompt_template)

    generator = OllamaGenerator(
        model=model_configs['GENERATIVE_MODEL'],
        url=model_configs['LLM_URI'],
        generation_kwargs={
            "num_predict": -1,
            "temperature": 0.6,
        }
    )

    basic_rag_pipeline = Pipeline()
    # Add components to your pipeline
    basic_rag_pipeline.add_component("text_embedder", text_embedder)
    basic_rag_pipeline.add_component("retriever", retriever)
    basic_rag_pipeline.add_component("prompt_builder", prompt_builder)
    basic_rag_pipeline.add_component("llm", generator)

    # Now, connect the components to each other
    basic_rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    basic_rag_pipeline.connect("retriever", "prompt_builder.documents")
    basic_rag_pipeline.connect("prompt_builder", "llm")

    return basic_rag_pipeline


@st.cache_data(show_spinner=True)
def query(_pipeline, question):
    results = _pipeline.run({"text_embedder": {"text": question}, "prompt_builder": {"question": question}})
    return results
