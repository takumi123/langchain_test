import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# Streamlitの設定
st.title("🤖 AI チャットボット")
st.write("ChatGPTとGeminiを切り替えて使用できます")

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# モデルの選択
model_option = st.selectbox(
    "使用するモデルを選択してください",
    ("ChatGPT", "Gemini")
)

# モデルの初期化
def get_llm():
    if model_option == "ChatGPT":
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            streaming=True
        )
    else:
        return ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            convert_system_message_to_human=True
        )

# チャット履歴の表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("メッセージを入力してください"):
    # ユーザーメッセージの表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIの応答
    with st.chat_message("assistant"):
        llm = get_llm()
        message_placeholder = st.empty()
        full_response = ""

        # ストリーミング応答の処理
        for chunk in llm.stream(prompt):
            full_response += chunk.content
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # 応答の保存
    st.session_state.messages.append({"role": "assistant", "content": full_response})
