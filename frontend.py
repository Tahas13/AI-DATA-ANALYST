#Step3: Build Streamlit frontend
import streamlit as st
from main import get_data_from_database
st.set_page_config(
    page_title="AI Data Analyst 2.0",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Data Analyst 2.0")
st.markdown("Ask questions about your data in natural language.")

user_query = st.text_area("💬 Enter your question:", placeholder="e.g., Total products sold in 2025")

if st.button("Analyze"):
    if user_query.strip() == "":
        st.warning("Please enter a question to analyze.")
    else:
        import time
        status = st.status("Running analysis...", expanded=True)
        try:
            with status:
                st.write("⏳ Step 1: Extracting database schema...")
                t_start = time.time()
                result = get_data_from_database(user_query)
                total_time = time.time() - t_start
                st.write(f"✅ Done in {total_time:.1f}s")
            status.update(label="Analysis complete!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="Analysis failed", state="error", expanded=True)
            st.error(f"❌ Error: {e}")
            st.stop()

        rows = result.get("rows", [])
        columns = result.get("columns", [])
        sql_used = result.get("query", "")

        if not rows:
            st.info("No records found for this query.")
        else:
            st.markdown("### 📊 Query Results")
            table_data = [dict(zip(columns, row)) for row in rows]
            st.dataframe(table_data, use_container_width=True)
            st.caption(f"🕒 Total time: {total_time:.1f}s")

        with st.expander("🔍 Show generated SQL"):
            st.code(sql_used, language="sql")

st.markdown("""
    <style>
    textarea {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)