import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="EcoRoute", page_icon="🚲")
st.title("🚲 EcoRoute")
st.caption("날씨와 고도를 고려한 스마트 경로 플래너")

# 2. API 키 설정 확인
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Streamlit Cloud 설정(Secrets)에 GOOGLE_API_KEY를 등록해주세요.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. 모델 설정 (404 에러 방지를 위해 명칭 수정)
# 'gemini-1.5-flash'가 안 될 경우 'models/gemini-1.5-flash'를 시도합니다.
try:
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash", 
        system_instruction="너는 친환경 경로 안내 전문가 EcoRoute야. 사용자의 목적지에 따라 날씨와 고도를 분석해줘."
    )
    # 모델이 정상 작동하는지 가볍게 테스트
    test_response = model.generate_content("hello")
except Exception as e:
    # 만약 위 이름도 안 된다면 최신형 'flash-latest'로 재시도
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

# 4. 채팅 메시지 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리
if prompt := st.chat_input("어디로 가고 싶으신가요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
