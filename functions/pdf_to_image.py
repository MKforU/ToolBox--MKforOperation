import fitz
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ctypes
from ui_theme import RoundButton, BG, TITLE_FG, OK_BG, OK_HO, OK_FG, ENTRY_BG, BTN_FG

# 4K 高分屏修复
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    pass

def run():
    win = tk.Toplevel()
    win.title("📄 PDF 转 图片 工具")
    win.config(bg=BG)

    # 创建居中内容容器
    container = tk.Frame(win, bg=BG)
    container.pack(fill="both", expand=True)

    # 内容区域，居中显示
    content = tk.Frame(container, bg=BG)
    content.pack(padx=20, pady=20, anchor="center")

    pdf_path  = tk.StringVar(value="未选择")
    save_path = tk.StringVar(value="未选择")

    def select_pdf():
        f = filedialog.askopenfilename(parent=win, filetypes=[("PDF 文件", "*.pdf")])
        if f: pdf_path.set(f)

    def select_save():
        d = filedialog.askdirectory(parent=win)
        if d: save_path.set(d)

    def start():
        pdf = pdf_path.get()
        sp  = save_path.get()
        if pdf == "未选择":
            messagebox.showwarning("提示", "请选择PDF"); return
        if sp == "未选择":
            messagebox.showwarning("提示", "请选择保存路径"); return
        try:
            doc    = fitz.open(pdf)
            total  = len(doc)
            matrix = fitz.Matrix(2, 2)
            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=matrix)
                pix.save(os.path.join(sp, f"page_{i+1}.png"))
            doc.close()
            messagebox.showinfo("✅ 完成", f"转换成功！共 {total} 页")
            win.destroy()
        except Exception as e:
            messagebox.showerror("❌ 错误", str(e))

    # 使用 pack 布局
    tk.Label(content, text="📄 PDF 转 图片",
             font=("微软雅黑", 16, "bold"), bg=BG, fg=TITLE_FG).pack(pady=(18, 8))

    RoundButton(content, text="1. 选择 PDF 文件", command=select_pdf,
                width=220, height=44).pack(pady=4)
    tk.Entry(content, textvariable=pdf_path, font=("微软雅黑", 10),
             width=48, state="readonly", relief="flat",
             bg=ENTRY_BG, fg=BTN_FG).pack(pady=2)

    RoundButton(content, text="2. 选择 保存目录", command=select_save,
                width=220, height=44).pack(pady=4)
    tk.Entry(content, textvariable=save_path, font=("微软雅黑", 10),
             width=48, state="readonly", relief="flat",
             bg=ENTRY_BG, fg=BTN_FG).pack(pady=2)

    RoundButton(content, text="3. ✅ 开始转换", command=start,
                bg=OK_BG, hover=OK_HO, fg=OK_FG,
                width=220, height=46).pack(pady=18)

    # 动态计算窗口大小
    win.update_idletasks()
    w = max(win.winfo_reqwidth() + 40, 520)
    h = max(win.winfo_reqheight() + 20, 420)
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    win.minsize(480, 380)
