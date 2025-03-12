import re

def divide_markdown(input_file="raw_text.txt", output_file="clrs_text_optimized.md"):
    """
    读取原始文本，按章节标题拆分，并优化格式。

    Args:
        input_file: 原始文本文件（如书籍目录）。
        output_file: 处理后的 Markdown 文件。
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 {input_file}")
        return

    # 通过章节编号匹配章节标题（如 "1 GETTING STARTED"）
    sections = re.split(r"\n(\d{1,2}(?:\.\d+)? .+)", text)
    chunks = []

    if not sections or len(sections) < 2:
        print("❌ 错误：未能正确拆分章节，请检查文本格式")
        return

    # 处理章节
    for i in range(1, len(sections), 2):  # 跳过偶数索引，偶数索引是章节内容
        title = sections[i].strip()
        content = sections[i + 1].strip() if i + 1 < len(sections) else ""

        # 清理标题，去除行尾的 `....` 或数字
        title = re.sub(r"\s\.*\s*\d*$", "", title)
        chapter_markdown = f"## {title}\n\n{content}"

        chunks.append(chapter_markdown)

    if not chunks:
        print("❌ 错误：未提取到任何章节内容")
        return

    print(f"✅ 处理完成，共 {len(chunks)} 个章节")

    # 保存优化后的 Markdown
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(chunks))

    print(f"✅ 已保存为 `{output_file}`")

if __name__ == "__main__":
    divide_markdown()
