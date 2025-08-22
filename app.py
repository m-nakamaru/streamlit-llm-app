# --- app.py の先頭に ---
import os, streamlit as st
if "OPENAI_API_KEY" in st.secrets and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass
# -----------------------

# app.py —— 課題要件フル対応版（Streamlit × LangChain）
import os
import streamlit as st

# --- Secrets（Cloud）を最優先で環境変数へ ---
if "OPENAI_API_KEY" in st.secrets and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# --- dotenv はローカル開発用。無ければスキップして落ちない ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- LangChain（0.2系） ---
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ========== UI ==========
st.set_page_config(page_title="LLM Expert App", page_icon="🤖")
st.title("LLM機能付きWebアプリ（Streamlit × LangChain）")

st.write(
    """
**使い方**
1. 下のラジオで「専門家の振る舞い」を選びます。  
2. テキスト欄に質問/依頼を入力し、**[実行]** を押します。  
3. 下部にLLMの回答が表示されます。  
"""
)

persona = st.radio(
    "専門家を選択してください：",
    ["特定行為研修の指導者（看護教育）", "生成AIエンジニア（Python/Streamlit）"],
    horizontal=True,
)

user_text = st.text_area(
    "質問・依頼内容：",
    height=160,
    placeholder="例）実習記録の評価観点を5つに整理して／Streamlit×LangChainの最小コードを教えて",
)


# ========== LLM呼び出し関数（要件：入力テキスト＆選択値を受けて回答文字列を返す） ==========
def ask_llm(input_text: str, persona_choice: str) -> str:
    """選択された専門家設定でLLMに問い合わせ、回答（文字列）を返す。"""
    system_map = {
        "特定行為研修の指導者（看護教育）": (
            "あなたは看護師の特定行為研修の指導者です。"
            "適応判断/病状評価/根拠/実施前後の評価/振り返りの観点で、"
            "要点を箇条書きで簡潔に示し、専門用語には短い補足を付けてください。"
        ),
        "生成AIエンジニア（Python/Streamlit）": (
            "あなたは初学者に教える生成AIエンジニア/講師です。"
            "Streamlit と LangChain の最小実装、設計の意図、落とし穴回避を、"
            "短いコード例と手順で具体的に説明してください。"
        ),
    }
    system_msg = system_map.get(persona_choice, "あなたは有能なアシスタントです。")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_msg + " 出力は日本語。冗長表現は避け、実務で役立つ粒度で。"),
            ("human", "{question}"),
        ]
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"question": input_text})


# ========== 実行 ==========
run = st.button("実行", type="primary", disabled=not user_text.strip())

if run:
    if not os.getenv("OPENAI_API_KEY"):
        st.error(
            "OPENAI_API_KEY が見つかりません。.env（ローカル）または Cloud Secrets を設定してください。"
        )
    else:
        with st.spinner("LLMに問い合わせ中..."):
            try:
                answer = ask_llm(user_text, persona)
                st.subheader("回答")
                st.write(answer)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")