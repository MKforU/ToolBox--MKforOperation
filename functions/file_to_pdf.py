import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pdfkit
import ctypes
from ui_theme import RoundButton, BG, TITLE_FG, OK_BG, OK_HO, OK_FG, ENTRY_BG, BTN_FG

# 4K 高分屏修复
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    pass

def run():
    win = tk.Toplevel()
    win.title("📄 文件转PDF工具")
    win.config(bg=BG)

    # 创建居中内容容器
    container = tk.Frame(win, bg=BG)
    container.pack(fill="both", expand=True)

    # 内容区域，居中显示
    content = tk.Frame(container, bg=BG)
    content.pack(padx=20, pady=20, anchor="center")

    file_path     = tk.StringVar(value="未选择")
    save_dir      = tk.StringVar(value="未选择")
    selected_file = None

    SUPPORTED_TYPES = [
        ("所有支持格式", "*.docx *.doc *.png *.jpg *.jpeg *.gif *.bmp *.tiff *.txt *.html *.htm"),
        ("Word文档",   "*.docx *.doc"),
        ("图片文件",   "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
        ("文本/网页",  "*.txt *.html *.htm"),
    ]

    def select_file():
        nonlocal selected_file
        fp = filedialog.askopenfilename(filetypes=SUPPORTED_TYPES)
        if not fp: return
        file_path.set(fp)
        selected_file = fp

    def select_save():
        d = filedialog.askdirectory()
        if d: save_dir.set(d)

    def image_to_pdf(img_path, pdf_path):
        try:
            img = Image.open(img_path).convert('RGB')
            c   = canvas.Canvas(pdf_path, pagesize=A4)
            aw, ah = A4
            iw, ih = img.size
            scale  = min(aw / iw, ah / ih)
            c.drawImage(img_path, 0, 0, width=iw*scale, height=ih*scale)
            c.save()
        except Exception as e:
            raise Exception(f"图片转换失败：{str(e)}")

    def docx_to_pdf(doc_path, pdf_path):
        try:
            from docx2pdf import convert
            convert(doc_path, pdf_path); return
        except ImportError:
            pass
        try:
            import comtypes.client
            word = comtypes.client.CreateObject('Word.Application')
            word.Visible = False
            doc = word.Documents.Open(os.path.abspath(doc_path))
            doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
            doc.Close(); word.Quit()
        except Exception as e:
            raise Exception(
                f"DOCX 转换失败：{str(e)}\n\n"
                "请安装 docx2pdf：\npip install docx2pdf\n"
                "（需要本机已安装 Microsoft Word）")

    def text_to_pdf(src_path, pdf_path):
        try:
            pdfkit.from_file(src_path, pdf_path)
        except Exception as e:
            raise Exception(f"文本/网页转换失败：{str(e)}\n\n请确认已安装 wkhtmltopdf 并加入 PATH。")

    def start_convert():
        nonlocal selected_file
        if not selected_file:
            messagebox.showwarning("提示", "请先选择待转换文件！"); return
        if save_dir.get() == "未选择":
            messagebox.showwarning("提示", "请选择保存目录！"); return
        try:
            folder, name_ext = os.path.split(selected_file)
            name, ext = os.path.splitext(name_ext)
            out_path  = os.path.join(save_dir.get(), f"{name}_转PDF.pdf")
            ext_lower = ext.lower()
            if ext_lower in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
                image_to_pdf(selected_file, out_path)
            elif ext_lower in ['.docx', '.doc']:
                docx_to_pdf(selected_file, out_path)
            elif ext_lower in ['.txt', '.html', '.htm']:
                text_to_pdf(selected_file, out_path)
            else:
                messagebox.showerror("错误", f"不支持的文件格式：{ext}"); return
            messagebox.showinfo("✅ 转换完成",
                f"文件转换成功！\n\n源文件：{selected_file}\n输出文件：\n{out_path}")
            win.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{str(e)}")

    # 使用 pack 布局
    tk.Label(content, text="📁 文件转 PDF",
             font=("微软雅黑", 16, "bold"), bg=BG, fg=TITLE_FG).pack(pady=(18, 8))

    RoundButton(content, text="1. 选择待转换文件", command=select_file,
                width=230, height=44).pack(pady=3)
    tk.Entry(content, textvariable=file_path, font=("微软雅黑", 10),
             width=52, state="readonly", relief="flat",
             bg=ENTRY_BG, fg=BTN_FG).pack(pady=2)

    RoundButton(content, text="2. 选择保存目录", command=select_save,
                width=230, height=44).pack(pady=3)
    tk.Entry(content, textvariable=save_dir, font=("微软雅黑", 10),
             width=52, state="readonly", relief="flat",
             bg=ENTRY_BG, fg=BTN_FG).pack(pady=4)

    RoundButton(content, text="✅ 开始转换为PDF", command=start_convert,
                bg=OK_BG, hover=OK_HO, fg=OK_FG,
                width=230, height=46).pack(pady=30)

    # 动态计算窗口大小
    win.update_idletasks()
    w = max(win.winfo_reqwidth() + 40, 560)
    h = max(win.winfo_reqheight() + 20, 480)
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    win.minsize(500, 420)
