import os
import streamlit as st
from streamlit_mic_recorder import speech_to_text
from supabase import create_client, Client
from langchain.vectorstores import SupabaseVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import requests
from bs4 import BeautifulSoup
import PyPDF2

# ---------- Utility functions ----------

@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client:
    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    if not url or not key:
        st.warning("Supabase credentials missing")
        return None
    return create_client(url, key)

@st.cache_resource(show_spinner=False)
def get_vector_store(client: Client) -> SupabaseVectorStore:
    embeddings = OpenAIEmbeddings()
    return SupabaseVectorStore(client, embeddings, table_name="documents")


def add_text_to_store(text: str, source: str, store: SupabaseVectorStore):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = [Document(page_content=chunk, metadata={"source": source}) for chunk in splitter.split_text(text)]
    store.add_documents(docs)


def process_pdf(file, store: SupabaseVectorStore):
    reader = PyPDF2.PdfReader(file)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    add_text_to_store(text, file.name, store)


def process_url(url: str, store: SupabaseVectorStore):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n")
    add_text_to_store(text, url, store)


def retrieve_context(query: str, store: SupabaseVectorStore):
    docs = store.similarity_search(query, k=4)
    context = "\n\n".join(d.page_content for d in docs)
    sources = [d.metadata.get("source", "unknown") for d in docs]
    return context, sources


def run_agent(query: str, role: str, prompt: str, store: SupabaseVectorStore, model: ChatOpenAI):
    context, sources = retrieve_context(query, store)
    system_text = f"You are {role}. {prompt}" if role or prompt else ""
    messages = []
    if system_text:
        messages.append(SystemMessage(content=system_text))
    messages.extend([
        HumanMessage(content=f"Use the following context to answer the question. If the context doesn't help, say you don't know.\n\nContext:\n{context}\n\nQuestion: {query}")
    ])
    response = model(messages)
    return response.content, sources

# ---------- Page handlers ----------


def agents_page():
    st.header("Configure Agents")
    for i in range(4):
        with st.container():
            st.subheader(f"Agent {i+1}")
            role = st.text_input(f"Role {i+1}", key=f"role_{i}")
            prompt = st.text_area(f"Prompt {i+1}", key=f"prompt_{i}")
            st.divider()


def home_page():
    st.header("AIWP Bot")
    client = get_supabase_client()
    if client is None:
        st.stop()
    store = get_vector_store(client)

    st.subheader("Add Sources")
    col1, col2 = st.columns(2)
    with col1:
        pdf = st.file_uploader("Upload PDF", type=["pdf"])
        if pdf is not None:
            process_pdf(pdf, store)
            st.success(f"Uploaded {pdf.name}")
    with col2:
        url = st.text_input("Add website URL")
        if st.button("Fetch & Store") and url:
            process_url(url, store)
            st.success(f"Stored {url}")

    st.subheader("Chat")
    query = st.text_input("Enter your question")
    voice = speech_to_text(language="en")
    if voice:
        query = voice
    if st.button("Ask") and query:
        model = ChatOpenAI(model_name="gpt-4o-mini")
        responses = []
        for i in range(4):
            role = st.session_state.get(f"role_{i}", "")
            prompt = st.session_state.get(f"prompt_{i}", "")
            if role or prompt:
                answer, sources = run_agent(query, role, prompt, store, model)
                responses.append((i + 1, answer, sources))
        if not responses:
            # generic answer
            context, _ = retrieve_context(query, store)
            generic_prompt = "Provide a brief answer without citing sources."
            model_resp = model([
                SystemMessage(content=generic_prompt),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
            ])
            st.write(model_resp.content)
        else:
            for idx, ans, src in responses:
                st.markdown(f"**Agent {idx}**: {ans}\n\nSources: {', '.join(src)}")

# ---------- App ----------

if "page" not in st.session_state:
    st.session_state.page = "home"

col_a, col_b = st.columns(2)
if col_a.button("AIWP Bot"):
    st.session_state.page = "home"
if col_b.button("The Agents"):
    st.session_state.page = "agents"

if st.session_state.page == "home":
    home_page()
else:
    agents_page()
