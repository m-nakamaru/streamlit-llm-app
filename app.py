import os
import streamlit as st

# Secrets（Cloud）を最優先で環境変数に流し込む
if "OPENAI_API_KEY" in st.secrets and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# dotenv は開発（ローカル）用。無ければスキップして落ちないようにする
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from dotenv import load_dotenv

load_dotenv()

# app.py
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# .env（ローカル）/ Secrets（Cloud）から読み込み
load_dotenv()

st.set_page_config(page_title="LLM Expert App", page_icon="🤖")
st.title("LLM機能付きWebアプリ（Streamlit × LangChain）")
st.write("""
**使い方**
1. ラジオボタンで「専門家の種類」を選択  
2. テキストを入力 → **実行**  
3. 以下にLLMの回答が出ます  

※ ローカルは `.env` に `OPENAI_API_KEY` を記載。  
※ デプロイ時は Cloud の **Secrets** に `OPENAI_API_KEY` を設定。
""")

persona = st.radio(
    "専門家を選択してください：",
    ["特定行為研修の指導者（看護教育）", "生成AIエンジニア（Python/Streamlit）"],
    horizontal=True
)

user_text = st.text_area("質問・依頼内容：", height=160, placeholder="例：実習記録の評価観点は？ / 最小のStreamlit×LangChainコードは？")

def ask_llm(input_text: str, persona_choice: str) -> str:
    """入力テキストと選択値を受け取り、LLMの回答（文字列）を返す"""
    system_map = {
        "特定行為研修の指導者（看護教育）":
            ("あなたは看護師の特定行為研修の指導者です。"
             "適応判断/病状評価/根拠/実施前後の評価/振り返りの観点で、"
             "要点を箇条書きで簡潔に示し、専門用語に短い補足を付けてください。"),
        "生成AIエンジニア（Python/Streamlit）":
            ("あなたは初学者に教える生成AIエンジニア/講師です。"
             "Streamlit×LangChainの最小実装、設計の意図、落とし穴回避を、"
             "短いコード例と手順で具体的に説明してください。")
    }
    system_msg = system_map.get(persona_choice, "あなたは有能なアシスタントです。")
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg + " 出力は日本語。冗長表現は避け、実務で使える粒度で。"),
        ("human", "{question}")
    ])
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"question": input_text})

if st.button("実行", type="primary"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY が見つかりません。.env または Cloud Secrets を確認してください。")
    elif not user_text.strip():
        st.warning("入力テキストを入れてから実行してください。")
    else:
        with st.spinner("LLMに問い合わせ中..."):
            try:
                st.subheader("回答")
                st.write(ask_llm(user_text, persona))
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")