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
user_input = st.text_input("質問を入力してください")

if st.button("送信"):
    st.write("あなたの質問：" + user_input)
    with st.spinner("回答を生成中..."):
        try:
            response = client.chat.completions.create(
                model = "google/gemma-3-4b-it:free",
                messages = [{"role": "user", "content": user_input}],
            )
            answer = response.choices[0].message.content
            st.write("質問に対する回答：" + answer)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")