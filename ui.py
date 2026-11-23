import streamlit as st

from copilot import answer, load_corpus

st.set_page_config(page_title="SentinelRAG")
st.title("SentinelRAG")
st.caption("Search the local security guidance and inspect the evidence behind each answer.")
corpus = load_corpus()
with st.form("search"):
    question = st.text_input("Question", value="How should we restore backups?")
    submitted = st.form_submit_button("Search guidance", type="primary")

if submitted and question.strip():
    result = answer(question, corpus)
    if result["sources"]:
        st.subheader("Matching guidance")
        for rank, source in enumerate(result["sources"], 1):
            with st.container(border=True):
                st.caption(f"Rank {rank} · {source}.txt")
                st.text(corpus[source])
    else:
        st.info(result["answer"])
elif submitted:
    st.info("Enter a question to search the guidance.")

with st.expander(f"Browse all {len(corpus)} source files"):
    for name, passage in corpus.items():
        st.markdown(f"**{name}.txt**")
        st.text(passage)
