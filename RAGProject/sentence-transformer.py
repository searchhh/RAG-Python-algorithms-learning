import re
import faiss
from sentence_transformers import SentenceTransformer

def build_faiss_index(input_file="clrs_text_optimized.md", index_file="clrs_faiss.index"):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 {input_file}")
        return

    sections = re.split(r'(?=\n## )', text)
    chunks = [section.strip() for section in sections if len(section.strip()) > 50]

    model = SentenceTransformer("all-mpnet-base-v2")

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # 使用内积计算余弦相似度
    index.add(embeddings)

    faiss.write_index(index, index_file)
    print("✅ 向量数据库构建完成！")

if __name__ == "__main__":
    build_faiss_index()
