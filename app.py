import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
import httpx

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    http_client=httpx.Client(verify=False),
)

st.title("streamlitアプリ練習")
user_input = st.chat_input("質問を入力してください")

# session_stateの初期化(if文で「まだ無ければ作る」)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 履歴の表示（for文でループ）
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):  # "user" or "assistant"
        st.write(msg["content"])

if user_input:
    # ユーザーの入力を追加
    st.session_state.messages.append({"role": "user", "content": user_input})
    # ユーザーのメッセージをその場で表示
    with st.chat_message("user"):
        st.write(user_input)
    with st.spinner("回答を生成中..."):
        try:
            response = client.chat.completions.create(
                model = "google/gemma-3-4b-it:free",
                messages = st.session_state.messages    #履歴全体を渡す
            )
            answer = response.choices[0].message.content
            # AIの回答を追加
            st.session_state.messages.append({"role": "assistant", "content": answer})
            # AIの回答をその場で表示
            with st.chat_message("assistant"):
                st.write(answer)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")