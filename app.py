import streamlit as st
import google.generativeai as genai

# 1. 웹 화면 꾸미기
st.set_page_config(page_title="EcoRoute", page_icon="🚲")
st.title("🚲 EcoRoute")
st.subheader("날씨와 고도를 고려한 스마트 경로 플래너")

# 2. API 키 연결 (Streamlit 설정에서 넣을 값)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Streamlit Cloud 설정에서 GOOGLE_API_KEY를 등록해주세요!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. AI 모델 설정 (질문자님의 앱 핵심 지침)
# AI Studio에서 만드셨던 앱의 역할을 아래 system_instruction에 적어주세요.
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. 채팅 히스토리 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 보여주기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 및 답변 생성
if prompt := st.chat_input("어디로 가고 싶으신가요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
