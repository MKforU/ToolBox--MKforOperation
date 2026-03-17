import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import ctypes
from ui_theme import RoundButton, BG, TITLE_FG, OK_BG, OK_HO, OK_FG, ENTRY_BG, BTN_FG

# 4K 高分屏修复
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    pass

def run():
    win = tk.Toplevel()
    win.title("📊 表格去重工具")
    win.config(bg=BG)

    # 创建居中内容容器
    container = tk.Frame(win, bg=BG)
    container.pack(fill="both", expand=True)

    # 内容区域，居中显示
    content = tk.Frame(container, bg=BG)
    content.pack(padx=20, pady=20, anchor="center")

    file_path = tk.StringVar(value="未选择")
    save_dir  = tk.StringVar(value="未选择")
    mode      = tk.StringVar(value="col")
    df        = None
    columns   = []

    def select_file():
        nonlocal df, columns
        fp = filedialog.askopenfilename(
            filetypes=[("Excel 文件", "*.xlsx"), ("Excel 旧版", "*.xls")])
        if not fp: return
        file_path.set(fp)
        try:
            df = pd.read_excel(fp, dtype=str)
            columns = df.columns.tolist()
            col_cb["values"] = columns
            if columns: col_cb.current(0)
        except Exception as e:
            messagebox.showerror("错误", f"读取失败：{str(e)}")

    def select_save():
        d = filedialog.askdirectory()
        if d: save_dir.set(d)

    def start_remove():
        nonlocal df
        if df is None:
            messagebox.showwarning("提示", "请先选择Excel文件！"); return
        if save_dir.get() == "未选择":
            messagebox.showwarning("提示", "请选择保存目录！"); return
        try:
            before = len(df)
            if mode.get() == "col":
                new_df = df.drop_duplicates(subset=[col_cb.get()], keep="first")
            else:
                new_df = df.drop_duplicates(keep="first")
            after = len(new_df)
            dup   = before - after

            folder, name_ext = os.path.split(file_path.get())
            name, ext = os.path.splitext(name_ext)
            out_path = os.path.join(save_dir.get(), f"{name}_去重结果{ext}")
            new_df.to_excel(out_path, index=False)

            messagebox.showinfo("✅ 去重完成",
                f"处理成功！\n\n"
                f"去重前：{before} 行\n"
                f"重复项：{dup} 行\n"
                f"去重后：{after} 行\n"
                f"已保存到：\n{out_path}")
            win.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"失败：{str(e)}")

    # 使用 pack 布局
    tk.Label(content, text="📊 表格去重",
             font=("微软雅黑", 16, "bold"), bg=BG, fg=TITLE_FG).pack(pady=(18, 8))

    RoundButton(content, text="1. 选择 Excel 文件", command=select_file,
                width=230, height=44).pack(pady=3)
    tk.Entry(content, textvariable=file_path, font=("微软雅黑", 10),
             width=52, state="readonly", relief="flat",
             bg=ENTRY_BG, fg=BTN_FG).pack(pady=2)

    RoundButton(content, text="2. 选择保存目录", command=select_save,
                width=230, height=44).pack(pady=3)
    tk.Entry(content, textvariable=save_dir, font=("微软雅黑", 10),
             width=52, state="readonly", relief="flat",
             bg=ENTRY_BG, fg=BTN_FG).pack(pady=4)

    tk.Label(content, text="3. 去重模式", bg=BG,
             font=("微软雅黑", 10, "bold"), fg=BTN_FG).pack(pady=4)
    mode_frame = tk.Frame(content, bg=BG)
    mode_frame.pack(pady=2)
    for txt, val in [("按指定列去重", "col"), ("整行完全重复去重", "row")]:
        tk.Radiobutton(mode_frame, text=txt, variable=mode, value=val,
                       bg=BG, fg=BTN_FG, selectcolor="#fce4ef",
                       activebackground=BG, font=("微软雅黑", 10)).pack(side="left", padx=10)

    tk.Label(content, text="4. 选择去重依据列", bg=BG,
             font=("微软雅黑", 10, "bold"), fg=BTN_FG).pack(pady=4)

    style = ttk.Style()
    style.configure("Pink.TCombobox", fieldbackground=ENTRY_BG, background=ENTRY_BG)
    col_cb = ttk.Combobox(content, width=30, font=("微软雅黑", 11),
                          state="readonly", style="Pink.TCombobox")
    col_cb.pack(pady=2)

    RoundButton(content, text="✅ 开始去重", command=start_remove,
                bg=OK_BG, hover=OK_HO, fg=OK_FG,
                width=220, height=46).pack(pady=18)

    # 动态计算窗口大小
    win.update_idletasks()
    w = max(win.winfo_reqwidth() + 40, 560)
    h = max(win.winfo_reqheight() + 20, 560)
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    win.minsize(500, 500)
