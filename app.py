import streamlit as st
import google.generativeai as genai
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🔒 GEMINI_API_KEY missing from your .env file.")
    st.stop()

genai.configure(api_key=api_key)

st.set_page_config(
    page_title="PromptCraft Studio Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* ── Base & Background ── */
.stApp {
    background: linear-gradient(135deg, #0A0F1D 0%, #0D1528 50%, #0A1020 100%);
    min-height: 100vh;
}

/* ── Animated Header Title ── */
.hero-title {
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #00E6FF, #A855F7, #EC4899, #00E6FF);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s ease infinite;
    margin: 0;
    line-height: 1.1;
}

@keyframes shimmer {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-sub {
    color: #64748B;
    font-size: 0.9rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Mode Cards ── */
.mode-card {
    background: linear-gradient(135deg, var(--card-from), var(--card-to));
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.mode-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px var(--card-glow); }
.mode-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--card-from), var(--card-to));
}

/* ── Metric Badges ── */
.stat-row {
    display: flex;
    gap: 10px;
    margin: 12px 0;
}
.stat-badge {
    flex: 1;
    background: #141B2D;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
}
.stat-num {
    font-size: 1.6rem;
    font-weight: 800;
    color: #00E6FF;
    display: block;
}
.stat-label {
    font-size: 0.7rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Chat Messages ── */
div[data-testid="stChatMessage"] {
    background: #0F172A !important;
    border: 1px solid #1E293B !important;
    border-radius: 16px !important;
    padding: 18px !important;
    margin-bottom: 12px !important;
    transition: border-color 0.2s;
}
div[data-testid="stChatMessage"]:hover {
    border-color: #334155 !important;
}
div[data-testid="stChatMessage"][data-testid*="user"] {
    border-left: 3px solid #A855F7 !important;
}
div[data-testid="stChatMessage"][data-testid*="assistant"] {
    border-left: 3px solid #00E6FF !important;
}

/* ── Sidebar ── */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080D1A 0%, #0A0F1D 100%) !important;
    border-right: 1px solid #1E293B !important;
}
div[data-testid="stSidebar"] .stSelectbox label,
div[data-testid="stSidebar"] .stCheckbox label,
div[data-testid="stSidebar"] p,
div[data-testid="stSidebar"] h1,
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3 {
    color: #CBD5E1 !important;
}

/* ── Select Box ── */
div[data-testid="stSelectbox"] > div > div {
    background: #141B2D !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1E293B, #0F172A) !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: #CBD5E1 !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: #00E6FF !important;
    color: #00E6FF !important;
    transform: translateY(-1px) !important;
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #A855F7, #7C3AED) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-weight: 700 !important;
}

/* ── Chat Input ── */
div[data-testid="stChatInput"] > div {
    background: #141B2D !important;
    border: 1px solid #334155 !important;
    border-radius: 16px !important;
}
div[data-testid="stChatInput"] textarea {
    color: #E2E8F0 !important;
    background: transparent !important;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: #0A1020 !important;
    border: 1px solid #1E293B !important;
    border-radius: 12px !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #00E6FF !important;
}

/* ── Code Block ── */
.stCodeBlock {
    background: #060B14 !important;
    border: 1px solid #1E293B !important;
    border-radius: 10px !important;
}

/* ── Divider ── */
hr {
    border-color: #1E293B !important;
    margin: 16px 0 !important;
}

/* ── Pulse Dot ── */
.pulse-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #22C55E;
    animation: pulse 2s infinite;
    margin-right: 6px;
    vertical-align: middle;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

/* ── Progress Bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #00E6FF, #A855F7) !important;
    border-radius: 99px !important;
}

/* ── Tabs (Token Debugger) ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0F172A !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748B !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: #1E293B !important;
    color: #00E6FF !important;
}

/* ── Tooltip Tag ── */
.tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-right: 5px;
}
.tag-cyan  { background: #0E3A4A; color: #00E6FF; border: 1px solid #00E6FF44; }
.tag-purple{ background: #2A1454; color: #C084FC; border: 1px solid #A855F744; }
.tag-pink  { background: #3A1030; color: #F472B6; border: 1px solid #EC489944; }
.tag-green { background: #0A2E1A; color: #4ADE80; border: 1px solid #22C55E44; }
.tag-amber { background: #2E1E04; color: #FBBF24; border: 1px solid #F59E0B44; }

/* ── Watermark ── */
.watermark {
    text-align: center;
    color: #1E293B;
    font-size: 0.7rem;
    letter-spacing: 2px;
    padding: 20px 0 10px;
}
</style>
""", unsafe_allow_html=True)



for key, default in {
    "messages": [],
    "total_queries": 0,
    "session_start": datetime.now().strftime("%H:%M"),
    "last_mode": None,
    "token_count": 0,
    "history_log": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


MODES = {
    "👶 Explain Like I'm 5": {
        "prompt": "You are a patient, warm teacher who explains any topic using simple everyday analogies, short sentences, and zero jargon. Use playful comparisons and emojis where helpful. Always end with a fun fact the user wouldn't expect.",
        "color_from": "#0E2A3A", "color_to": "#0A1F30",
        "border": "#0EA5E940", "glow": "#0EA5E920",
        "tag": "tag-cyan", "tag_text": "SIMPLIFY"
    },
    "📊 System Thinker (First Principles)": {
        "prompt": "You are a Socratic philosopher and scientist. Deconstruct the user's topic into its most fundamental, irreducible truths. Rebuild understanding step-by-step from axioms. Use numbered reasoning chains, challenge assumptions explicitly, and finish with a second-order insight most people miss.",
        "color_from": "#1A0A3A", "color_to": "#120826",
        "border": "#A855F740", "glow": "#A855F720",
        "tag": "tag-purple", "tag_text": "FIRST PRINCIPLES"
    },
    "🧠 Interactive Quiz Master": {
        "prompt": "Transform the user's topic into an engaging 3-question multiple-choice quiz. Format: **Q[N]: [Question]** followed by A) B) C) D) options on separate lines. After all questions, add a **Answers & Explanations** section revealing the correct answers with rich context. Make questions progressively harder.",
        "color_from": "#2A0A1A", "color_to": "#1E0814",
        "border": "#EC489940", "glow": "#EC489920",
        "tag": "tag-pink", "tag_text": "QUIZ"
    },
    "💻 Code Mentor & Debugger": {
        "prompt": "You are a Staff Engineer at a FAANG company with 15 years of experience. Analyze the user's code or concept. Provide: 1) A diagnosis of any issues, 2) Optimized, refactored code in clean Markdown code blocks with language tags, 3) Inline comments explaining each key decision, 4) Time/space complexity analysis, 5) One advanced pattern or best practice the user should adopt.",
        "color_from": "#0A2A0A", "color_to": "#081E08",
        "border": "#22C55E40", "glow": "#22C55E20",
        "tag": "tag-green", "tag_text": "CODE"
    },
    "📅 Actionable Study Blueprint": {
        "prompt": "You are an expert curriculum designer and learning coach. Build a detailed 4-week study roadmap for the given topic. Each week: **Week N — [Theme]** with daily goals (Mon–Fri), key concepts to master, recommended resources (books/courses/videos), a hands-on mini-project, and a self-check question. End with a motivational note.",
        "color_from": "#2A1A00", "color_to": "#1E1200",
        "border": "#F59E0B40", "glow": "#F59E0B20",
        "tag": "tag-amber", "tag_text": "STUDY PLAN"
    },
    "🎯 Socratic Interview Coach": {
        "prompt": "You are a senior hiring manager at a top tech firm. Generate 5 role-specific behavioral + technical interview questions for the topic the user provides. For each question: give the question itself, explain what the interviewer is really testing, provide a model STAR-format answer, and list two common mistakes candidates make. End with a confidence-building tip.",
        "color_from": "#1A0A2A", "color_to": "#12081E",
        "border": "#C084FC40", "glow": "#C084FC20",
        "tag": "tag-purple", "tag_text": "INTERVIEW"
    },
    "🔥 Devil's Advocate": {
        "prompt": "You are a brilliant contrarian thinker. Your job is to challenge every assumption in the user's input. Present the strongest possible counter-arguments with evidence and logic. Force the user to stress-test their thinking. Be respectful but intellectually ruthless. End with the one critique that is hardest to refute.",
        "color_from": "#2A0808", "color_to": "#1E0606",
        "border": "#EF444440", "glow": "#EF444420",
        "tag": "tag-pink", "tag_text": "CHALLENGE"
    },
}

with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 20px;">
            <p style="color:#00E6FF; font-weight:900; font-size:1.1rem; letter-spacing:1px; margin:0;">
                ⚡ PROMPTCRAFT
            </p>
            <p style="color:#334155; font-size:0.7rem; letter-spacing:2px; margin:0;">STUDIO PRO v3.0</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**🤖 Model Engine**")
    selected_model = st.selectbox(
        "LLM Engine",
        ["gemini-3.5-flash", "gemini-3.1-pro"],
        label_visibility="collapsed"
    )
    model_badge = "⚡ Flash" if "flash" in selected_model else "🧠 Pro"
    st.markdown(f"""
        <div style="background:#0F172A; border:1px solid #1E293B; border-radius:8px;
                    padding:8px 12px; display:flex; align-items:center; gap:8px; margin-bottom:16px;">
            <span class="pulse-dot"></span>
            <span style="color:#CBD5E1; font-size:0.8rem;">{model_badge} — Live</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**🎨 Prompt Mode**")
    mode = st.selectbox(
        "Prompt Mode",
        list(MODES.keys()),
        label_visibility="collapsed"
    )

    cfg = MODES[mode]
    st.markdown(f"""
        <div style="background:linear-gradient(135deg,{cfg['color_from']},{cfg['color_to']});
                    border:1px solid {cfg['border']}; border-radius:12px;
                    padding:12px 14px; margin:8px 0 16px;">
            <span class="tag {cfg['tag']}">{cfg['tag_text']}</span>
            <p style="color:#94A3B8; font-size:0.75rem; margin:8px 0 0; line-height:1.4;">
                {cfg['prompt'][:100]}…
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📊 Session Stats**")
    st.markdown(f"""
        <div class="stat-row">
            <div class="stat-badge">
                <span class="stat-num">{st.session_state.total_queries}</span>
                <span class="stat-label">Queries</span>
            </div>
            <div class="stat-badge">
                <span class="stat-num" style="color:#A855F7;">{len(st.session_state.messages)}</span>
                <span class="stat-label">Messages</span>
            </div>
        </div>
        <div class="stat-row">
            <div class="stat-badge" style="flex:1;">
                <span class="stat-num" style="color:#4ADE80; font-size:1rem;">
                    {st.session_state.session_start}
                </span>
                <span class="stat-label">Session Start</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**🛠️ Dev Tools**")
    show_debug = st.checkbox("Show Prompt Injection Layer", value=False)
    show_history = st.checkbox("Show Query Timeline", value=False)
    temperature = st.slider("🌡️ Temperature", 0.0, 1.0, 0.7, 0.05)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.total_queries = 0
            st.session_state.history_log = []
            st.rerun()
    with col_b:
        if st.button("📋 Copy All"):
            all_text = "\n\n".join(
                f"[{m['role'].upper()}]\n{m['content']}"
                for m in st.session_state.messages
            )
            st.session_state["copy_buffer"] = all_text
            st.toast("✅ Copied to session buffer!")


# ─────────────────────────────────────────────────────
#  Main Layout
# ─────────────────────────────────────────────────────
st.markdown("""
    <div style="padding: 10px 0 24px;">
        <p class="hero-title">PromptCraft Studio</p>
        <p class="hero-sub">Advanced Prompt Engineering Workspace · 7 AI Modes · Multi-Model</p>
    </div>
""", unsafe_allow_html=True)

# Active Mode Banner
cfg = MODES[mode]
st.markdown(f"""
    <div style="background:linear-gradient(135deg,{cfg['color_from']},{cfg['color_to']});
                border:1px solid {cfg['border']}; border-radius:14px;
                padding:14px 20px; margin-bottom:20px; display:flex;
                align-items:center; gap:14px;">
        <div style="font-size:1.8rem;">{mode.split()[0]}</div>
        <div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span class="tag {cfg['tag']}">{cfg['tag_text']}</span>
                <span style="color:#475569; font-size:0.75rem;">
                    {selected_model.upper()} · TEMP {temperature}
                </span>
            </div>
            <p style="color:#CBD5E1; font-size:0.85rem; margin:0; line-height:1.4;">
                {cfg['prompt'][:140]}…
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

if show_history and st.session_state.history_log:
    with st.expander("⏱️ Query Timeline", expanded=False):
        for i, entry in enumerate(reversed(st.session_state.history_log[-10:])):
            st.markdown(f"""
                <div style="background:#0F172A; border-left:3px solid {entry['color']};
                            border-radius:0 8px 8px 0; padding:8px 14px; margin-bottom:6px;">
                    <span style="color:#475569; font-size:0.7rem;">{entry['time']} · {entry['model']}</span><br>
                    <span style="color:#CBD5E1; font-size:0.8rem;">
                        <b style="color:{entry['color']};">{entry['mode_icon']}</b> {entry['query'][:80]}…
                    </span>
                </div>
            """, unsafe_allow_html=True)


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input ──
if user_input := st.chat_input("Ask anything — choose a mode on the left to shape the response…"):

    # Empty input guard
    if not user_input.strip():
        st.warning("⚠️ Please enter something before sending.")
        st.stop()

    cfg = MODES[mode]

    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.total_queries += 1

    # Log to history
    st.session_state.history_log.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "model": selected_model,
        "mode_icon": mode.split()[0],
        "query": user_input,
        "color": "#00E6FF" if "flash" in selected_model else "#A855F7",
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Debug Layer
    if show_debug:
        with st.expander("🛠️ Injected Prompt Layer", expanded=True):
            tab1, tab2 = st.tabs(["System Prompt", "Full Payload"])
            with tab1:
                st.code(cfg["prompt"], language="markdown")
            with tab2:
                payload = {
                    "model": selected_model,
                    "temperature": temperature,
                    "system_prompt_chars": len(cfg["prompt"]),
                    "user_input_chars": len(user_input),
                    "total_chars": len(cfg["prompt"]) + len(user_input),
                    "mode": mode,
                }
                st.json(payload)

    # Inference
    with st.chat_message("assistant"):
        loading_messages = [
            f"🔮 Routing to {selected_model}…",
            f"🧠 Applying {cfg['tag_text']} persona…",
            "✨ Generating response…",
        ]
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, msg_text in enumerate(loading_messages):
            status_text.markdown(
                f"<p style='color:#475569; font-size:0.8rem;'>{msg_text}</p>",
                unsafe_allow_html=True
            )
            progress_bar.progress((i + 1) * 30)
            time.sleep(0.3)

        try:
            model_obj = genai.GenerativeModel(
                selected_model,
                generation_config=genai.GenerationConfig(temperature=temperature)
            )
            orchestrated_prompt = f"{cfg['prompt']}\n\nUser Request: {user_input}"
            response = model_obj.generate_content(orchestrated_prompt)

            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()

            response_text = response.text

            # Render markdown response
            st.markdown(response_text)

            # Append assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })

            # ── Action Row ──
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 2, 3])

            with col1:
                st.download_button(
                    label="📥 Export as .md",
                    data=f"# PromptCraft Export\n**Mode:** {mode}\n**Model:** {selected_model}\n\n---\n\n**Prompt:**\n{user_input}\n\n---\n\n**Response:**\n{response_text}",
                    file_name=f"promptcraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                )
            with col2:
                st.download_button(
                    label="📄 Export as .txt",
                    data=f"Mode: {mode}\nModel: {selected_model}\n\nPrompt: {user_input}\n\nResponse:\n{response_text}",
                    file_name=f"promptcraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                )
            with col3:
                char_count = len(response_text)
                word_count = len(response_text.split())
                st.markdown(f"""
                    <div style="background:#0F172A; border:1px solid #1E293B; border-radius:10px;
                                padding:10px 14px; display:flex; gap:16px; align-items:center;">
                        <span style="color:#475569; font-size:0.75rem;">
                            <b style="color:#00E6FF;">{word_count}</b> words ·
                            <b style="color:#A855F7;">{char_count}</b> chars
                        </span>
                    </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Inference failed: {str(e)}")
            st.info("💡 Check your API key and model availability in your .env file.")

# ── Footer ──
st.markdown("""
    <div class="watermark">
        PROMPTCRAFT STUDIO PRO · POWERED BY GOOGLE GEMINI · BUILT WITH STREAMLIT
    </div>
""", unsafe_allow_html=True)
