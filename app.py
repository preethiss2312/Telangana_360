"""app.py - Telangana 360 (run with: streamlit run app.py)

Pages: Chat (RAG chatbot), Timeline, Map, Quiz
"""
import pandas as pd
import streamlit as st

import features
import rag

st.set_page_config(page_title="Telangana 360", page_icon="🏛️", layout="wide")

# ---------- Look and feel (CSS) ----------
# Colours: ikat indigo, madder red, turmeric, Pochampally white
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bitter:wght@600;800&family=Noto+Sans+Telugu:wght@400;600&display=swap');

html, body, [class*="css"], .stMarkdown, .stChatInput textarea {
    font-family: 'Noto Sans Telugu', 'Segoe UI', sans-serif;
}
.stApp { background: #FAFAF7; }

/* ikat-style border strip at the very top */
.stApp::before {
    content: "";
    display: block;
    height: 10px;
    background:
        repeating-linear-gradient(135deg, #1B2A6B 0 10px, #FAFAF7 10px 14px,
                                  #B23A3A 14px 24px, #FAFAF7 24px 28px);
}

.hero { padding: 1.2rem 0 0.4rem 0; }
.hero h1 {
    font-family: 'Bitter', serif; font-weight: 800; font-size: 3rem;
    color: #1B2A6B; margin: 0; letter-spacing: -0.5px;
}
.hero p { color: #5a5a52; font-size: 1.05rem; margin: 0.2rem 0 0 0; max-width: 62ch; }
h2, h3 { font-family: 'Bitter', serif; color: #1B2A6B; }

[data-testid="stSidebar"] { background: #1B2A6B; }
[data-testid="stSidebar"] * { color: #F4F1E8 !important; }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { font-family: 'Bitter', serif; }

.stButton > button {
    border: 1.5px solid #1B2A6B; color: #1B2A6B; background: #FFFFFF;
    border-radius: 6px; text-align: left; font-weight: 600;
}
.stButton > button:hover { background: #E0A526; border-color: #E0A526; color: #1B2A6B; }
.stButton > button:focus-visible { outline: 3px solid #B23A3A; outline-offset: 2px; }

[data-testid="stChatMessage"] { border-left: 4px solid #E0A526; background: #FFFFFF; }

/* timeline */
.tl-item { display: flex; gap: 1.2rem; padding: 0.8rem 0; border-bottom: 1px dashed #d8d4c8; }
.tl-year { font-family: 'Bitter', serif; font-weight: 800; font-size: 1.4rem;
           color: #B23A3A; min-width: 4.5rem; }
.tl-title { font-weight: 600; color: #1B2A6B; }
.tl-tag { display: inline-block; font-size: 0.72rem; padding: 1px 8px; margin-left: 8px;
          border-radius: 10px; background: #E0A526; color: #1B2A6B; }
.tl-text { color: #4a4a44; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## Telangana 360")
    page = st.radio("Go to", ["Chat", "Timeline", "Map", "Quiz"])
    st.divider()
    use_ai = st.toggle("Write chat answers with AI (slower)", value=True)
    if st.button("Rebuild knowledge base"):
        with st.spinner("Reading data folder..."):
            rag.get_collection(rebuild=True)
        st.success("Done. Data files re-indexed.")

# ---------- Header ----------
st.markdown(
    """
<div class="hero">
  <h1>Telangana 360</h1>
  <p>Telangana's history, its struggle for statehood, its land and its culture,
  in one place. Answers come from the facts in the knowledge base.</p>
</div>
""",
    unsafe_allow_html=True,
)


# ---------- Page: Chat ----------
QUICK = [
    "Who was the last Nizam of Hyderabad?",
    "What was Operation Polo?",
    "Who was Komaram Bheem?",
    "When was Telangana state formed?",
    "Which rivers flow through Telangana?",
    "Why is Ramappa Temple famous?",
]


def set_pending(q):
    st.session_state.pending = q


def show_sources(sources):
    if sources:
        with st.expander("Sources used"):
            for s in sources:
                st.markdown(f"**{s['topic'].replace('_', ' ').title()}**")
                st.write(s["text"])


def page_chat():
    cols = st.columns(3)
    for i, q in enumerate(QUICK):
        cols[i % 3].button(q, on_click=set_pending, args=(q,), use_container_width=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            show_sources(m.get("sources"))

    typed = st.chat_input("Ask about Telangana...")
    question = typed or st.session_state.pop("pending", None)
    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the knowledge base..."):
            passages = rag.retrieve(question)
            if not passages:
                answer = (
                    "I could not find this in the knowledge base. "
                    "Try different words, or add the facts to a file in the data folder."
                )
            elif use_ai:
                answer = rag.generate_answer(question, passages)
            else:
                answer = passages[0]["text"]
        st.markdown(answer)
        show_sources(passages)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": passages}
    )


# ---------- Page: Timeline ----------
def page_timeline():
    st.subheader("Timeline of Telangana")
    chosen = st.multiselect("Show", features.CATEGORIES, default=features.CATEGORIES)
    events = [e for e in features.TIMELINE if e[3] in chosen]
    html = ""
    for year, title, text, cat in sorted(events):
        html += (
            f'<div class="tl-item"><div class="tl-year">{year}</div>'
            f'<div><span class="tl-title">{title}</span>'
            f'<span class="tl-tag">{cat}</span>'
            f'<div class="tl-text">{text}</div></div></div>'
        )
    st.markdown(html or "Pick at least one category.", unsafe_allow_html=True)


# ---------- Page: Map ----------
def page_map():
    st.subheader("Key places of Telangana")
    df = pd.DataFrame(features.PLACES, columns=["place", "lat", "lon", "note"])
    st.map(df, latitude="lat", longitude="lon", size=6000)
    st.caption("Locations are approximate.")
    st.dataframe(df[["place", "note"]], hide_index=True, use_container_width=True)


# ---------- Page: Quiz ----------
def page_quiz():
    st.subheader("Test yourself")
    with st.form("quiz_form"):
        answers = []
        for i, item in enumerate(features.QUIZ):
            answers.append(
                st.radio(f"{i + 1}. {item['q']}", item["options"], index=None, key=f"q{i}")
            )
        submitted = st.form_submit_button("Submit answers")

    if submitted:
        score = 0
        for a, item in zip(answers, features.QUIZ):
            if a == item["answer"]:
                score += 1
            else:
                st.error(f"{item['q']}  Correct answer: {item['answer']}")
        st.success(f"You scored {score} out of {len(features.QUIZ)}")


# ---------- Router ----------
if page == "Chat":
    page_chat()
elif page == "Timeline":
    page_timeline()
elif page == "Map":
    page_map()
else:
    page_quiz()