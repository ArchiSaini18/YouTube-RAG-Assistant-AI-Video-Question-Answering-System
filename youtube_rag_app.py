import os
import streamlit as st
import warnings
warnings.simplefilter("ignore")

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube RAG Assistant",
    page_icon="▶",
    layout="wide",
)

# ══════════════════════════════════════════════════════════════════════════════
#  CSS — Indigo Midnight · Dark Theme · matching Breast.py style
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

/* ── Variables ── */
:root {
    --bg:          #080c18;
    --surface:     #0e1220;
    --surface2:    #141828;
    --border:      #1a2040;
    --border-hi:   #243060;
    --indigo:      #818cf8;
    --indigo-light:#c7d2fe;
    --indigo-dim:  rgba(129,140,248,0.13);
    --red:         #f43f5e;
    --green:       #10b981;
    --amber:       #f59e0b;
    --text:        #e8eaf6;
    --muted:       #4a5480;
    --head-font:   'Playfair Display', Georgia, serif;
    --mono-font:   'IBM Plex Mono', monospace;
    --glow-indigo: 0 0 28px rgba(129,140,248,0.22);
}

/* ── Global ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background: var(--bg) !important;
    font-family: var(--mono-font) !important;
    color: var(--text) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 4px; }

/* ══════════════════════════════
   HERO
══════════════════════════════ */
.hero {
    position: relative;
    padding: 3rem 3.5rem 2.5rem;
    margin-bottom: 2.5rem;
    background: linear-gradient(135deg, #080c18 0%, #0d1228 60%, #080c18 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 60% 50% at 90% 50%, rgba(129,140,248,0.09) 0%, transparent 70%),
        radial-gradient(ellipse 40% 60% at 10% 80%, rgba(129,140,248,0.04) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--indigo), var(--indigo-light), transparent);
}
.hero-tag {
    display: inline-block;
    font-family: var(--mono-font);
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--indigo);
    background: var(--indigo-dim);
    border: 1px solid rgba(129,140,248,0.28);
    border-radius: 4px;
    padding: 0.25rem 0.8rem;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: var(--head-font) !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    line-height: 1.1 !important;
    letter-spacing: -0.01em;
    margin: 0 0 0.6rem 0 !important;
}
.hero h1 span {
    background: linear-gradient(135deg, var(--indigo), var(--indigo-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.82rem;
    color: var(--muted);
    letter-spacing: 0.04em;
}
.hero-badge {
    position: absolute;
    right: 3.5rem; top: 50%;
    transform: translateY(-50%);
    width: 80px; height: 80px;
    border-radius: 50%;
    background: var(--indigo-dim);
    border: 1px solid rgba(129,140,248,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.2rem;
    box-shadow: var(--glow-indigo);
}
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--indigo);
    box-shadow: 0 0 6px var(--indigo);
    margin-right: 0.5rem;
    vertical-align: middle;
}
.status-badge {
    font-size: 0.7rem; letter-spacing: 0.1em;
    color: var(--muted); text-transform: uppercase;
}

/* ── Stat Chips ── */
.stat-row {
    display: flex; gap: 0.8rem; margin-bottom: 2.5rem; flex-wrap: wrap;
}
.stat-chip {
    background: var(--surface2);
    border: 1px solid var(--border-hi);
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-size: 0.78rem;
    color: var(--muted);
    letter-spacing: 0.05em;
}
.stat-chip span {
    font-family: var(--head-font);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--indigo);
    margin-right: 0.35rem;
}

/* ══════════════════════════════
   SECTION LABELS
══════════════════════════════ */
.section-label {
    font-family: var(--mono-font);
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--indigo);
    border-left: 2px solid var(--indigo);
    padding-left: 0.7rem;
    margin-bottom: 1.4rem;
    margin-top: 0.5rem;
}

