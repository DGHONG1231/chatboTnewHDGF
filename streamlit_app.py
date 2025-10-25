import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="💬대균의 챗봇", page_icon="🤖")
st.title("💬 대균의 챗봇 ")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT model to generate responses. "
    "To use this app, provide your OpenAI API key. "
    "You can get one [here](https://platform.openai.com/account/api-keys)."
)

# --- API Key ---
# (권장) Streamlit Cloud에서는 Settings > Secrets에 OPENAI_API_KEY로 저장
default_key = st.secrets.get("OPENAI_API_KEY", "")
openai_api_key = st.text_input("OpenAI API Key", type="password", value=default_key)

# --- 초기화 버튼(상단 영역) ---
col1, col2 = st.columns([0.8, 0.2])
with col2:
    if st.button("🧹 리셋버튼입니당 ", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    st.stop()

# --- OpenAI Client ---
client = OpenAI(api_key=openai_api_key)

# --- 세션 상태 초기화 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 기존 대화 표시 ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 입력 & 응답 ---
if prompt := st.chat_input("What is up?"):
    # 사용자 메시지 표시/저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 응답 생성 (스트리밍)
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",           # ✅ 최신 사용 가능 모델
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )

        with st.chat_message("assistant"):
            response_text = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response_text})

    except Exception as e:
        # 인증/빌링/모델 문제 등 전부 여기로 잡아서 알려줌
        st.error(f"OpenAI API error: {e}")
