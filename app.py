import streamlit as st
import os
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="YouTube QA Assistant", page_icon="🎬", layout="wide")

# Custom CSS for the "Oracle" aesthetic
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
html, body, [class*="css"] { background-color: #0e1117; color: #e8e0d0; }
h1 { font-family: 'Cinzel', serif !important; font-size: 2.6rem !important; letter-spacing: 0.08em;
    background: linear-gradient(135deg, #c8a96e 0%, #e8c97e 50%, #c8a96e 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
h2, h3 { font-family: 'Cinzel', serif !important; color: #c8a96e !important; letter-spacing: 0.04em; }
.stTextInput>div>div>input, .stTextArea textarea {
    background-color: #1a1d27 !important; color: #e8e0d0 !important;
    font-family: 'Crimson Text', serif !important; font-size: 17px !important;
    border: 1px solid #3a3420 !important; border-radius: 6px !important; padding: 12px 16px !important; }
.stTextInput>div>div>input:focus, .stTextArea textarea:focus {
    border-color: #c8a96e !important; box-shadow: 0 0 0 2px rgba(200,169,110,0.2) !important; }
label, .stTextInput label, .stTextArea label {
    font-family: 'Cinzel', serif !important; font-size: 0.85rem !important;
    color: #c8a96e !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; }
.stButton>button {
    background: linear-gradient(135deg, #4a7c59 0%, #3d6b4a 100%) !important;
    color: #f0ead6 !important; font-family: 'Cinzel', serif !important;
    font-size: 15px !important; letter-spacing: 0.08em !important;
    padding: 12px 32px !important; border-radius: 6px !important;
    border: 1px solid #5a8c69 !important; transition: all 0.25s ease !important; }
.stButton>button:hover {
    background: linear-gradient(135deg, #5a8c69 0%, #4a7c59 100%) !important;
    border-color: #7aac89 !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(74,124,89,0.35) !important; }
.info-card { background-color: #14171f; padding: 16px 20px; border-radius: 8px;
    border-left: 5px solid #c8a96e; font-family: 'Crimson Text', serif;
    font-size: 16px; color: #c8d0a0; margin: 12px 0; }
hr { border-color: #2a2620 !important; }
section[data-testid="stSidebar"] { background-color: #0b0e14 !important; border-right: 1px solid #2a2620; }
section[data-testid="stSidebar"] * { color: #c8a96e !important; }
.stAlert { font-family: 'Crimson Text', serif !important; font-size: 16px !important; border-radius: 6px !important; }
.chat-user { background: #1a1d27; border-left: 4px solid #c8a96e; padding: 10px 16px;
    border-radius: 6px; font-family: 'Crimson Text', serif; font-size: 17px; color: #d8c8a0; margin-bottom: 6px; }
.chat-bot { background: #14171f; border-left: 4px solid #4CAF50; padding: 10px 16px;
    border-radius: 6px; font-family: 'Crimson Text', serif; font-size: 18px; color: #e8e0d0; margin-bottom: 14px; }
</style>
""", unsafe_allow_html=True)

st.title("🎬 YouTube QA Assistant")
st.markdown("### Ask anything about a YouTube video — powered by LangChain & HuggingFace")
st.markdown("---")

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Configuration")
st.sidebar.subheader("HuggingFace API Key")
hf_token = st.sidebar.text_input(
    "Enter your HuggingFace API Token:",
    value="",
    type="password",
    help="Get your token from huggingface.co/settings/tokens"
)
st.sidebar.markdown("---")
st.sidebar.subheader("Model Settings")

model_id = st.sidebar.selectbox(
    "LLM Model:",
    options=[
        "Qwen/Qwen2.5-Coder-7B-Instruct", # Updated to a widely supported stable model
        "mistralai/Mistral-7B-Instruct-v0.3"
    ],
    index=0
)
top_k_docs = st.sidebar.slider("Top-K chunks for retrieval:", 2, 8, 4)
st.sidebar.markdown("---")
st.sidebar.info("""
**How it works:**
1. Paste a YouTube URL
2. Click **Load Video**
3. Ask questions below
4. Get AI-powered answers!
""")

# ── Session state ──────────────────────────────────────────────────────────────
for key, default in [("chain", None), ("video_loaded", False), ("video_title", ""), ("chat_history", [])]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Build chain ────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def build_chain(youtube_url, hf_token, model_id, top_k):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token

    loader = YoutubeLoader.from_youtube_url(youtube_url, add_video_info=False)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

    # FIX: Using ChatHuggingFace to handle the "conversational" task requirement
    llm = HuggingFaceEndpoint(
        repo_id=model_id,
        huggingfacehub_api_token=hf_token,
        task="text-generation", # Base task
        temperature=0.1,
        max_new_tokens=512,
    )
    
    chat_model = ChatHuggingFace(llm=llm)

    # Use ChatPromptTemplate for better structure
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert assistant. Answer the user's question using ONLY the provided transcript context. If the answer is not in the context, say you don't know."),
        ("human", "Context:\n{context}\n\nQuestion: {question}")
    ])

    def format_docs(retrieved_docs):
        return "\n\n".join(d.page_content for d in retrieved_docs)

    chain = (
        RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        })
        | prompt
        | chat_model
        | StrOutputParser()
    )
    return chain

# ── Step 1: URL ────────────────────────────────────────────────────────────────
st.subheader("Step 1 · Paste a YouTube URL")
col_url, col_btn = st.columns([4, 1])
with col_url:
    youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
with col_btn:
    load_btn = st.button("▶  Load Video", use_container_width=True)

if load_btn:
    if not youtube_url.strip():
        st.error("Please enter a YouTube URL first.")
    elif not hf_token.strip():
        st.error("Please enter your HuggingFace API token in the sidebar.")
    else:
        with st.spinner("Loading transcript and building knowledge base…"):
            try:
                chain = build_chain(youtube_url, hf_token, model_id, top_k_docs)
                st.session_state.chain = chain
                st.session_state.video_loaded = True
                st.session_state.video_title = youtube_url
                st.session_state.chat_history = []
                st.success("✅ Video loaded! Ask your questions below.")
            except Exception as e:
                st.error(f"Failed to load video: {e}")
                st.info("Check if the video has subtitles enabled or if the model name is correct.")

if st.session_state.video_loaded:
    st.markdown(f'<div class="info-card">📺 Loaded: <code>{st.session_state.video_title}</code></div>', unsafe_allow_html=True)

st.markdown("---")

# ── Step 2: Q&A ───────────────────────────────────────────────────────────────
st.subheader("Step 2 · Ask Your Question")
question = st.text_input("Your Question", placeholder="e.g. What is the main topic of this video?",
    label_visibility="collapsed", disabled=not st.session_state.video_loaded)

col_ask1, col_ask2, col_ask3 = st.columns([1, 2, 1])
with col_ask2:
    ask_btn = st.button("Ask the Oracle", use_container_width=True, disabled=not st.session_state.video_loaded)

if ask_btn:
    if not question.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Consulting the transcript…"):
            try:
                answer = st.session_state.chain.invoke(question)
                st.session_state.chat_history.append((question, answer))
            except Exception as e:
                st.error(f"Error: {e}")

# ── Chat history ───────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("📜 Conversation History")
    for q, a in reversed(st.session_state.chat_history):
        st.markdown(f'<div class="chat-user">🧑 {q}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bot">🤖 {a}</div>', unsafe_allow_html=True)

    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    with col_dl2:
        history_text = "\n\n".join(f"Q: {q}\nA: {a}" for q, a in st.session_state.chat_history)
        st.download_button(label="⬇  Download Conversation", data=history_text,
            file_name="youtube_qa_conversation.txt", mime="text/plain", use_container_width=True)

st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#555; font-family:"Crimson Text",serif; font-size:15px;'>
Built with Streamlit · LangChain · HuggingFace · FAISS<br>YouTube Transcript RAG Pipeline
</div>
""", unsafe_allow_html=True)