/* ══════════════════════════════
   FORM PANELS
══════════════════════════════ */
.form-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.8rem 2rem 2rem;
    position: relative;
    margin-bottom: 1.4rem;
    transition: border-color 0.3s;
}
.form-panel:hover { border-color: var(--border-hi); }
.form-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 1.5rem; right: 1.5rem; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(129,140,248,0.15), transparent);
}

/* ══════════════════════════════
   INPUTS
══════════════════════════════ */
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {
    font-family: var(--mono-font) !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin-bottom: 0.2rem !important;
}
[data-testid="stTextInput"] input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--mono-font) !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 0.8rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--indigo) !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.12) !important;
    outline: none !important;
}
[data-testid="stTextArea"] textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--mono-font) !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--indigo) !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.12) !important;
    outline: none !important;
}

/* ══════════════════════════════
   SLIDER
══════════════════════════════ */
[data-testid="stSlider"] label {
    font-family: var(--mono-font) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ══════════════════════════════
   BUTTONS
══════════════════════════════ */
[data-testid="stButton"] > button {
    width: 100% !important;
    height: 58px !important;
    background: linear-gradient(135deg, #3730a3, var(--indigo), #c7d2fe) !important;
    color: #080c18 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: var(--head-font) !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(129,140,248,0.3), 0 1px 0 rgba(255,255,255,0.08) inset !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(129,140,248,0.45), 0 2px 0 rgba(255,255,255,0.12) inset !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ══════════════════════════════
   CHAT MESSAGES
══════════════════════════════ */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 0.5rem;
}
.msg-user {
    align-self: flex-end;
    background: var(--indigo-dim);
    border: 1px solid rgba(129,140,248,0.28);
    border-radius: 12px 12px 2px 12px;
    padding: 0.9rem 1.2rem;
    max-width: 85%;
    font-size: 0.85rem;
    color: var(--text);
    line-height: 1.6;
}
.msg-user .msg-label {
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--indigo);
    margin-bottom: 0.4rem;
}
.msg-assistant {
    align-self: flex-start;
    background: var(--surface);
    border: 1px solid var(--border-hi);
    border-radius: 12px 12px 12px 2px;
    padding: 0.9rem 1.2rem;
    max-width: 92%;
    font-size: 0.85rem;
    color: var(--text);
    line-height: 1.7;
    position: relative;
}
.msg-assistant::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, var(--indigo), transparent);
    border-radius: 12px 12px 0 0;
}
.msg-assistant .msg-label {
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}

/* ── Idle / Info cards ── */
.idle-card {
    background: var(--surface);
    border: 1px dashed var(--border-hi);
    border-radius: 14px;
    padding: 3.5rem 2rem;
    text-align: center; color: var(--muted);
}
.idle-icon { font-size: 2.8rem; margin-bottom: 1rem; opacity: 0.45; }
.idle-head {
    font-family: var(--head-font);
    font-size: 1.2rem; color: #2a3060; margin-bottom: 0.4rem;
}
.idle-body { font-size: 0.8rem; line-height: 1.6; }

/* ── Info card (loaded) ── */
.info-card {
    background: var(--surface2);
    border: 1px solid rgba(129,140,248,0.22);
    border-left: 3px solid var(--indigo);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.78rem;
    color: var(--muted);
    margin-bottom: 1.2rem;
    line-height: 1.6;
}
.info-card strong { color: var(--indigo); }

/* ── Error card ── */
.error-card {
    background: rgba(244,63,94,0.07);
    border: 1px solid rgba(244,63,94,0.3);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #fb7185;
    margin-bottom: 1rem;
}

/* ── Layout helpers ── */
[data-testid="stHorizontalBlock"] {
    gap: 1.4rem !important;
    align-items: stretch !important;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
}
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chain" not in st.session_state:
    st.session_state.chain = None
if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False
if "video_id" not in st.session_state:
    st.session_state.video_id = ""
