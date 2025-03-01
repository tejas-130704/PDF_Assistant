import streamlit as st
from phi.agent import Agent
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.model.groq import Groq
from phi.vectordb.pgvector import PgVector
from phi.embedder.sentence_transformer import SentenceTransformerEmbedder
import os

# Streamlit UI
st.title("PDF Assistant")
st.write("Ask any questions related to the PDF!")

# Sidebar Inputs
st.sidebar.header("Configuration")
groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
pdf_url = st.sidebar.text_input("Enter PDF URL")
load_button = st.sidebar.button("Load Knowledge Base")

# Initialize session state for agent if not set
if "agent" not in st.session_state:
    st.session_state.agent = None

if load_button and groq_api_key and pdf_url:
    os.environ["GROQ_API_KEY"] = groq_api_key
    
    # Initialize Embedder
    db_url = "postgresql+psycopg://root:test@localhost:5432/mydb"
    embedder = SentenceTransformerEmbedder(model="BAAI/bge-large-en-v1.5", dimensions=1024)
    
    # Initialize Knowledge Base
    knowledge_base = PDFUrlKnowledgeBase(
        urls=[pdf_url],
        vector_db=PgVector(table_name="embeddings", db_url=db_url, embedder=embedder)
    )
    knowledge_base.load()
    
    if knowledge_base:  # Ensure knowledge base is properly loaded
        st.session_state.agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            knowledge_base=knowledge_base,
            show_tool_calls=True,
            search_knowledge=True,
            read_chat_history=True,
        )
        st.sidebar.success("Knowledge Base Loaded Successfully!")
    else:
        st.sidebar.error("Failed to load knowledge base. Please check your PDF URL.")

# Chat Interface
user_query = st.text_input("Enter your query:")
if st.button("Get Response"):
    if st.session_state.agent:
        response = st.session_state.agent.run(user_query)
        st.write("### Response:")
        # st.write(response)
        st.write(response.content)
        
    else:
        st.error("Please load the knowledge base first.")
