import streamlit as st
import httpx
import time

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

    # ✅ Step 1: POST with long timeout (just to submit the job)
    with st.spinner("Submitting research job..."):
        try:
            response = httpx.post(
                f"{api_base}/research",
                json={"query": query, "citation_style": citation_style},
                timeout=30  # زيادة للـ submission بس
            )
            job_id = response.json()["job_id"]
            st.success(f"Job started! ID: {job_id}")
        except Exception as e:
            st.error(f"Failed to start job: {e}")
            st.stop()

    # ✅ Step 2: Poll for results (كل 5 ثواني)
    progress_bar = st.progress(0)
    status_text  = st.empty()
    i = 0
    max_wait = 120  # ينتظر max 10 دقايق (120 * 5 ثواني)

    while i < max_wait:
        time.sleep(5)
        try:
            poll = httpx.get(
                f"{api_base}/research/{job_id}",
                timeout=10
            )
            data = poll.json()
        except Exception as e:
            status_text.text(f"Polling error: {e}, retrying...")
            i += 1
            continue

        progress = min(int((i / max_wait) * 95), 95)
        progress_bar.progress(progress)
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

        i += 1
    else:
        st.warning("⏱️ Timed out after 10 minutes. The job may still be running.")