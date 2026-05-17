import streamlit as st
import httpx, time

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 AI Research Assistant")
st.caption("Powered by GPT-4 + Claude Sonnet multi-agent system")

with st.sidebar:
    st.header("Settings")
    api_base = st.text_input("API URL", value="http://localhost:8000")
    citation_style = st.selectbox("Citation Style", ["APA", "MLA", "Chicago"])
    export_md = st.checkbox("Export Markdown", value=True)

query = st.text_area(
    "Research Query",
    placeholder="e.g. Transformer Architectures in NLP",
    height=100
)

if st.button("🚀 Start Research", type="primary") and query:
    with st.spinner("Submitting research job..."):
        response = httpx.post(
            f"{api_base}/research",
            json={"query": query, "citation_style": citation_style},
            timeout=10
        )
        job_id = response.json()["job_id"]

    progress_bar = st.progress(0)
    status_text  = st.empty()
    i = 0

    while True:
        time.sleep(3)
        poll = httpx.get(f"{api_base}/research/{job_id}", timeout=10)
        data = poll.json()
        i = min(i + 5, 95)
        progress_bar.progress(i)
        status_text.text(f"Status: {data['status']}...")

        if data["status"] == "done":
            progress_bar.progress(100)
            status_text.text("✅ Research complete!")
            st.markdown(data["result"])
            if export_md:
                st.download_button(
                    "📥 Download Markdown",
                    data["result"],
                    file_name="research_report.md",
                    mime="text/markdown"
                )
            break
        elif data["status"] == "error":
            st.error(f"Error: {data['result']}")
            break