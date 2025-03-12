import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    """
    从 PDF 文件中提取文本，并进行初步清理。

    Args:
        pdf_path: PDF 文件路径。

    Returns:
        提取后的原始文本。
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            extracted_text = [pdf.pages[i].extract_text() for i in range(num_pages) if pdf.pages[i].extract_text()]
        return "\n".join(extracted_text[4:])  # 跳过前 4 页目录
    except Exception as e:
        print(f"❌ PDF 提取失败: {e}")
        return None

def process_formula(text):
    """
    识别和处理文本中的公式。这里只是简单的替换，可以根据实际情况添加 Mathpix API 调用等复杂处理。
    """
    # 1. 基本公式模式识别 (示例，需根据实际情况修改)
    formula_pattern = r"\$(.*?)\$"  # 识别行内 LaTeX 公式
    text = re.sub(formula_pattern, "[FORMULA]", text) #替换为特殊标记，后续可以处理

    # 2. 更复杂的公式模式识别 (示例，需根据实际情况修改)
    # 识别包含特定数学符号的表达式
    formula_pattern2 = r"(\b(?:log|sin|cos|sum|int|in|forall|exists|lim)\b.*?)"
    text = re.sub(formula_pattern2, "[FORMULA]", text) #替换为特殊标记，后续可以处理

    # 3.  清除公式周围多余的空格
    text = re.sub(r"\s*\[FORMULA]\s*", "[FORMULA]", text)

    return text

def main(pdf_path, output_file="raw_text.txt"):
    """
    主函数：提取文本、处理公式，并将处理后的文本保存到文件。
    """
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text:
        print("❌ 无法从 PDF 提取文本，流程终止。")
        return

    processed_text = process_formula(raw_text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(processed_text)
    print(f"✅ 提取完成，公式已标记，已保存到 {output_file}")

if __name__ == "__main__":
    pdf_path = "D:/books/AC Textbooke/level04/Programming Language Research/ALTR.pdf"
    main(pdf_path)