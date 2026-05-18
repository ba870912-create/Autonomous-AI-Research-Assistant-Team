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

    with st.spinner("Submitting research job..."):
        try:
            response = httpx.post(
                f"{api_base}/research",
                json={"query": query, "citation_style": citation_style},
                timeout=30
            )
            job_id = response.json()["job_id"]
            st.success(f"Job started! ID: {job_id}")
        except Exception as e:
            st.error(f"Failed to start job: {e}")
            st.stop()

    progress_bar = st.progress(0)
    status_text = st.empty()
    i = 0
    max_wait = 120
    final_result = None

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
            final_result = data["result"]
            st.markdown(final_result)

            #  Markdown download
            if export_md:
                st.download_button(
                    "📥 Download Markdown",
                    data=final_result,
                    file_name="research_report.md",
                    mime="text/markdown"
                )

            # PDF download
            try:
                pdf_response = httpx.post(
                    f"{api_base}/export-pdf",
                    json={"job_id": job_id, "markdown": final_result},
                    timeout=30
                )
                if pdf_response.status_code == 200:
                    st.download_button(
                        label="📄 Download PDF",
                        data=pdf_response.content,
                        file_name="research_report.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.warning("PDF generation failed")
            except Exception as e:
                st.warning(f"PDF export error: {e}")

            break

        elif data["status"] == "error":
            st.error(f"Error: {data['result']}")
            break

        i += 1
    else:
        st.warning("⏱️ Timed out after 10 minutes. The job may still be running.")

#  Research History
st.divider()
st.subheader("📚 Research History")
if st.button("🔄 Load History"):
    try:
        hist_response = httpx.get(f"{api_base}/history", timeout=10)
        history = hist_response.json().get("history", [])
        if history:
            for item in history:
                status_icon = "✅" if item["status"] == "done" else "❌"
                st.write(f"{status_icon} **{item['query']}** — {item['citation_style']} — {item['created_at'][:19]}")
        else:
            st.info("No research history yet.")
    except Exception as e:
        st.error(f"Failed to load history: {e}")