import os

file_path = "clrs_text_optimized.md"
if os.path.exists(file_path):
    print(f"✅ 确认 Markdown 文件存在: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"📄 文件大小: {len(content)} 字节")
        print(f"📝 前 500 个字符: \n{content[:500]}")
else:
    print("❌ 错误：Markdown 文件不存在")
