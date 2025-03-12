import streamlit as st
import requests
from openai_answer import generate_answer

st.title("📘 CLRS AI Assistant")

question = st.text_input("Please Input the question：")

if st.button("查询"):
    url = "http://127.0.0.1:5000/query"
    try:
        response = requests.post(url, json={"question": question}).json()
        if "error" in response:
            st.error(f"服务器错误：{response['error']}")
        else:
            st.subheader("📖 Related Knowledge：")
            for result in response["results"]:
                st.markdown(result["header"])  
                st.write(result["content"])
                st.markdown("---") 

            st.subheader("🤖 GPT Explanation：")
            filtered_content = [r["content"] for r in response["results"] if len(r["content"]) > 20]
            if filtered_content:
                answer = generate_answer(question, filtered_content)
                st.write(answer)
            else:
                st.write("未找到相关内容，请换个问题试试。")

    except requests.exceptions.RequestException as e:
        st.error(f"连接服务器失败：{e}")
    except Exception as e:
        st.error(f"发生未知错误：{e}")
