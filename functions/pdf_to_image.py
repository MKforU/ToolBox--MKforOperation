import fitz
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def run():
    # ========== 圆角窗口 + 柔和多巴胺配色 ==========
    win = tk.Tk()
    win.title("📄 PDF 转 图片 工具")
    win.geometry("520x360")
    win.resizable(False, False)
    win.config(bg="#f0f9ff")

    x = (win.winfo_screenwidth() - 520) // 2
    y = (win.winfo_screenheight() - 360) // 2
    win.geometry(f"+{x}+{y}")

    # 变量
    pdf_path = tk.StringVar(value="未选择")
    save_path = tk.StringVar(value="未选择")

    # ========== 选择PDF ==========
    def select_pdf():
        f = filedialog.askopenfilename(filetypes=[("PDF 文件", "*.pdf")])
        if f: pdf_path.set(f)

    # ========== 选择保存目录 ==========
    def select_save():
        d = filedialog.askdirectory()
        if d: save_path.set(d)

    # ========== 开始转换 ==========
    def start():
        pdf = pdf_path.get()
        sp = save_path.get()

        if pdf == "未选择":
            messagebox.showwarning("提示", "请选择PDF")
            return
        if sp == "未选择":
            messagebox.showwarning("提示", "请选择保存路径")
            return

        try:
            doc = fitz.open(pdf)
            total = len(doc)
            for i, page in enumerate(doc):
                pix = page.get_pixmap()
                pix.save(os.path.join(sp, f"page_{i+1}.png"))
            doc.close()
            messagebox.showinfo("✅ 完成", f"转换成功！共 {total} 页")
            win.destroy()
        except Exception as e:
            messagebox.showerror("❌ 错误", str(e))

    # ========== 界面布局 ==========
    tk.Label(
        win, text="PDF 转 图片 工具",
        font=("微软雅黑", 16, "bold"),
        bg="#f0f9ff", fg="#4a5568"
    ).pack(pady=20)

    # 选择PDF
    tk.Button(
        win, text="1. 选择 PDF 文件",
        font=("微软雅黑", 10, "bold"),
        bg="#bae6fd", fg="#1e3a8a",
        relief="flat", cursor="hand2",
        width=20, height=2,
        command=select_pdf
    ).pack(pady=4)

    tk.Entry(win, textvariable=pdf_path, font=("微软雅黑", 10), width=45, state="readonly").pack(pady=2)

    # 选择保存目录
    tk.Button(
        win, text="2. 选择 保存目录",
        font=("微软雅黑", 10, "bold"),
        bg="#bae6fd", fg="#1e3a8a",
        relief="flat", cursor="hand2",
        width=20, height=2,
        command=select_save
    ).pack(pady=4)

    tk.Entry(win, textvariable=save_path, font=("微软雅黑", 10), width=45, state="readonly").pack(pady=2)

    # 开始转换
    tk.Button(
        win, text="3. ✅ 开始转换",
        font=("微软雅黑", 11, "bold"),
        bg="#4ade80", fg="white",
        relief="flat", cursor="hand2",
        width=22, height=2,
        command=start
    ).pack(pady=20)

    win.mainloop()