if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">⬡ Retrieval-Augmented Generation Platform</div>
    <h1>YouTube <span>RAG</span><br>Assistant</h1>
    <p class="hero-sub">
        LangChain · FAISS · HuggingFace · Qwen3 &nbsp;·&nbsp;
        <span class="status-dot"></span>
        <span class="status-badge">Pipeline Ready</span>
    </p>
    <div class="hero-badge">▶</div>
</div>
""", unsafe_allow_html=True)

# ── Main Layout ───────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.0, 1.1], gap="medium")

# ════════════════════════════════════════════════════════════
#  LEFT COLUMN — Configuration
# ════════════════════════════════════════════════════════════
with left_col:

    # Section 01 — API & Model Config
    st.markdown('<div class="section-label">01 — API & Model Configuration</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-panel">', unsafe_allow_html=True)

    hf_token = st.text_input(
        "HuggingFace API Token",
        type="password",
        placeholder="hf_xxxxxxxxxxxxxxxx",
        help="Your HuggingFace Hub API token"
    )

    model_id = st.text_input(
        "LLM Model ID",
        value="Qwen/Qwen3-Coder-Next",
        help="HuggingFace model repo ID"
    )

    c1, c2 = st.columns(2)
    with c1:
        max_tokens = st.slider("Max New Tokens", 50, 500, 200, step=50)
    with c2:
        temperature = st.slider("Temperature", 0.1, 1.0, 0.5, step=0.1)

    st.markdown('</div>', unsafe_allow_html=True)

    # Section 02 — Video & RAG Config
    st.markdown('<div class="section-label">02 — Video & Retrieval Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-panel">', unsafe_allow_html=True)

    video_url = st.text_input(
        "YouTube Video URL or Video ID",
        placeholder="https://youtube.com/watch?v=jmmW0F0biz0  or  jmmW0F0biz0",
        help="Paste a full YouTube URL or just the video ID"
    )

    c3, c4 = st.columns(2)
    with c3:
        chunk_size = st.slider("Chunk Size", 200, 2000, 1000, step=100)
    with c4:
        chunk_overlap = st.slider("Chunk Overlap", 0, 400, 200, step=50)

    top_k = st.slider("Top-K Retrieved Chunks", 1, 5, 2)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    load_btn = st.button("⬡ Load Video & Build Index →")

    # ── Load Pipeline ─────────────────────────────────────────────────────────
    if load_btn:
        if not hf_token:
            st.markdown('<div class="error-card">⚠ Please provide your HuggingFace API token.</div>', unsafe_allow_html=True)
        elif not video_url.strip():
            st.markdown('<div class="error-card">⚠ Please enter a YouTube video URL or ID.</div>', unsafe_allow_html=True)
        else:
            # Extract video ID
            vid = video_url.strip()
            if "v=" in vid:
                vid = vid.split("v=")[-1].split("&")[0]
            elif "youtu.be/" in vid:
                vid = vid.split("youtu.be/")[-1].split("?")[0]

            with st.spinner("Fetching transcript and building vector index…"):
                try:
                    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token

                    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
                    from langchain_text_splitters import RecursiveCharacterTextSplitter
                    from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
                    from langchain_community.vectorstores import FAISS
                    from langchain_core.prompts import PromptTemplate
                    from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
                    from langchain_core.output_parsers import StrOutputParser

                    # Fetch transcript
                    api = YouTubeTranscriptApi()
                    transcript_list = api.fetch(vid, languages=["en"])
                    transcript = " ".join(chunk.text for chunk in transcript_list)

                    # Split
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=chunk_size, chunk_overlap=chunk_overlap
                    )
                    chunks = splitter.create_documents([transcript])

                    # Embed + FAISS
                    embeddings = HuggingFaceEmbeddings(
                        model_name="sentence-transformers/all-MiniLM-L6-v2"
                    )
                    vector_store = FAISS.from_documents(chunks, embeddings)
                    retriever = vector_store.as_retriever(
                        search_type='similarity', search_kwargs={'k': top_k}
                    )

                    # LLM + Chain
                    llm = HuggingFaceEndpoint(
                        repo_id=model_id,
                        task="conversational",
                        max_new_tokens=max_tokens,
                        temperature=temperature,
                    )
                    model_chat = ChatHuggingFace(llm=llm)

                    prompt = PromptTemplate(
                        template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
                        input_variables=['context', 'question']
                    )

                    def format_docs(retrieved_docs):
                        return "\n\n".join(doc.page_content for doc in retrieved_docs)

                    parallel_chain = RunnableParallel({
                        'context': retriever | RunnableLambda(format_docs),
                        'question': RunnablePassthrough()
                    })

                    main_chain = parallel_chain | prompt | model_chat | StrOutputParser()

                    st.session_state.chain = main_chain
                    st.session_state.video_loaded = True
                    st.session_state.video_id = vid
                    st.session_state.chunk_count = len(chunks)
                    st.session_state.messages = []
                    st.success(f"✓ Indexed {len(chunks)} chunks from video `{vid}`")

                except TranscriptsDisabled:
                    st.markdown('<div class="error-card">⚠ Transcripts are disabled for this video. Try another video.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-card">⚠ Error: {str(e)}</div>', unsafe_allow_html=True)

    # ── Stats row (shown after loading) ───────────────────────────────────────
    if st.session_state.video_loaded:
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-chip"><span>{st.session_state.chunk_count}</span> Chunks Indexed</div>
            <div class="stat-chip"><span>{top_k}</span> Top-K Retrieval</div>
            <div class="stat-chip"><span>MiniLM</span> Embeddings</div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  RIGHT COLUMN — Chat Interface
# ════════════════════════════════════════════════════════════
with right_col:
    st.markdown('<div class="section-label">03 — Ask the Video</div>', unsafe_allow_html=True)

    if not st.session_state.video_loaded:
        st.markdown("""
        <div class="idle-card">
            <div class="idle-icon">◈</div>
            <div class="idle-head">Awaiting Video</div>
            <div class="idle-body">
                Enter your HuggingFace token and a<br>
                YouTube video URL on the left,<br>
                then click <em>Load Video &amp; Build Index</em>.
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        # Info banner
        st.markdown(f"""
        <div class="info-card">
            <strong>▶ Video loaded:</strong> <code>{st.session_state.video_id}</code><br>
            Ask any question about the video content below.
        </div>
        """, unsafe_allow_html=True)

        # Chat history
        if st.session_state.messages:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="msg-user">
                        <div class="msg-label">You</div>
                        {msg["content"]}
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="msg-assistant">
                        <div class="msg-label">⬡ Assistant</div>
                        {msg["content"]}
                    </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # Question input
        question = st.text_area(
            "Your Question",
            placeholder="e.g. What are the five types of neural networks discussed?",
            height=90,
            key="question_input"
        )

        ask_btn = st.button("Ask →")

        if ask_btn:
            if not question.strip():
                st.markdown('<div class="error-card">⚠ Please type a question first.</div>', unsafe_allow_html=True)
            else:
                st.session_state.messages.append({"role": "user", "content": question.strip()})
                with st.spinner("Retrieving context and generating answer…"):
                    try:
                        answer = st.session_state.chain.invoke(question.strip())
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                        st.rerun()
                    except Exception as e:
                        st.markdown(f'<div class="error-card">⚠ Generation error: {str(e)}</div>', unsafe_allow_html=True)

        # Clear chat
        if st.session_state.messages:
            if st.button("Clear Chat"):
                st.session_state.messages = []
                st.rerun()

    st.markdown("""
    <div style="margin-top:2rem;font-size:0.72rem;color:#2a3060;
                border-top:1px solid #1a2040;padding-top:1rem;line-height:1.7">
        This tool is for educational and informational purposes only.
        Answers are grounded solely in the provided video transcript via RAG.
        Always verify information from original sources.
    </div>
    """, unsafe_allow_html=True)
