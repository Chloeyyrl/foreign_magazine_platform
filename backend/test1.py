import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF

def open_pdf():
    # 创建文件选择对话框让用户选择一个PDF文件
    root = tk.Tk()
    root.withdraw()  # 不显示主窗口
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return "No file selected."

    doc = fitz.open(file_path)  # 打开PDF文件
    html_content = "<html><body>"

    # 遍历每一页
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block['type'] == 0:  # 检查文本块
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        if text.startswith('\t'):
                            html_content += "<br>"
                        style = ""
                        if span['flags'] & 1:  # 粗体
                            style += "font-weight:bold;"
                        if span['flags'] & 2:  # 斜体
                            style += "font-style:italic;"
                        if span['flags'] & 4:  # 上标
                            style += "vertical-align:super;"
                        if span['flags'] & 8:  # 下标
                            style += "vertical-align:sub;"

                        html_content += f'<span style="{style}">{text}</span>'
                    html_content += "<br>"  # 每行后添加换行

    html_content += "</body></html>"
    doc.close()

    # 可以选择保存HTML到文件或直接返回字符串
    with open("output.html", "w") as f:
        f.write(html_content)
    
    return "HTML file has been created."

# 运行函数
print(open_pdf())
