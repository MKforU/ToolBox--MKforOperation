import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import tempfile
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pdfkit

def run():
    win = tk.Tk()
    win.title("📄 文件转PDF工具")
    win.geometry("560x480")
    win.resizable(False, False)
    win.config(bg="#f0f9ff")

    # 窗口居中
    x = (win.winfo_screenwidth() - 560) // 2
    y = (win.winfo_screenheight() - 480) // 2
    win.geometry(f"+{x}+{y}")

    # 变量定义
    file_path = tk.StringVar(value="未选择")
    save_dir = tk.StringVar(value="未选择")
    selected_file = None

    # 支持的文件类型
    SUPPORTED_TYPES = [
        ("所有支持格式", "*.docx *.doc *.png *.jpg *.jpeg *.gif *.bmp *.tiff *.txt *.html *.htm"),
        ("Word文档", "*.docx *.doc"),
        ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
        ("文本/网页", "*.txt *.html *.htm"),
    ]

    # 选择待转换文件
    def select_file():
        nonlocal selected_file
        fp = filedialog.askopenfilename(filetypes=SUPPORTED_TYPES)
        if not fp:
            return
        file_path.set(fp)
        selected_file = fp

    # 选择保存目录
    def select_save():
        d = filedialog.askdirectory()
        if d:
            save_dir.set(d)

    # 图片转PDF
    def image_to_pdf(img_path, pdf_path):
        try:
            img = Image.open(img_path)
            img = img.convert('RGB')
            c = canvas.Canvas(pdf_path, pagesize=A4)
            a4_width, a4_height = A4
            img_width, img_height = img.size

            # 等比例缩放适配A4
            scale = min(a4_width / img_width, a4_height / img_height)
            new_width = img_width * scale
            new_height = img_height * scale

            c.drawImage(img_path, 0, 0, width=new_width, height=new_height)
            c.save()
            return True
        except Exception as e:
            raise Exception(f"图片转换失败：{str(e)}")

    # DOCX/DOC 转 PDF（优先用 docx2pdf，保留完整格式；回退到 COM 接口）
    def docx_to_pdf(doc_path, pdf_path):
        try:
            from docx2pdf import convert
            convert(doc_path, pdf_path)
            return True
        except ImportError:
            pass

        # 回退：用 Word COM 接口（需要本机安装 Word）
        try:
            import comtypes.client
            word = comtypes.client.CreateObject('Word.Application')
            word.Visible = False
            doc = word.Documents.Open(os.path.abspath(doc_path))
            doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)  # 17 = wdFormatPDF
            doc.Close()
            word.Quit()
            return True
        except Exception as e:
            raise Exception(
                f"DOCX 转换失败：{str(e)}\n\n"
                "请安装 docx2pdf：\npip install docx2pdf\n"
                "（需要本机已安装 Microsoft Word）"
            )

    # TXT / HTML 转 PDF（依赖 wkhtmltopdf）
    def text_to_pdf(src_path, pdf_path):
        try:
            pdfkit.from_file(src_path, pdf_path)
            return True
        except Exception as e:
            raise Exception(f"文本/网页转换失败：{str(e)}\n\n请确认已安装 wkhtmltopdf 并加入 PATH。")

    # 核心转换逻辑
    def start_convert():
        nonlocal selected_file
        if not selected_file:
            messagebox.showwarning("提示", "请先选择待转换文件！")
            return
        if save_dir.get() == "未选择":
            messagebox.showwarning("提示", "请选择保存目录！")
            return

        try:
            # 生成输出文件名
            folder, name_ext = os.path.split(selected_file)
            name, ext = os.path.splitext(name_ext)
            out_file = f"{name}_转PDF.pdf"
            out_path = os.path.join(save_dir.get(), out_file)

            # 根据文件类型选择转换方式
            ext_lower = ext.lower()
            if ext_lower in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
                image_to_pdf(selected_file, out_path)
            elif ext_lower in ['.docx', '.doc']:
                docx_to_pdf(selected_file, out_path)
            elif ext_lower in ['.txt', '.html', '.htm']:
                text_to_pdf(selected_file, out_path)
            else:
                messagebox.showerror("错误", f"不支持的文件格式：{ext}")
                return

            messagebox.showinfo(
                "✅ 转换完成",
                f"文件转换成功！\n\n"
                f"源文件：{selected_file}\n"
                f"输出文件：\n{out_path}"
            )
            win.destroy()

        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{str(e)}")

    # ==================== UI界面（保持原有风格） ====================
    tk.Label(
        win, text="文件转PDF工具",
        font=("微软雅黑", 16, "bold"),
        bg="#f0f9ff", fg="#374151"
    ).pack(pady=20)

    # 选择文件
    tk.Button(
        win, text="1. 选择待转换文件",
        font=("微软雅黑", 10, "bold"),
        bg="#bae6fd", fg="#1e3a8a",
        relief="flat", cursor="hand2",
        width=24, height=2,
        command=select_file
    ).pack(pady=3)
    tk.Entry(win, textvariable=file_path, font=("微软雅黑", 10), width=55, state="readonly").pack(pady=2)

    # 选择保存目录
    tk.Button(
        win, text="2. 选择保存目录",
        font=("微软雅黑", 10, "bold"),
        bg="#bae6fd", fg="#1e3a8a",
        relief="flat", cursor="hand2",
        width=24, height=2,
        command=select_save
    ).pack(pady=3)
    tk.Entry(win, textvariable=save_dir, font=("微软雅黑", 10), width=55, state="readonly").pack(pady=5)

    # 开始转换按钮
    tk.Button(
        win, text="✅ 开始转换为PDF",
        font=("微软雅黑", 11, "bold"),
        bg="#4ade80", fg="white",
        relief="flat", cursor="hand2",
        width=22, height=2,
        command=start_convert
    ).pack(pady=40)

    win.mainloop()
