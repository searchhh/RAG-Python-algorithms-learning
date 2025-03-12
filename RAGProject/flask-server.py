from flask import Flask, request, jsonify
import faiss
import json
from sentence_transformers import SentenceTransformer, util
import re

app = Flask(__name__)

try:
    index = faiss.read_index("clrs_faiss.index")
except Exception as e:
    print(f"❌ 无法加载 FAISS 索引: {e}")
    index = None 

chunks = []

try:
    with open("clrs_text_optimized.md", "r", encoding="utf-8") as f:
        text = f.read()
        sections = re.split(r'(^##\s+)', text, flags=re.MULTILINE)
        #chunks = []
        for i in range(1, len(sections), 2):  # 跳过偶数索引，偶数索引是章节内容
            title = sections[i].strip()
            content = sections[i + 1].strip() if i + 1 < len(sections) else ""

            if len(content) < 10:  # 确保内容不为空
                continue

            chapter_markdown = f"## {title}\n\n{content}"
            chunks.append({"header": title, "content": content})

        print(f"✅ 解析完成，存入 {len(chunks)} 个章节")

        for section in sections:
            header_match = re.match(r"##\s+(\d+\.\d+(?:\.\d+)?)\s+(.+)", section)
            if header_match:
                chapter_number = header_match.group(1)
                chapter_title = header_match.group(2)
                header_str = f"## {chapter_number} {chapter_title}\n"
                section_text = section[header_match.end():].strip()
                chunks.append({"header": header_str, "content": section_text})
except FileNotFoundError as e:
    print(f"❌ 错误：找不到Markdown文件 {e}")
    chunks = [] 
    
    


try:
    model = SentenceTransformer("all-mpnet-base-v2")
except Exception as e:
    print(f"❌ 无法加载 SentenceTransformer 模型: {e}")
    model = None 

def filter_relevant_results(question, faiss_results):
    question_embedding = model.encode(question, convert_to_tensor=True)

    if not faiss_results:
        print("⚠️ 没有找到相关内容，跳过相似度计算")
        return []

    result_embeddings = model.encode(faiss_results, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(question_embedding, result_embeddings)[0]

    print(f"🔍 相似度得分: {similarities.tolist()}")

    relevant_indices = (similarities > 0.2).nonzero(as_tuple=True)[0].tolist()  # **放宽阈值**
    
    return [faiss_results[i] for i in relevant_indices] if relevant_indices else faiss_results[:3]  # **确保返回至少 3 条**

@app.route("/query", methods=["POST"])
def query():
    if model is None or index is None:
        return jsonify({"error": "模型或索引未加载"}), 500

    try:
        question = request.json["question"]
    except Exception as e:
        return jsonify({"error": f"请求体 JSON 解析失败: {e}"}), 400

    question_vector = model.encode([question])
    D, I = index.search(question_vector, 5)  
    results = []

    if I is not None and len(I[0]) > 0:
        for i in I[0]:
            if 0 <= i < len(chunks):
                results.append({"header": chunks[i]["header"], "content": chunks[i]["content"]})

    if I is None or len(I[0]) == 0:
        print("⚠️ FAISS 未找到匹配项")
        response_data = {"query": question, "results": [{"header": "", "content": "未找到相关内容"}]}
        print(f"📤 发送给前端的数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        return jsonify(response_data), 200

    # 过滤相关内容
    filtered_results = filter_relevant_results(question, [r["content"] for r in results])

    print(f"🔍 过滤后剩余内容数量: {len(filtered_results)}")

    # ⚠️ **修复 Flask 没有返回数据的问题**
    if not filtered_results:
        response_data = {"query": question, "results": [{"header": "", "content": "未找到相关内容"}]}
    else:
        response_data = {"query": question, "results": results}

    print(f"📤 发送给前端的数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")

    return jsonify(response_data), 200  # **确保返回 JSON 响应**

if __name__ == "__main__":
    app.run(debug=True)
