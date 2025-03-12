import faiss

try:
    index = faiss.read_index("clrs_faiss.index")
    print("✅ FAISS 索引成功加载！")
    print(f"索引大小: {index.ntotal}")  # 检查是否存入数据
except Exception as e:
    print(f"❌ 无法加载 FAISS 索引: {e}")
