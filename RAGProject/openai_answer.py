import openai

OPENAI_API_KEY = ""

def generate_answer(question, faiss_results):
    prompt = f"请基于以下内容回答问题（如果无关请忽略）：\n\n"
    
    # 过滤掉太短或乱码的段落
    valid_results = [r for r in faiss_results if len(r) > 20]

    for i, result in enumerate(valid_results):
        prompt += f"段落 {i+1}: {result}\n"

    prompt += f"\n问题：{question}\n请分析概念，概念的类比，以及实际现实生活中的用途如果是有关算法的问题，请提供三个LeetCode练习题"

    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ 新版 API 需要创建 client

    response = client.chat.completions.create(  # ✅ 新版 API 语法
        model="gpt-4o",
        messages=[{"role": "system", "content": "你是一个擅长算法的 AI 教授"},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content  # ✅ 读取返回内容
