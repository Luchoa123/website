import re
import streamlit as st
from openai import OpenAI

# =====================================
# CONFIG
# =====================================

API_KEY = st.secrets["GROQ_API_KEY"]

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# =====================================
# PAGE
# =====================================

st.set_page_config(
    page_title="Hành chính công",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Hành chính công")
st.caption("Powered by Groq + Qwen")

# =====================================
# CHAT HISTORY
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Bạn là trợ lý AI tiếng Việt. "
                "Trả lời trực tiếp và ngắn gọn. "
                "Không hiển thị quá trình suy nghĩ. "
                "Không xuất thẻ <think>."
            )
        }
    ]

# Display chat history (skip system prompt)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =====================================
# USER INPUT
# =====================================

prompt = st.chat_input("Nhập câu hỏi...")

if prompt:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate answer
    with st.chat_message("assistant"):

        try:

            response = client.chat.completions.create(
                model="qwen/qwen3-32b",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=2048
            )

            answer = response.choices[0].message.content

            # Remove think tags if model returns them
            answer = re.sub(
                r"<think>.*?</think>",
                "",
                answer,
                flags=re.DOTALL
            ).strip()

            # Fallback
            if "</think>" in answer:
                answer = answer.split("</think>")[-1].strip()

        except Exception as e:

            answer = f"❌ Error: {str(e)}"

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.header("Settings")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "Bạn là trợ lý AI tiếng Việt. "
                    "Trả lời trực tiếp và ngắn gọn. "
                    "Không hiển thị quá trình suy nghĩ. "
                    "Không xuất thẻ <think>."
                )
            }
        ]

        st.rerun()