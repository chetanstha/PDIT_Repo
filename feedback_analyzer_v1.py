import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="🗣️ Feedback Summarizer - Version 1", layout="wide")

st.title("🗣️ Multi-Channel Feedback Summarizer (Version-1)")
st.markdown("Upload feedback data and let GenAI summarize suggestions, tone, and flags.")

# Sidebar for API key
with st.sidebar:
    st.header("🔐 Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password")

# Upload feedback file
st.subheader("📤 Upload Feedback (CSV or Excel)")
uploaded_file = st.file_uploader("Choose a feedback file", type=["csv", "xlsx"])

if uploaded_file and openai_api_key:
    # Read data
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")
        st.write("### Preview of Uploaded Data", df.head())

        # Select column with feedback
        feedback_column = st.selectbox("📝 Select the column containing feedback text:", df.columns)

        if st.button("🧠 Summarize Feedback"):
            openai.api_key = openai_api_key
            feedbacks = df[feedback_column].dropna().tolist()
            summaries = []

            with st.spinner("Summarizing feedback using GenAI..."):
                for fb in feedbacks:
                    prompt = f"Summarize the tone, main point, and any suggestion or complaint in the following feedback:{fb}"
                    try:
                        response = openai.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=150
                        )
                        summary = response.choices[0].message.content.strip()
                    except Exception as e:
                        summary = f"[Error: {str(e)}]"
                    summaries.append(summary)

            df['GenAI Summary'] = summaries
            st.success("✅ Feedback summarized!")
            st.write("### Summarized Feedback", df[[feedback_column, 'GenAI Summary']])

            # Optional download
            st.download_button("📥 Download with Summaries", data=df.to_csv(index=False), file_name="summarized_feedback.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("Upload a feedback file and enter your OpenAI API key to get started.")